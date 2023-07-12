class Config:
    __conf = {
        "toggl_api_token": "",
        "plex_username": "",
        "mapping": [{"libraries": ["TV Shows", "Movies"], "project": "Watching TV"}],
    }

    __setters = __conf.keys()

    @staticmethod
    def get(name):
        return Config.__conf[name]

    @staticmethod
    def set(name, value):
        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")


def configure(
    toggl_api_token: str,
    plex_username: str,
    mapping: "list[dict]" = None,
):

    Config.set("toggl_api_token", toggl_api_token)
    Config.set("plex_username", plex_username)
    Config.set("mapping", mapping)
