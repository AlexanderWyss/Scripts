import os
from typing import Tuple, Any

from paramiko import SSHClient
from paramiko.channel import ChannelFile, ChannelStderrFile, ChannelStdinFile


def types(args: Tuple[Any, Any, Any]) -> Tuple[ChannelStdinFile, ChannelFile, ChannelStderrFile]:
    return args


class SshService:
    def __init__(self):
        self._client = SSHClient()

    def login(self, username="alexander", hostname='laptop'):
        self._client.load_system_host_keys()
        self._client.connect(hostname=hostname, username=username)

    def exit(self):
        self._client.close()

    def exec(self, command):
        stdin, stdout, stderr = types(self._client.exec_command(command))
        self._handle_error(stderr)
        return self._handle_out(stdout)

    def sudo_exec(self, command):
        stdin, stdout, stderr = types(self._client.exec_command(f"sudo -S {command}"))
        if stdin.writable():
            stdin.write(os.getenv('sudoPass') + '\n')
            stdin.flush()
        self._handle_error(stderr)
        return self._handle_out(stdout)

    def _handle_error(self, stderr):
        if stderr.readable():
            err = stderr.read()
            if len(err) > 0 and not err.startswith(b'[sudo] password for '):
                raise Exception(err)

    def _handle_out(self, stdout):
        if stdout.readable():
            return stdout.read()
        else:
            return None
