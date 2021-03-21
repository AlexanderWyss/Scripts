import re

from git import Git


class GitService:
    def __init__(self, work_dir):
        self._git = Git(work_dir)
        self._remote_url = self._git.execute("git remote get-url origin")
        matcher = re.match(r"git@(?P<domain>.+):(?P<user>.+)/(?P<name>.+).git", self._remote_url)
        self._name = matcher.group("name")
        self._domain = matcher.group("domain")
        self._user = matcher.group("user")

    def get_name(self):
        return self._name

    def get_ssh_url(self):
        return self._remote_url

    def get_http_url(self):
        return f"https://{self._domain}/{self._user}/{self._name}"

    def is_github(self):
        return self._domain == "github.com"

    def get_repo_id(self):
        return f"{self._user}/{self._name}"
