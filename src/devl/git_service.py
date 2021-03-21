import shutil
import re
from pathlib import Path
from git import Git, Repo


class GitService:
    def __init__(self, work_dir):
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

    def init(self, ssh_url, auto_commit_all=False):
        repo = Repo.init(self._work_dir)
        repo.create_remote('origin', ssh_url)
        if auto_commit_all:
            self._git.execute('git add -A')
        else:
            readme = Path(self._work_dir + '/README.md')
            if not readme.exists():
                readme.touch()
            repo.index.add('README.md')
        repo.index.commit('init')
        self._git.execute("git push --set-upstream origin master")
        print("Created local repo")

    def from_template(self, target_ssh_url, template_ssh_url='git@github.com:AlexanderWyss/Web-Starter.git'):
        self._git.execute(f"git clone {template_ssh_url} .")
        shutil.rmtree(self._work_dir + '/.git', ignore_errors=True)
        self.init(target_ssh_url, True)
        print("Created Repo from templated")

    def commit(self, message):
        self._git.execute('git add -A')
        self._git.execute(f'git commit -m "{message}"')
        self._git.execute('git push')
