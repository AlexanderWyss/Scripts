import os

from github import Github


class GithubService:
    def __init__(self, token=None):
        if token is None:
            token = os.getenv('githubToken')
        self.github = Github(token)

    def add_webhook(self, repo_id, url='https://jenkins.wyss.tech/github-webhook/'):
        config = {
            "url": url,
            "content_type": "json",
        }
        self.github.get_repo(repo_id).create_hook(name='web', config=config, events=['push'], active=True)
        print(f"Created Webhook {repo_id}")

    def create_repo(self, name, private):
        repo = self.github.get_user().create_repo(name=name, private=private)
        print("Created Github repo")
        return repo
