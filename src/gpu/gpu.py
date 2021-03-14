import subprocess
import re
from enum import Enum


class Status(Enum):
    Enabled = 1
    Disabled = 2
    Missing = 3


class GPU(object):
    @staticmethod
    def e_gpu():
        return GPU("PCI\\VEN_10DE&DEV_13C2&SUBSYS_36831458&REV_A1", "eGPU")

    @staticmethod
    def i_gpu():
        return GPU("PCI\\VEN_10DE&DEV_1F91&SUBSYS_22A817AA&REV_A1", "iGPU")

    def __init__(self, device_id, gpu_type):
        self.device_id = device_id
        self.gpu_type = gpu_type
        self.status = Status.Missing
        self.name = None
        self.refresh()

    def refresh(self):
        lines = self._run("status")
        if len(lines) == 1:
            self.status = Status.Missing
            self.name = None
        else:
            matching_device_amount = GPU._parse_device_amount(lines)
            if matching_device_amount == 1:
                self.name = GPU._parse_name(lines[1])
                self.status = GPU._parse_status(lines[2])
                print(f"{self.gpu_type} Name: '{self.name}', Status: '{self.status.name}'")
            else:
                raise Exception(
                    f"Not specific enough id. Matching devices: '{matching_device_amount}', id: '{self.device_id}'")

    def enable(self):
        if self.status == Status.Disabled:
            print(f"Enabling {self.gpu_type} {self.name}")
            self._run("enable", log=True)
        elif self.status == Status.Enabled:
            print(f"{self.gpu_type} {self.name} already enabled.")
        else:
            raise Exception(f"Unexpected {self.gpu_type} status: '{self.status.name}', id: {self.device_id}")

    def disable(self):
        if self.status == Status.Enabled:
            print(f"Disabling {self.gpu_type} {self.name}")
            self._run("disable", log=True)
        elif self.status == Status.Disabled:
            print(f"{self.gpu_type} {self.name} already disabled.")
        elif self.status == Status.Missing:
            print(f"{self.gpu_type} cannot be disabled. GPU not found.")
        else:
            raise Exception(f"Unexpected {self.gpu_type} status: '{self.status.name}', id: {self.device_id}")

    def _run(self, command, log=False):
        process = subprocess.run(f'./util/devcon {command} "{self.device_id}"', capture_output=True, timeout=60,
                                 check=True)
        if log:
            print(process.stdout.decode("utf-8"))
        return [line.decode("utf-8").strip() for line in process.stdout.splitlines()]

    @staticmethod
    def _parse_device_amount(lines):
        return int(re.match(r"(?P<amount>\d+) matching device\(s\) found\.", lines[len(lines) - 1]).group("amount"))

    @staticmethod
    def _parse_status(line) -> Status:
        if "running" in line:
            return Status.Enabled
        elif "disabled" in line:
            return Status.Disabled
        else:
            return Status.Missing

    @staticmethod
    def _parse_name(line) -> str:
        return re.match(r"Name: (?P<name>.+)", line).group("name")
