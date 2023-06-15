from datetime import datetime, timezone
import os
import requests
from rin import config


class Toggl:

    BASE_URL = "https://api.track.toggl.com/api/v9"
    HEADERS = {"content-type": "application/json"}

    def __init__(self, api_token="", app_name="rin"):
        self._app_name = app_name
        self._workspace = None

        if api_token:
            self._api_token = api_token
        elif os.environ.get("TOGGL_API_TOKEN"):
            self._api_token = os.environ.get("TOGGL_API_TOKEN")
        elif config.get("toggl_api_token"):
            self._api_token = config.get("toggl_api_token")
        else:
            raise ValueError("Missing toggl api key")

        self._auth = (api_token, "api_token")

    def _request(self, endpoint, params="", method="GET", body={}):
        url = Toggl.BASE_URL + endpoint

        if method == "POST":
            return requests.post(
                url,
                headers=Toggl.HEADERS,
                auth=self._auth,
                json=body,
                params=params,
            )
        elif method == "GET":
            return requests.get(
                url, headers=Toggl.HEADERS, auth=self._auth, params=params
            )
        elif method == "PATCH":
            return requests.patch(
                url, headers=Toggl.HEADERS, auth=self._auth, params=params
            )

    def get_workspace(self):
        if not self._workspace:
            self._workspace = self._request("/workspaces").json()[0]

        return self._workspace

    def get_projects(self, name: str = ""):
        workspace_id = self.get_workspace()["id"]
        endpoint = "/workspaces/{workspace_id}/projects".format(
            workspace_id=workspace_id
        )

        projects = self._request(endpoint).json()

        if name:
            project = list(filter(lambda x: x["name"] == name, projects))

            return project[0] if project else []
        else:
            return projects

    def get_running_timer(self):
        return self._request("/me/time_entries/current").json()

    def stop_timer(self):
        timer = self.get_running_timer()

        if not timer:
            return

        endpoint = (
            "/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop".format(
                workspace_id=timer["workspace_id"], time_entry_id=timer["id"]
            )
        )

        return self._request(endpoint, method="PATCH").json()

    def start_timer(self, description: str, project_id: int):
        workspace_id = self.get_workspace()["id"]
        endpoint = "/workspaces/{workspace_id}/time_entries".format(
            workspace_id=workspace_id
        )
        body = {
            "created_with": self._app_name,
            "description": description,
            "workspace_id": workspace_id,
            "project_id": project_id,
            "duration": -1,
            "start": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        return self._request(endpoint, method="POST", body=body).json()
