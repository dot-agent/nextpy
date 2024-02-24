import os
import re
import sys
from typing import Optional
from nextpy.interfaces.jupyter.minisettings import BaseSettings

HOST_DEFAULT = os.environ.get("HOST", "localhost")
is_mac_os_conda = "arm64-apple-darwin" in HOST_DEFAULT
is_wsl_windows = re.match(r".*?-w1[0-9]", HOST_DEFAULT)
if is_mac_os_conda or is_wsl_windows:
    HOST_DEFAULT = "localhost"

class MainSettings(BaseSettings):
    use_pdb: bool = False
    mode: str = "production"
    tracer: bool = False
    timing: bool = False
    root_path: Optional[str] = None  # e.g. /myapp (without trailing slash)
    base_url: str = ""  # e.g. https://myapp.widget.run/myapp/
    platform: str = sys.platform
    host: str = HOST_DEFAULT
    experimental_performance: bool = False

    class Config:
        env_prefix = "solara_"
        case_sensitive = False
        env_file = ".env"

main = MainSettings()