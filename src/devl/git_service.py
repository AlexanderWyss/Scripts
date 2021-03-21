import os
import re
from pathlib import Path
from git import Git, Repo


class GitService:
    def __init__(self, work_dir=None):
        if work_dir is None:
            work_dir = os.getcwd()
        self._work_dir = work_dir
        self._git = Git(work_dir)
        self._remote_url = None
        self._name = None
        self._domain = None
        self._user = None

    def init_from_remote(self):
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

    def init(self, ssh_url):
        repo = Repo.init()
        repo.create_remote('origin', ssh_url)
        readme = Path('README.md')
        if not readme.exists():
            readme.touch()
        repo.index.add('README.md')
        repo.index.commit('init')
        self._git.execute("git push --set-upstream origin master")
        print("Created repo")