import os
import sys
import uuid
import subprocess
from typing import Optional
from nextpy.sandbox.kernals.jupyter import JupyterKernel

class SandBox:
    def __init__(self, session_id: Optional[str] = None, work_dir: str = ".sandbox") -> None:
        self.session_id = session_id or str(uuid.uuid4())
        os.makedirs(work_dir, exist_ok=True)
        self.kernel = JupyterKernel(work_dir)

    def start(self) -> str:
        # Jupyter Kernel is started in the JupyterKernel __init__ method
        return "Jupyter Kernel started."

    def stop(self) -> str:
        self.kernel.restart_jupyter_kernel()
        return "SandBox stopped."

    def run_code(self, code: str) -> str:
        text_output, _ = self.kernel.execute_code(code)
        return text_output

    def install_package(self, package_name: str) -> str:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], capture_output=True, text=True)
        return result.stdout or result.stderr

    def upload_file(self, file_name: str, content: bytes) -> str:
        with open(file_name, "wb") as file:
            file.write(content)
        return f"{file_name} uploaded."

    def download_file(self, file_name: str) -> bytes:
        with open(file_name, "rb") as file:
            return file.read()

    def _kernel_connection_file(self):
        connection_file = os.path.join(self.work_dir, f"kernel-{self.session_id}.json")
        with open(connection_file, "w") as f:
            f.write(self.kernel.get_connection_info_json())
        return connection_file