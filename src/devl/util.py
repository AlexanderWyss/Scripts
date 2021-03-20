import os
import sys
import jenkins
from dotenv import load_dotenv
import jenkins_job_config


def main(argv):
    name = os.path.basename(os.getcwd())
    server = jenkins.Jenkins('https://jenkins.wyss.tech', username='admin', password=os.getenv('jenkinsPassword'))
    server.create_job(name, jenkins_job_config.config.replace("{{name}}", name))


if __name__ == '__main__':
    try:
        load_dotenv(dotenv_path="C:\\Users\\alexs\\development\\Scripts\\path\\.env")
        load_dotenv()
        main(sys.argv[1:])
    except Exception as e:
        print(e)

