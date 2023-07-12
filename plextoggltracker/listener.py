import json

from flask import Blueprint, Response, request

from plextoggltracker.config import Config
from plextoggltracker.toggl import Toggl

webhook = Blueprint("PlexTogglTracker", __name__)


@webhook.route("/webhook", methods=["POST"])
def _webhook():
    mapping = Config.get("mapping")
    plex_username = Config.get("plex_username")
    toggl = Toggl()

    data = json.loads(request.form["payload"])

    # event filter
    if (
        data["Account"]["title"] != plex_username
        or "media." not in data["event"]
        or data["Metadata"]["type"] not in ["episode", "movie"]
    ):
        return Response(status=200)

    metadata = data["Metadata"]

    project = {}
    for m in mapping:
        if metadata["librarySectionTitle"] in m["libraries"]:
            project = toggl.get_projects(name=m["project"])
            break

    if not project:
        return Response(status=200)

    if data["event"] in ["media.play", "media.resume"]:
        if metadata["type"] == "episode":
            title = metadata["grandparentTitle"]
        else:
            title = metadata["title"]

        toggl.start_timer(title, project["id"])
    if data["event"] in ["media.pause", "media.stop"]:
        toggl.stop_timer()

    return Response(status=200)
