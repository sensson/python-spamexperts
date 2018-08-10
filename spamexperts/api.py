import json
import requests
from spamexperts.exceptions import ApiException


class API(object):
    def __init__(self, url, username, password, debug=False):
        '''Set up the SpamExperts API

        url        -- the url the SpamExperts API
        username   -- the username to authenticate with
        password   -- the password to authenticate with'''

        self.url = "{}/api".format(url)
        self.username = username
        self.password = password
        self.debug = debug

    def get(self, controller, action, params={}):
        '''A basic GET request to the SpamExperts API.

        api/controller/action/<format>/param1/value/param2/value
        controller -- a string containing the API controller
        action     -- a string containing the API action
        params     -- a dict containing all parameters

        returns the response of the SpamExperts API.'''

        url = self.set_url(controller, action, params)
        response = requests.get(
            url,
            auth=(self.username, self.password),
        )

        # Basic debugging, it only returns the request and its output
        if self.debug is True:
            print("Sent request: {}".format(url))
            print("Got output {}".format(response.text))

        data = json.loads(response.text)

        # Basic error check, this doesn't raise specific exceptions but
        # does point you to the right controller/action.
        if 'error' in data['messages']:
            error_controller = "Error processing /api/{}/{}.".format(
                controller,
                action,
            )

            raise ApiException("{} {}".format(
                error_controller,
                ' '.join(data['messages']['error']),
            ))

        # If a call is successful we may get a 'success' message. In that
        # case, return the success message.
        if 'success' in data['messages']:
            return data['messages']['success']

        # Return the result
        return data['result']

    def set_url(self, controller, action, params={}):
        '''Set the url the client will consume from the SpamExperts API.

        api/controller/action/<format>/param1/value/param2/value
        controller -- a string containing the API controller
        action     -- a string containing the API action
        params     -- a dict containing all parameters

        returns the url that can be used by a get or post request'''

        # Handle formatting
        format = 'format/json'

        # Set the url
        params = params.items()
        return "{}/{}/{}/{}/{}/".format(
            self.url,
            controller,
            action,
            format,
            '/'.join("{}/{}".format(key, value) for key, value in params),
        )
