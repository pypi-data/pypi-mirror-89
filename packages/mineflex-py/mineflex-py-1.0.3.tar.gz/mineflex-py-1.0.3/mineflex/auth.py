from urllib.parse import urljoin
from requests import Session, codes
from .endpoint import UserEndpoint, ServerEndpoint
from .server import json_to_server
from .exceptions import *

from json.decoder import JSONDecodeError

failed_reference = {
    "404 page not found": APIMissingException,
    "Forbidden": InsufficientPermissions,
    "Server Must be in Running State to Execute Commands": ServerOfflineException
}


class MineflexSession(Session):
    def __init__(self, base_url=None, *args, **kwargs):
        super(MineflexSession, self).__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        request_result = super(MineflexSession, self).request(method, url, *args, **kwargs)
        error_reference = None

        try:
            request_json = request_result.json()

            if not isinstance(request_json, list):
                error_reference = failed_reference.get(
                    request_json.get("error")
                )
            # Inside try because json() might throw an error
        except JSONDecodeError:
            error_reference = failed_reference.get(request_result.text)

        if error_reference:
            raise error_reference(
                list(failed_reference.keys())[list(failed_reference.values()).index(error_reference)]
            )

        return request_result


class Mineflex:
    def __init__(self, email: str, password: str,
                 base_url: str = "https://mineflex.io/"):
        self.email = email
        self.password = password

        self.logged = False

        self.session = MineflexSession(base_url)

    def login(self):
        attempt = self.session.post(
            UserEndpoint.login.value,
            json={
                "email": self.email,
                "password": self.password
            }
        )
        attempt_json = attempt.json()

        if not attempt_json.get("Authorized"):
            raise InvalidCredentials(attempt_json.get("Message"))

        self.logged = True
        return True

    def get_all_server(self):
        all_server = self.session.get(ServerEndpoint.list.value).json()
        return_list = []

        for server in all_server:
            print(server)
            return_list.append(
                json_to_server(self.session, server)
            )

        return return_list

    def get_server(self, id):
        server = self.session.get(
            "%s/%s" % (ServerEndpoint.list.value, str(id))
        ).json()
        print(server)
        return json_to_server(self.session, server)

        # session, id: int, user_id: int, ram: int, protocol: Protocol, domain: str, state: str, host: int,
        # datacenter: DataCenter, description: str, server_type: ServerType, image: MineflexImage {"id": 244,
        # "userId": 191, "ram": "5G", "protocolVersion": 753, "protocolName": "1.16.3", "domain":
        # "vibingcrusaders.us1.mineflex.io", "state": "STOPPED", "host": 1, "datacenter": "", "maxPlayers": 10,
        # "description": "just vibing", "serverType": "PAPER", "imageId": 18}
