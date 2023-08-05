from enum import Enum
from .endpoint import ServerEndpoint, PlayerEndpoint
from .player import MinecraftPlayer


def json_to_server(session, json):
    return Server(session, id=json.get("id"), user_id=json.get("userId"), ram=json.get("ram"),
                  protocol_version=json.get("protocolVersion"),
                  protocol_name=json.get("protocolName"),
                  domain=json.get("domain"), state=json.get("state"), host=json.get("host"),
                  datacenter=json.get("datacenter"), max_player=json.get("maxPlayers"),
                  description=json.get("description"), server_type=json.get("serverType"))


class MineflexImage:
    def __init__(self, URL: str):
        self.URL = URL


class DataCenter(Enum):
    BHS = "US1"


class ServerState(Enum):
    stopped = "STOPPED"
    stopping = "STOPPING"
    running = "RUNNING"


class ServerType(Enum):
    paper = "PAPER"


class Protocol:
    def __init__(self, name: str, version: int, title: str, image: MineflexImage,
                 server_type: ServerType, build: int):
        self.name = name
        self.version = version
        self.title = title
        self.image = image
        self.server_type = server_type
        self.build = build


class Server:
    def __init__(self, session,
                 id: int,
                 user_id: int,
                 ram: int,
                 protocol_version: int,
                 protocol_name: str,
                 domain: str,
                 state: str,
                 host: int,
                 description: str,
                 server_type: ServerType or str,
                 max_player: int,
                 datacenter: DataCenter or str = None,
                 image_id: str = None):

        # imageId and datacenter is empty sometime, leaving it optional is the best
        # way to deal with it

        for (key, value) in locals().items():
            setattr(self, key, value)

        self.session = session

        if self.datacenter and not isinstance(self.datacenter, DataCenter):
            self.datacenter = DataCenter[self.datacenter]
        if not isinstance(self.server_type, ServerType):
            self.server_type = ServerType[self.server_type.lower()]

        self.protocol = self.get_protocol()

    def get_logs(self):
        return self.session.get(ServerEndpoint.logs.value + str(self.id)).json()['logs']

    def get_protocol(self):
        all_ver = self.session.get(
            ServerEndpoint.version_endpoint.value[self.server_type.name].value
        ).json()

        for ver in all_ver:
            if ver['protocolName'] == self.protocol_name:
                return Protocol(
                    ver['protocolName'], ver['protocolVersions'], ver['title'], MineflexImage(ver['imageUrl']),
                    ServerType[ver['serverType'].lower()], build=ver['build']
                )

    def ban_player(self, player: MinecraftPlayer):
        player.ban(self.id)

    def get_user(self):
        all_user_json = self.session.get(PlayerEndpoint.config.value + str(self.id)).json()
        all_user = []

        for user in all_user_json['playerList']:
            all_user.append(MinecraftPlayer(
                self.session,
                user['name'],
                user['uuid'],
                user['expiresOn'],
                user['bypassesPlayerLimit'],
                user['banned'],
                user['operator']
            ))

        return all_user

    def update_information(self):
        new_server = json_to_server(
            self.session,
            self.session.get("%s/%s" % (ServerEndpoint.list.value, str(self.id))).json()
        )

        self = new_server
