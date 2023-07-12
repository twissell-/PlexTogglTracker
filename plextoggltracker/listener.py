import json
import logging

from flask import Blueprint, Response, request
from werkzeug.exceptions import BadRequestKeyError

from plextoggltracker.config import Config
from plextoggltracker.toggl import Toggl

logger = logging.getLogger("PlexTogglTracker")
webhook = Blueprint("PlexTogglTracker", __name__)


@webhook.route("/webhook", methods=["POST"])
def _webhook():
    mapping = Config.get("mapping")
    plex_username = Config.get("plex_username")
    toggl = Toggl()

    data = request.form.get("payload")
    if not data:
        logger.debug("Request does not have a payload.")
        return Response(status=200)

    data = json.loads(data)

    # event filter
    if (
        data["Account"]["title"] != plex_username
        or "media." not in data["event"]
        or data["Metadata"]["type"] not in ["episode", "movie"]
    ):
        logger.debug("Request ignored by filters.")
        return Response(status=200)

    metadata = data["Metadata"]

    project = {}
    for m in mapping:
        if metadata["librarySectionTitle"] in m["libraries"]:
            project = toggl.get_projects(name=m["project"])
            break

    if not project:
        logger.debug(
            "No mapping found for '{}' or project does not exists.".format(
                metadata["librarySectionTitle"]
            )
        )
        return Response(status=200)

    if data["event"] in ["media.play", "media.resume"]:
        if metadata["type"] == "episode":
            title = metadata["grandparentTitle"]
        else:
            title = metadata["title"]

        toggl.start_timer(title, project["id"])
        logger.info("Started timer: {} ({}).".format(title, project["name"]))
    if data["event"] in ["media.pause", "media.stop"]:
        toggl.stop_timer()
        logger.info("Stoped timer.")

    return Response(status=200)
