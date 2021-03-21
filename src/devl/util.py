import getopt
import os
import sys
import jenkins
from dotenv import load_dotenv
import jenkins_job_config


def main(args):
    if len(args) > 0:
        name = general_args(args[1:])
        value = args[0]
        if value in ("j", "jenkins"):
            validate_args(name)
            create_jenkins_job(name)
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


def create_jenkins_job(name):
    server = jenkins.Jenkins('https://jenkins.wyss.tech', username='admin', password=os.getenv('jenkinsPassword'))
    server.create_job(name, jenkins_job_config.config.replace("{{name}}", name))


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        print(e)
