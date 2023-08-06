from spell.api import base_client
from spell.api.utils import url_path_join


PROJECT_RESOURCE_URL = "projects"


class ProjectsClient(base_client.BaseClient):
    def create_project(self, proj_req):
        r = self.request("post", url_path_join(PROJECT_RESOURCE_URL, self.owner), payload=proj_req)
        self.check_and_raise(r)
        resp = self.get_json(r)
        return resp["project"]

    def list_projects(self):
        r = self.request("get", url_path_join(PROJECT_RESOURCE_URL, self.owner))
        self.check_and_raise(r)
        resp = self.get_json(r)
        return resp["projects"]

    def get_project(self, id):
        r = self.request("get", url_path_join(PROJECT_RESOURCE_URL, self.owner, id))
        self.check_and_raise(r)
        resp = self.get_json(r)
        return resp["project"]
