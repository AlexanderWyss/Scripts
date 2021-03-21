from github import Github


class GithubService:
    def __init__(self, token):
        self.github = Github(token)

    def add_webhook(self, repo_id, url):
        config = {
            "url": url,
            "content_type": "json",
        }
        self.github.get_repo(repo_id).create_hook(name='web', config=config, events=['push'], active=True)
        print(f"Created Webhook {repo_id}")
