import pathlib
import ssl
import subprocess
from typing import Optional
from urllib import request


class Processor:
    def __init__(
            self,
            user_agent: str,
            urls_file_path: str,
            robots_file_path: Optional[str] = None,
            robots_file_url: Optional[str] = None
    ):
        """
        :param user_agent: The user agent used
        :param urls_file_path: The urls file path
        :param robots_file_path: The robots.txt file path
        :param robots_file_url: The robots.txt file url
        """
        self.user_agent = user_agent
        self.urls_file_path = urls_file_path

        if robots_file_path:
            self.robots_file = robots_file_path
        elif robots_file_url:
            context = ssl._create_unverified_context()
            with request.urlopen(robots_file_url, context=context) as r:
                with open("robots.txt", "w") as robots_file:
                    content = r.read()
                    robots_file.write(content.decode("utf-8"))
                    self.robots_file = "robots.txt"
        else:
            raise InvalidConfigurationError("The robots.txt file path/url has to be specified")

    def run(self) -> str:
        root = pathlib.Path(__file__).parent.absolute()
        out = subprocess.run([
            f"{root}/main",
            f"-userAgent={self.user_agent}",
            f"-urlsFilePath={self.urls_file_path}",
            f"-robotsFilePath={self.robots_file}"
        ], capture_output=True)
        return str(out.stderr)


class InvalidConfigurationError(Exception):
    pass
