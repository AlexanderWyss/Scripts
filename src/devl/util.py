import getopt
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from jenkins_service import JenkinsService
from git_service import GitService
from github_service import GithubService
from templat_service import TemplateService


def jenkins_job(work_dir):
    git = GitService(work_dir)
    git.init_from_remote()
    jenkins = JenkinsService()
    jenkins.create_job(git.get_name(), git.get_ssh_url(), git.get_http_url())
    git_webhook(work_dir)


def git_webhook(work_dir):
    git = GitService(work_dir)
    git.init_from_remote()
    if git.is_github():
        github = GithubService()
        github.add_webhook(git.get_repo_id())
    else:
        print('Not a github repo. Webhook could not be added.')


def init_repo(work_dir, private, auto_commit_all):
    name = os.path.basename(os.getcwd())
    github = GithubService()
    repo = github.create_repo(name, private)
    git = GitService(work_dir)
    git.init(repo.ssh_url, auto_commit_all)


def starter(name, private, subdomain):
    github = GithubService()
    repo = github.create_repo(name, private)
    path = Path(name)
    path.mkdir()
    git = GitService(str(path))
    git.from_template(repo.ssh_url)
    github.add_webhook(repo.full_name)
    jenkins = JenkinsService()
    jenkins.create_job(name, repo.ssh_url, repo.html_url)
    jenkins.build(name)
    template(path, name, subdomain)
    git.commit("Edit Template")


def template(path: Path, name, subdomain):
    templater = TemplateService()
    templater.template(path, name, subdomain)


def main(args):
    if len(args) > 0:
        value = args[0]
        name, private, auto_commit_all, subdomain, work_dir = general_args(args[1:])
        if value in ("j", "jenkins"):
            jenkins_job(work_dir)
        elif value in ("wh", "webhook"):
            git_webhook(work_dir)
        elif value in ("i", "init"):
            init_repo(work_dir, private, auto_commit_all)
        elif value in ("s", "starter"):
            validate_args(name)
            starter(name, private, subdomain)
        elif value in ("t", "template"):
            validate_args(name)
            template(Path(work_dir), name, subdomain)
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
    auto_commit_all = False
    subdomain = None
    work_dir = os.getcwd()
    opts, args = getopt.getopt(args, "n:pad:w:", ["name=", "private", "all", "domain=", "workdir="])
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            if arg == ".":
                name = os.path.basename(os.getcwd())
            else:
                name = arg
        elif opt in ("-p", "--private"):
            private = True
        elif opt in ("-a", "--all"):
            auto_commit_all = True
        elif opt in ("-d", "--domain"):
            subdomain = arg
        elif opt in ("-w", "--workdir"):
            work_dir = arg
        else:
            raise Exception(f"Unknown argument: {opt}")
    return name, private, auto_commit_all, subdomain, work_dir


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        print(e)
