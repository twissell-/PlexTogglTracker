import json
from flask import Flask, request, Response
from rin import config
from rin.toggl import Toggl

listener = Flask(__name__)

_toggl = Toggl()
_endpoint = "/" + config.get("endpoint")
_mapping = config.get("mapping")
_plex_username = config.get("plex_username")


@listener.route(_endpoint, methods=["POST"])
def plex_webhook():
    if request.method == "POST":
        data = json.loads(request.form["payload"])

        # event filter
        if (
            data["Account"]["title"] != _plex_username
            or "media." not in data["event"]
            or data["Metadata"]["type"] not in ["episode", "movie"]
        ):
            return Response(status=200)

        metadata = data["Metadata"]

        project = {}
        for m in _mapping:
            if metadata["librarySectionTitle"] in m["libraries"]:
                project = _toggl.get_projects(name=m["project"])
                break

        if not project:
            return Response(status=200)

        if data["event"] in ["media.play", "media.resume"]:
            if metadata["type"] == "episode":
                title = metadata["grandparentTitle"]
            else:
                title = metadata["title"]

            _toggl.start_timer(title, project["id"])
        if data["event"] in ["media.pause", "media.stop"]:
            _toggl.stop_timer()

        return Response(status=200)
