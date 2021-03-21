from pathlib import Path


def _read(file: Path) -> str:
    with open(file, "r") as f:
        return f.read()


def _write(file: Path, data):
    with open(file, "w") as f:
        f.write(data)


class TemplateService:

    def template(self, work_dir: Path, name: str, subdomain: str):
        if subdomain is None:
            subdomain = name
        self.templateReadme(work_dir, name)
        technical_name = name.lower()
        self.template_jenkinsfile(work_dir, technical_name, subdomain.lower())
        self.template_package("package.json", work_dir, technical_name)
        self.template_package("package-lock.json", work_dir, technical_name)
        self.create_dotenv(work_dir)
        print('edited template')

    def template_package(self, package_json, work_dir, name):
        package = work_dir.joinpath(package_json)
        data = _read(package)
        data = data.replace("\"name\": \"Web-Starter\"", f"\"name\": \"{name}\"")
        _write(package, data)

    def template_jenkinsfile(self, work_dir, name, subdomain):
        jenkinsfile = work_dir.joinpath("Jenkinsfile")
        data = _read(jenkinsfile)
        data = data.replace("alexanderwyss/web-starter", f"alexanderwyss/{name}") \
            .replace("docker stop web-starter", f"docker stop {name}") \
            .replace("docker rm -f web-starter", f"docker rm -f {name}") \
            .replace("--name web-starter", f"--name {name}") \
            .replace("web-starter.wyss.tech", f"{subdomain}.wyss.tech") \
            .replace("\n    /*", "") \
            .replace("\n    */", "")
        _write(jenkinsfile, data)

    def templateReadme(self, work_dir, name):
        readme = work_dir.joinpath("README.md")
        data = _read(readme)
        data = data.replace("# Web-Starter", f"# {name}")
        _write(readme, data)

    def create_dotenv(self, work_dir):
        work_dir.joinpath(".env").touch()
