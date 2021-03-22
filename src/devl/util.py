import getopt
import os
import sys
import traceback
from pathlib import Path
from dotenv import load_dotenv
from jenkins_service import JenkinsService
from git_service import GitService
from github_service import GithubService
from proxy_service import ProxyService
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
    template(path, name, subdomain)
    git.commit("Edit Template")
    github.add_webhook(repo.full_name)
    jenkins = JenkinsService()
    jenkins.create_job(name, repo.ssh_url, repo.html_url)
    jenkins.build(name)
    print("https://ap.www.namecheap.com/Domains/DomainControlPanel/wyss.tech/advancedns")


def template(path: Path, name, subdomain):
    templater = TemplateService()
    templater.template(path, name, subdomain)


def add_auth(name, subdomain, htpasswd_suffix):
    service = ProxyService()
    service.create_auth_config(subdomain, name, htpasswd_suffix)


def list_auth():
    service = ProxyService()
    for auth in service.get_auth_list():
        print(auth)


def main(args):
    if len(args) > 0:
        value = args[0]
        name, private, auto_commit_all, subdomain, work_dir, htpasswd_suffix = general_args(args[1:])
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
        elif value in ("a", "auth"):
            validate_args(subdomain)
            add_auth(name, subdomain, htpasswd_suffix)
        elif value in ("la", "list-auth"):
            list_auth()
        else:
            print_help()
            raise Exception("What do you want to do?")
    else:
        print_help()
        raise Exception("What do you want to do?")


def validate_args(*args):
    for arg in args:
        if arg is None:
            raise Exception("Required arg missing.")


def general_args(args) -> object:
    name = None
    private = False
    auto_commit_all = False
    subdomain = None
    work_dir = os.getcwd()
    htpasswd_suffix = None
    opts, args = getopt.getopt(args, "n:pad:w:h:", ["name=", "private", "all", "domain=", "workdir=", "htpasswd="])
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
        elif opt in ("-h", "--htpasswd"):
            htpasswd_suffix = arg
        else:
            print_help()
            raise Exception(f"Unknown argument: {opt}")
    return name, private, auto_commit_all, subdomain, work_dir, htpasswd_suffix


def print_help():
    print("Util Scripts")
    print("j/jenkins : create jenkins job and create Webhook [Git repo required] P:(w)")
    print("wh/webhook : creates jenkins Webhook [Git repo required] P:(w)")
    print("i/init : create git repo locally and github in current dir P:(w, p, a)")
    print("s/starter : creates a project form Web-Starter template P:(n, p, d)")
    print("t/template : templates a Web-Starter project P:(w, n, d)")
    print("a/auth : add proxy auth for domain P:(n, d, h)")
    print("la/list-auth : lists registered auth on proxy P:()")
    print("Params: (P:)")
    print("-n/--name= : Name")
    print("-p/--private : created Github repo is set to private")
    print("-a/--all : auto commit all")
    print("-d/--domain= : subdomain of site")
    print("-w/--workdir= : working directory")
    print("-h/--htpasswd= : password file suffix")


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        traceback.print_exc()
        print(e)
