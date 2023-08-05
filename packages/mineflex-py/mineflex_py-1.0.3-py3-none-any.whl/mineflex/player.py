from .endpoint import PlayerEndpoint
from enum import Enum


class user_action(Enum):
    ban = "Ban"


class MinecraftPlayer:
    def __init__(
            self, session,
            name: str,
            uuid: str,
            expires_on: str,
            bypass_player_limit: bool,
            banned: bool,
            operator: str
    ):
        self.session = session

        for (key, value) in locals().items():
            setattr(self, key, value)

    def action(self, action_type: user_action or str, server_id: int or str):
        action_value = action_type

        if isinstance(action_type, user_action):
            action_value = action_type.value

        return self.session.post(PlayerEndpoint.command.value + str(server_id), json={
            "command": action_value,
            "player": self.name
        }).ok

# {
#   "playerList": [
#     {
#       "name": "BigNutBoi",
#       "uuid": "10c6b8a1-5c74-4038-b629-83f61f763016",
#       "expiresOn": "2020-12-12 10:24:47 +0000",
#       "bypassesPlayerLimit": false,
#       "banned": false,
#       "operator": false
#     },
#     {
#       "name": "Nunui",
#       "uuid": "444eda4d-9c61-4459-8e68-c6c78e35fb8a",
#       "expiresOn": "2020-12-18 04:38:13 +0000",
#       "bypassesPlayerLimit": false,
#       "banned": false,
#       "operator": false
#     },
#     {
#       "name": "_Pnlmon",
#       "uuid": "b52f6a6f-5b2e-4c16-b88b-608a89001420",
#       "expiresOn": "2020-12-02 07:02:09 +0000",
#       "bypassesPlayerLimit": false,
#       "banned": false,
#       "operator": false
#     },
#     {
#       "name": "evangelos08",
#       "uuid": "29ce9c41-ecf2-4424-9673-d97690b7a4f7",
#       "expiresOn": "2020-12-02 09:39:13 +0000",
#       "bypassesPlayerLimit": false,
#       "banned": false,
#       "operator": false
#     }
#   ],
#   "error": ""
# }
