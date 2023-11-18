"""
Local implementation of AgentBox.
This is useful for testing and development.c
In case you don't put an api_key,
this is the default AgentBox.
"""

import asyncio
from queue import Queue
import threading
import json
import os
import subprocess
import sys
import time
from asyncio.subprocess import Process
from pathlib import Path
from typing import List, Optional, Union
from uuid import uuid4
import aiohttp
import requests
from websockets.client import WebSocketClientProtocol
from websockets.client import connect as ws_connect
from websockets.exceptions import ConnectionClosedError
from websockets.sync.client import ClientConnection
from websockets.sync.client import connect as ws_connect_sync
from openams.agentbox import BaseBox
from openams.schema import AgentBoxFile, AgentBoxOutput, AgentBoxStatus
from openams.config import settings


class TinyBox(BaseBox):
    """
    TinyBox is a AgentBox implementation that runs code locally.
    This is useful for testing and development.
    """

    _instance: Optional["TinyBox"] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        else:
            if settings.SHOW_INFO:
                print(
                    "INFO: Using a TinyBox which is not fully isolated\n"
                    "      and not scalable across multiple users.\n"
                    "      Make sure to use a AGENTBOX_API_KEY in production.\n"
                    "      Set envar SHOW_INFO=False to not see this again.\n"
                )
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.port: int = 8888
        self.kernel_id: Optional[dict] = None
        self.ws: Union[WebSocketClientProtocol, ClientConnection, None] = None
        self.jupyter: Union[Process, subprocess.Popen, None] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.message_queue = Queue()
        self.message_thread = threading.Thread(target=self._message_handler)
        self.message_thread.start()
        
    def _message_handler(self):
        while True:
            message = self.message_queue.get()
            if message == "STOP":
                break
            self._send_message_to_kernel(message)


    def _send_message_to_kernel(self, message):
        msg_json = json.dumps(message)
        if self.ws:
            try:
                self.ws.send(msg_json)
            except ConnectionClosedError:
                # Handle connection closed error if needed
                pass


    def start(self) -> AgentBoxStatus:
        os.makedirs(".agentbox", exist_ok=True)
        self._check_port()
        if settings.VERBOSE:
            print("Starting kernel...")
            out = None
        else:
            out = subprocess.PIPE
        self._check_installed()
        try:
            python = Path(sys.executable).absolute()
            self.jupyter = subprocess.Popen(
                [
                    python,
                    "-m",
                    "jupyter",
                    "kernelgateway",
                    "--KernelGatewayApp.ip='0.0.0.0'",
                    f"--KernelGatewayApp.port={self.port}",
                ],
                stdout=out,
                stderr=out,
                cwd=".agentbox",
            )
        except FileNotFoundError:
            raise ModuleNotFoundError(
                "Jupyter Kernel Gateway not found, please install it with:\n"
                "`pip install jupyter_kernel_gateway`\n"
                "to use the TinyBox."
            )
        while True:
            try:
                response = requests.get(self.kernel_url, timeout=90)
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                pass
            if settings.VERBOSE:
                print("Waiting for kernel to start...")
            time.sleep(1)

        response = requests.post(
            f"{self.kernel_url}/kernels",
            headers={"Content-Type": "application/json"},
            timeout=90,
        )
        self.kernel_id = response.json()["id"]
        if self.kernel_id is None:
            raise Exception("Could not start kernel")

        self.ws = ws_connect_sync(f"{self.ws_url}/kernels/{self.kernel_id}/channels")

        return AgentBoxStatus(status="started")

    def _check_port(self) -> None:
        try:
            response = requests.get(f"http://localhost:{self.port}", timeout=90)
        except requests.exceptions.ConnectionError:
            pass
        else:
            if response.status_code == 200:
                self.port += 1
                self._check_port()

    def _check_installed(self) -> None:
        """if jupyter-kernel-gateway is installed"""
        import pkg_resources  # type: ignore

        try:
            pkg_resources.get_distribution("jupyter-kernel-gateway")
        except pkg_resources.DistributionNotFound:
            print(
                "Make sure 'jupyter-kernel-gateway' is installed "
                "when using without a AGENTBOX_API_KEY.\n"
                "You can install it with 'pip install jupyter-kernel-gateway'."
            )
            raise

    async def astart(self) -> AgentBoxStatus:
        os.makedirs(".agentbox", exist_ok=True)
        self.session = aiohttp.ClientSession()
        await self._acheck_port()
        if settings.VERBOSE:
            print("Starting kernel...")
            out = None
        else:
            out = asyncio.subprocess.PIPE
        self._check_installed()
        python = Path(sys.executable).absolute()
        try:
            self.jupyter = await asyncio.create_subprocess_exec(
                python,
                "-m",
                "jupyter",
                "kernelgateway",
                "--KernelGatewayApp.ip='0.0.0.0'",
                f"--KernelGatewayApp.port={self.port}",
                stdout=out,
                stderr=out,
                cwd=".agentbox",
            )
        except Exception as e:
            print(e)
            raise ModuleNotFoundError(
                "Jupyter Kernel Gateway not found, please install it with:\n"
                "`pip install jupyter_kernel_gateway`\n"
                "to use the TinyBox."
            )
        while True:
            try:
                response = await self.session.get(self.kernel_url)
                if response.status == 200:
                    break
            except aiohttp.ClientConnectorError:
                pass
            except aiohttp.ServerDisconnectedError:
                pass
            if settings.VERBOSE:
                print("Waiting for kernel to start...")
            await asyncio.sleep(1)

        response = await self.session.post(
            f"{self.kernel_url}/kernels", headers={"Content-Type": "application/json"}
        )
        self.kernel_id = (await response.json())["id"]
        if self.kernel_id is None:
            raise Exception("Could not start kernel")
        self.ws = await ws_connect(f"{self.ws_url}/kernels/{self.kernel_id}/channels")

        return AgentBoxStatus(status="started")

    async def _acheck_port(self) -> None:
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            response = await self.session.get(f"http://localhost:{self.port}")
        except aiohttp.ClientConnectorError:
            pass
        except aiohttp.ServerDisconnectedError:
            pass
        else:
            if response.status == 200:
                self.port += 1
                await self._acheck_port()

    def status(self) -> AgentBoxStatus:
        return AgentBoxStatus(
            status="running"
            if self.kernel_id
            and requests.get(self.kernel_url, timeout=90).status_code == 200
            else "stopped"
        )

    async def astatus(self) -> AgentBoxStatus:
        return AgentBoxStatus(
            status="running"
            if self.kernel_id
            and self.session
            and (await self.session.get(self.kernel_url)).status == 200
            else "stopped"
        )

    def run(
        self,
        code: Optional[str] = None,
        file_path: Optional[os.PathLike] = None,
        retry=3,
    ) -> AgentBoxOutput:
        if not code and not file_path:
            raise ValueError("Code or file_path must be specified!")

        if code and file_path:
            raise ValueError("Can only specify code or the file to read_from!")

        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

        # run code in jupyter kernel
        if retry <= 0:
            raise RuntimeError("Could not connect to kernel")
        if not self.ws:
            self.start()
            if not self.ws:
                raise RuntimeError("Could not connect to kernel")
            # Message to send to kernel
        message = {
            "header": {
                "msg_id": (msg_id := uuid4().hex),
                "msg_type": "execute_request",
            },
            "parent_header": {},
            "metadata": {},
            "content": {
                "code": code,
                "silent": False,
                "store_history": True,
                "user_expressions": {},
                "allow_stdin": False,
                "stop_on_error": True,
            },
            "channel": "shell",
            "buffers": [],
        }

        # Put the message into the queue
        self.message_queue.put(message)

        if settings.VERBOSE:
            print("Running code:\n", code)

        # send code to kernel
        self.ws.send(json.dumps(self.message_queue.get()))

        result = ""
        while True:
            try:
                if isinstance(self.ws, WebSocketClientProtocol):
                    raise RuntimeError("Mixing asyncio and sync code is not supported")
                received_msg = json.loads(self.ws.recv())
            except ConnectionClosedError:
                self.start()
                return self.run(code, file_path, retry - 1)

            if (
                received_msg["header"]["msg_type"] == "stream"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                msg = received_msg["content"]["text"].strip()
                if "Requirement already satisfied:" in msg:
                    continue
                result += msg + "\n"
                if settings.VERBOSE:
                    print("Output:\n", result)

            elif (
                received_msg["header"]["msg_type"] == "execute_result"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                result += received_msg["content"]["data"]["text/plain"].strip() + "\n"
                if settings.VERBOSE:
                    print("Output:\n", result)

            elif received_msg["header"]["msg_type"] == "display_data":
                if "image/png" in received_msg["content"]["data"]:
                    return AgentBoxOutput(
                        type="image/png",
                        content=received_msg["content"]["data"]["image/png"],
                    )
                if "text/plain" in received_msg["content"]["data"]:
                    return AgentBoxOutput(
                        type="text",
                        content=received_msg["content"]["data"]["text/plain"],
                    )
                return AgentBoxOutput(
                    type="error",
                    content="Could not parse output",
                )
            elif (
                received_msg["header"]["msg_type"] == "status"
                and received_msg["parent_header"]["msg_id"] == msg_id
                and received_msg["content"]["execution_state"] == "idle"
            ):
                if len(result) > 500:
                    result = "[...]\n" + result[-500:]
                return AgentBoxOutput(
                    type="text", content=result or "code run successfully (no output)"
                )

            elif (
                received_msg["header"]["msg_type"] == "error"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                error = (
                    f"{received_msg['content']['ename']}: "
                    f"{received_msg['content']['evalue']}"
                )
                if settings.VERBOSE:
                    print("Error:\n", error)
                return AgentBoxOutput(type="error", content=error)

    async def arun(
        self,
        code: str,
        file_path: Optional[os.PathLike] = None,
        retry=3,
    ) -> AgentBoxOutput:
        if file_path:
            raise NotImplementedError(
                "Reading from file is not supported in async mode"
            )

        # run code in jupyter kernel
        if retry <= 0:
            raise RuntimeError("Could not connect to kernel")
        if not self.ws:
            await self.astart()
            if not self.ws:
                raise RuntimeError("Could not connect to kernel")
        # Message to send to kernel
        message = {
            "header": {
                "msg_id": (msg_id := uuid4().hex),
                "msg_type": "execute_request",
            },
            "parent_header": {},
            "metadata": {},
            "content": {
                "code": code,
                "silent": False,
                "store_history": True,
                "user_expressions": {},
                "allow_stdin": False,
                "stop_on_error": True,
            },
            "channel": "shell",
            "buffers": [],
        }

        # Put the message into the queue
        self.message_queue.put(message)

        if settings.VERBOSE:
            print("Running code:\n", code)


        if not isinstance(self.ws, WebSocketClientProtocol):
            raise RuntimeError("Mixing asyncio and sync code is not supported")
        
        await self.ws.send(json.dumps(self.message_queue.get()))
        result = ""
        while True:
            try:
                received_msg = json.loads(await self.ws.recv())
            except ConnectionClosedError:
                await self.astart()
                return await self.arun(code, file_path, retry - 1)

            if (
                received_msg["header"]["msg_type"] == "stream"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                msg = received_msg["content"]["text"].strip()
                if "Requirement already satisfied:" in msg:
                    continue
                result += msg + "\n"
                if settings.VERBOSE:
                    print("Output:\n", result)

            elif (
                received_msg["header"]["msg_type"] == "execute_result"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                result += received_msg["content"]["data"]["text/plain"].strip() + "\n"
                if settings.VERBOSE:
                    print("Output:\n", result)

            elif received_msg["header"]["msg_type"] == "display_data":
                if "image/png" in received_msg["content"]["data"]:
                    return AgentBoxOutput(
                        type="image/png",
                        content=received_msg["content"]["data"]["image/png"],
                    )
                if "text/plain" in received_msg["content"]["data"]:
                    return AgentBoxOutput(
                        type="text",
                        content=received_msg["content"]["data"]["text/plain"],
                    )
            elif (
                received_msg["header"]["msg_type"] == "status"
                and received_msg["parent_header"]["msg_id"] == msg_id
                and received_msg["content"]["execution_state"] == "idle"
            ):
                if len(result) > 500:
                    result = "[...]\n" + result[-500:]
                return AgentBoxOutput(
                    type="text", content=result or "code run successfully (no output)"
                )

            elif (
                received_msg["header"]["msg_type"] == "error"
                and received_msg["parent_header"]["msg_id"] == msg_id
            ):
                error = (
                    f"{received_msg['content']['ename']}: "
                    f"{received_msg['content']['evalue']}"
                )
                if settings.VERBOSE:
                    print("Error:\n", error)
                return AgentBoxOutput(type="error", content=error)

    def upload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        os.makedirs(".agentbox", exist_ok=True)
        with open(os.path.join(".agentbox", file_name), "wb") as f:
            f.write(content)

        return AgentBoxStatus(status=f"{file_name} uploaded successfully")

    async def aupload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        return await asyncio.to_thread(self.upload, file_name, content)

    def download(self, file_name: str) -> AgentBoxFile:
        with open(os.path.join(".agentbox", file_name), "rb") as f:
            content = f.read()

        return AgentBoxFile(name=file_name, content=content)

    async def adownload(self, file_name: str) -> AgentBoxFile:
        return await asyncio.to_thread(self.download, file_name)

    def install(self, package_name: str) -> AgentBoxStatus:
        self.run(f"!pip install -q {package_name}")
        
        return AgentBoxStatus(status=f"{package_name} installed successfully")

    async def ainstall(self, package_name: str) -> AgentBoxStatus:
        await self.arun(f"!pip install -q {package_name}")
        
        return AgentBoxStatus(status=f"{package_name} installed successfully")

    def list_files(self) -> List[AgentBoxFile]:
        return [
            AgentBoxFile(name=file_name, content=None)
            for file_name in os.listdir(".agentbox")
        ]

    async def alist_files(self) -> List[AgentBoxFile]:
        return await asyncio.to_thread(self.list_files)

    def restart(self) -> AgentBoxStatus:
        if self.jupyter is not None:
            self.stop()
        else:
            self.start()
        return AgentBoxStatus(status="restarted")

    async def arestart(self) -> AgentBoxStatus:
        if self.jupyter is not None:
            await self.astop()
        else:
            await self.astart()
        return AgentBoxStatus(status="restarted")

    def stop(self) -> AgentBoxStatus:
        self.message_queue.put("STOP")
        self.message_thread.join()
        if self.ws is not None:
            try:
                self.ws.close()
            except ConnectionClosedError:
                pass
            self.ws = None

        if self.jupyter is not None:
            self.jupyter.terminate()
            self.jupyter.wait()
            self.jupyter = None
            time.sleep(2)

        return AgentBoxStatus(status="stopped")

    async def astop(self) -> AgentBoxStatus:
        self.message_queue.put("STOP")
        self.message_thread.join()  
        if self.ws is not None:
            try:
                if not isinstance(self.ws, WebSocketClientProtocol):
                    raise RuntimeError("Mixing asyncio and sync code is not supported")
                await self.ws.close()
            except ConnectionClosedError:
                pass
            self.ws = None

        if self.jupyter is not None:
            self.jupyter.terminate()
            self.jupyter = None
            await asyncio.sleep(2)

        if self.session is not None:
            await self.session.close()
            self.session = None

        return AgentBoxStatus(status="stopped")

    @property
    def kernel_url(self) -> str:
        """Return the url of the kernel."""
        return f"http://localhost:{self.port}/api"

    @property
    def ws_url(self) -> str:
        """Return the url of the websocket."""
        return f"ws://localhost:{self.port}/api"
