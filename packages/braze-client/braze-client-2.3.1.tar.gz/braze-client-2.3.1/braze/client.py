import time

import requests
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_random_exponential

DEFAULT_API_URL = "https://rest.iad-02.braze.com"
USER_TRACK_ENDPOINT = "/users/track"
USER_DELETE_ENDPOINT = "/users/delete"
USER_EXPORT_ENDPOINT = "/users/export/ids"
#: Endpoint for Scheduled Trigger Campaign Sends
CAMPAIGN_TRIGGER_SCHEDULE_CREATE = "/campaigns/trigger/schedule/create"
MAX_RETRIES = 3
# Max time to wait between API call retries
MAX_WAIT_SECONDS = 1.25


class BrazeClientError(Exception):
    """
    Represents any Braze Client Error.

    https://www.braze.com/docs/developer_guide/rest_api/user_data/#user-track-responses
    """

    pass


class BrazeRateLimitError(BrazeClientError):
    def __init__(self, reset_epoch_s):
        """
        A rate limit error was encountered.

        :param float reset_epoch_s: Unix timestamp for when the API may be called again.
        """
        self.reset_epoch_s = reset_epoch_s
        super(BrazeRateLimitError, self).__init__()


class BrazeInternalServerError(BrazeClientError):
    """
    Used for Braze API responses where response code is of type 5XX suggesting
    Braze side server errors.
    """

    pass


def _wait_random_exp_or_rate_limit():
    """Creates a tenacity wait callback that accounts for explicit rate limits."""
    random_exp = wait_random_exponential(multiplier=1, max=MAX_WAIT_SECONDS)

    def check(retry_state):
        """
        Waits with either a random exponential backoff or attempts to obey rate limits
        that Braze returns.

        :param tenacity.RetryCallState retry_state: Info about current retry invocation
        :raises BrazeRateLimitError: If the rate limit reset time is too long
        :returns: Time to wait, in seconds.
        :rtype: float
        """
        exc = retry_state.outcome.exception()
        if isinstance(exc, BrazeRateLimitError):
            sec_to_reset = exc.reset_epoch_s - float(time.time())
            if sec_to_reset >= MAX_WAIT_SECONDS:
                raise exc
            return max(0.0, sec_to_reset)
        return random_exp(retry_state=retry_state)

    return check


class BrazeClient(object):
    """
    Client for Appboy public API. Support user_track.
    usage:
     from braze.client import BrazeClient
     client = BrazeClient(api_key='Place your API key here')
     r = client.user_track(
            attributes=[{
                'external_id': '1',
                'first_name': 'First name',
                'last_name': 'Last name',
                'email': 'email@example.com',
                'status': 'Active',
            }],
            events=None,
            purchases=None,
     )
    if r['success']:
        print 'Success!'
        print r
    else:
        print r['client_error']
        print r['errors']
    """

    def __init__(self, api_key, api_url=None, use_auth_header=False):
        self.api_key = api_key
        self.api_url = api_url or DEFAULT_API_URL
        self.use_auth_header = use_auth_header
        self.session = requests.Session()
        self.request_url = ""

    def user_track(self, attributes=None, events=None, purchases=None):
        """
        Record custom events, user attributes, and purchases for users.
        :param attributes: dict or list of user attributes dict (external_id, first_name, email)
        :param events: dict or list of user events dict (external_id, app_id, name, time, properties)
        :param purchases: dict or list of user purchases dict (external_id, app_id, product_id, currency, price)
        :return: json dict response, for example: {"message": "success", "errors": [], "client_error": ""}
        """
        if attributes is events is purchases is None:
            raise ValueError(
                "Bad arguments, at least one of attributes, events or purchases must be "
                "non None"
            )
        self.request_url = self.api_url + USER_TRACK_ENDPOINT

        payload = {}

        if events:
            payload["events"] = events
        else:
            payload["events"] = []

        if attributes:
            payload["attributes"] = attributes
        else:
            payload["attributes"] = []

        if purchases:
            payload["purchases"] = purchases
        else:
            payload["purchases"] = []

        return self.__create_request(payload=payload)

    def user_delete(self, external_ids):
        """
        Delete user from braze.
        :param external_ids: dict or list of user external ids
        :return: json dict response, for example: {"message": "success", "errors": [], "client_error": ""}
        """
        if not external_ids:
            raise ValueError("No external ids specified")

        self.request_url = self.api_url + USER_DELETE_ENDPOINT

        payload = {"external_ids": external_ids}

        return self.__create_request(payload=payload)

    def user_export(self, external_ids=None, email=None, fields_to_export=None):
        """
        Export user profiles from braze. One or both of ``external_ids`` or ``email``
        must be provided. Braze allows exporting multiple user profiles through
        ``external_ids`` but only one with the ``email`` argument.
        ref: https://www.braze.com/docs/developer_guide/rest_api/export/

        :param list[str] external_ids:
            optional list of braze external ids whose profiles are to be exported.
        :param str email:
            optional email for a braze profile whose data will be exported.
        :param list[str] fields_to_export:
            optional list of fields to export. If not specified braze exports all fields,
            with a warning that this may slow down the API response time. See API doc for
            list of valid fields.
        :return: json dict response from braze
        """
        if external_ids is email is None:
            raise ValueError("At least one of external_ids or email must be specified")

        self.request_url = self.api_url + USER_EXPORT_ENDPOINT

        payload = {}

        if external_ids:
            payload["external_ids"] = external_ids
        elif email:
            payload["email_address"] = email

        if fields_to_export:
            payload["fields_to_export"] = fields_to_export

        return self.__create_request(payload)

    def __create_request(self, payload):

        if not self.use_auth_header:
            payload["api_key"] = self.api_key

        response = {"errors": []}
        r = self._post_request_with_retries(payload)
        response.update(r.json())
        response["status_code"] = r.status_code

        message = response["message"]
        response["success"] = (
            message in ("success", "queued") and not response["errors"]
        )

        if message != "success":
            # message contains the fatal error message from Braze
            raise BrazeClientError(message, response["errors"])

        if "status_code" not in response:
            response["status_code"] = 0

        if "message" not in response:
            response["message"] = ""

        return response

    @retry(
        reraise=True,
        wait=_wait_random_exp_or_rate_limit(),
        stop=stop_after_attempt(MAX_RETRIES),
    )
    def _post_request_with_retries(self, payload):
        """
        :param dict payload:
        :rtype: requests.Response
        """

        headers = {}
        # Prior to April 2020, API keys would be included as a part of the API request body or within the request URL
        # as a parameter. Braze now has updated the way in which we read API keys. API keys are now set with the HTTP
        # Authorization request header, making your API keys more secure.
        # https://www.braze.com/docs/api/api_key/#how-can-i-use-it
        if self.use_auth_header:
            headers["Authorization"] = "Bearer {}".format(self.api_key)

        r = self.session.post(
            self.request_url, json=payload, timeout=2, headers=headers
        )
        # https://www.braze.com/docs/developer_guide/rest_api/messaging/#fatal-errors
        if r.status_code == 429:
            reset_epoch_s = float(r.headers.get("X-RateLimit-Reset", 0))
            raise BrazeRateLimitError(reset_epoch_s)
        elif str(r.status_code).startswith("5"):
            raise BrazeInternalServerError
        return r

    def campaign_trigger_schedule_create(
        self,
        campaign_id,
        schedule,
        send_id=None,
        broadcast=None,
        audience=None,
        recipients=None,
    ):
        """
        Send Messages via API Triggered Delivery at a specified time
        ref: https://www.braze.com/docs/developer_guide/rest_api/messaging/#schedule-endpoints

        :return: json dict response, for example: {"message": "success", "errors": [], "client_error": ""}
        """
        self.request_url = self.api_url + CAMPAIGN_TRIGGER_SCHEDULE_CREATE

        payload = {"campaign_id": campaign_id, "schedule": schedule}

        if send_id is not None:
            payload["send_id"] = send_id
        if broadcast is not None:
            payload["broadcast"] = broadcast
        if audience is not None:
            payload["audience"] = audience
        if recipients is not None:
            payload["recipients"] = recipients

        return self.__create_request(payload)
