import json

_CONFIG_PATH = "./config.json"


def get(identifier):
    try:
        config_file = open(_CONFIG_PATH)
        data = json.load(config_file)
        for key in identifier.split("."):
            data = data.get(key)
            if not data:
                return data
    except OSError as err:
        exit(
            'ERROR: Error reading file: "{configFile}". {error}'.format(
                configFile=_CONFIG_PATH, error=err
            )
        )
    except json.JSONDecodeError as err:
        print(err)
        exit(
            'ERROR: Error deconding file: "{configFile}"'.format(
                configFile=_CONFIG_PATH
            )
        )
    else:
        return data
