from ssh_service import SshService


class ProxyService:
    def __init__(self, auth_path='/docker/proxy/auth/', vhost_path='/docker/proxy/vhost.d/'):
        self._auth_path = auth_path
        self._vhost_path = vhost_path

    def create_auth_config(self, domain, name, htpasswd_suffix):
        ssh = SshService()
        try:
            ssh.login()
            ssh.exec(f"printf '{self.template_file(name, htpasswd_suffix)}' > {self._vhost_path}/{domain}")
            print(f'Created file: {self._vhost_path}/{domain}')
            print('Restarting proxy')
            ssh.sudo_exec("docker restart proxy")
        finally:
            ssh.exit()

    def template_file(self, name=None, htpasswd_suffix=None):
        if name is None:
            name = 'RESTRICTED ZONE'
        if htpasswd_suffix is None:
            htpasswd_suffix = ''
        return f'auth_basic "{name}";\n' + \
               f'auth_basic_user_file /etc/customauth/.htpasswd{htpasswd_suffix};'

    def get_auth_list(self):
        ssh = SshService()
        try:
            ssh.login()
            split = ssh.exec(f"ls {self._vhost_path}").split('\n')
            split.remove('default')
            split.remove('')
            return split
        finally:
            ssh.exit()
