import os

import winshell

root_path = "C:\\Users\\alexs\\development\\Scripts"
python = f"{root_path}\\venv\\Scripts\\python.exe"
tools_path = f"{root_path}\\Tools"
gpu = "gpu\\main.py"


def as_admin(path):
    with open(path, "rb") as f2:
        ba = bytearray(f2.read())
    ba[0x15] |= 0x20
    with open(path, "wb") as f3:
        f3.write(ba)


def create_link(name, file, params):
    path = f"{tools_path}\\{name}.lnk"
    shortcut = winshell.shortcut(path)
    shortcut.path = f'{python}'
    shortcut.arguments = f'src\\{file} {params}'
    shortcut.working_directory = root_path
    shortcut.write()
    as_admin(path)


def create_links():
    if not os.path.exists(tools_path):
        os.mkdir(tools_path)
    #taskschd.msc
    create_link("GPU_Startup", gpu, "-s")
    create_link("iGPU", gpu, "-c iGPU")
    create_link("eGPU", gpu, "-c eGPU")


if __name__ == '__main__':
    create_links()
