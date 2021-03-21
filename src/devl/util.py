import getopt
import os
import sys
from dotenv import load_dotenv
from jenkins_service import JenkinsService
from git_service import GitService
from github_service import GithubService


def jenkins():
    git = GitService()
    service = JenkinsService()
    service.create_job(git.get_name(), git.get_ssh_url(), git.get_http_url())
    git_webhook()


def git_webhook():
    git = GitService()
    if git.is_github():
        github = GithubService()
        github.add_webhook(git.get_repo_id())
    else:
        print('Not a github repo. Webhook could not be added.')


def init_repo(private):
    name = os.path.basename(os.getcwd())
    github = GithubService()
    repo = github.create_repo('ScriptTestRepo', private)


def main(args):
    if len(args) > 0:
        name, private = general_args(args[1:])
        value = args[0]
        if value in ("j", "jenkins"):
            jenkins()
        elif value in ("wh", "webhook"):
            git_webhook()
        elif value in ("i", "init"):
            init_repo(private)
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
    private = False
    opts, args = getopt.getopt(args, "n:p", ["name=", "private"])
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            if arg == ".":
                name = os.path.basename(os.getcwd())
            else:
                name = arg
        elif opt in ("-p", "--private"):
            private = True
        else:
            raise Exception(f"Unknown argument: {opt}")
    return name, private


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        print(e)
