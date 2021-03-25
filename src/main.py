import os
import shutil
import winshell
import PyInstaller.__main__

root_path = "C:\\Users\\alexs\\development\\Scripts"
python = f"{root_path}\\venv\\Scripts\\python.exe"
tools_path = f"{root_path}\\Tools"
exec_path = f"{root_path}\\path"
spec_path = f"{root_path}\\spec"
build_path = f"{root_path}\\build"
dotenv_path = f"{root_path}\\.env"

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


def add_to_path(file, name):
    PyInstaller.__main__.run([
        f"src\\{file}",
        f"--distpath={exec_path}",
        f"--specpath={spec_path}",
        f"--workpath={build_path}",
        "--onefile",
        f"--name={name}"
    ])


def copy_dotenv():
    shutil.copyfile(dotenv_path, f"{exec_path}\\.env")


def create_links():
    if not os.path.exists(tools_path):
        os.mkdir(tools_path)
    # taskschd.msc
    create_link("GPU_Startup", gpu, "-s")
    create_link("iGPU", gpu, "-c iGPU")
    create_link("eGPU", gpu, "-c eGPU")
    add_to_path(gpu, "gpu")
    add_to_path("devl\\util.py", "util")
    copy_dotenv()


if __name__ == '__main__':
    create_links()
