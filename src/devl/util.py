import getopt
import os
import sys
from dotenv import load_dotenv
from jenkins_service import JenkinsService
from git_service import GitService
from github_service import GithubService


def jenkins():
    git = GitService(os.getcwd())
    service = JenkinsService(url='https://jenkins.wyss.tech', username='admin', password=os.getenv('jenkinsPassword'))
    service.create_job(git.get_name(), git.get_ssh_url(), git.get_http_url())
    git_webhook()


def git_webhook():
    git = GitService(os.getcwd())
    if git.is_github():
        github = GithubService(os.getenv('githubToken'))
        github.add_webhook(git.get_repo_id(), 'https://jenkins.wyss.tech/github-webhook/')
    else:
        print('Not a github repo. Webhook could not be added.')


def main(args):
    if len(args) > 0:
        name = general_args(args[1:])
        value = args[0]
        if value in ("j", "jenkins"):
            jenkins()
        elif value in ("wh", "webhook"):
            git_webhook()
        else:
            raise Exception("What do you want to do?")
    else:
        raise Exception("What do you want to do?")


def validate_args(*args):
    for arg in args:
        if arg is None:
            raise Exception("Required arg missing.")


def general_args(args):
    name = None
    opts, args = getopt.getopt(args, "n:", ["name="])
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            if arg == ".":
                name = os.path.basename(os.getcwd())
            else:
                name = arg
        else:
            raise Exception(f"Unknown argument: {opt}")
    return name


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        print(e)
