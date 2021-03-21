import jenkins
import jenkins_job_config


class JenkinsService:
    def __init__(self, url, username, password):
        self._server = jenkins.Jenkins(url=url, username=username, password=password)

    def create_job(self, name, ssh_url, http_url):
        self._server.create_job(name, jenkins_job_config.template_config(ssh_url, http_url))
        print(f"Created Jenkins job {name}")
