from os import PathLike
from typing import Any, Dict, List, Optional
from uuid import UUID

from aiohttp import ClientSession

from nextpy.ai.agent.agentbox._utils import abase_request, base_request
from nextpy.ai.agent.agentbox.basebox import BaseBox
from nextpy.ai.config import settings
from nextpy.ai.schema import AgentBoxFile, AgentBoxOutput, AgentBoxStatus


class AgentBox(BaseBox):
    """Agentboxed Python Interpreter."""

    def __new__(cls, *args, **kwargs):
        if (
            kwargs.pop("local", False)
            or settings.AGENTBOX_API_KEY is None
            or settings.AGENTBOX_API_KEY == "local"
        ):
            from .tinybox import TinyBox

            return TinyBox(*args, **kwargs)

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session_id: Optional[UUID] = kwargs.get("id", None)
        self.aiohttp_session: Optional[ClientSession] = None

    def agentbox_request(self, method, endpoint, *args, **kwargs) -> Dict[str, Any]:
        """Basic request to the AgentBox API."""
        self._update()
        return base_request(
            method, f"/agentbox/{self.session_id}" + endpoint, *args, **kwargs
        )

    async def aagentbox_request(
        self, method, endpoint, *args, **kwargs
    ) -> Dict[str, Any]:
        """Basic async request to the AgentBox API."""
        self._update()
        if self.aiohttp_session is None:
            raise RuntimeError("AgentBox session not started")
        return await abase_request(
            self.aiohttp_session,
            method,
            f"/agentbox/{self.session_id}" + endpoint,
            *args,
            **kwargs,
        )

    def start(self) -> AgentBoxStatus:
        self.session_id = base_request(
            method="GET",
            endpoint="/agentbox/start",
        )["id"]
        return AgentBoxStatus(status="started")

    async def astart(self) -> AgentBoxStatus:
        self.aiohttp_session = ClientSession()
        self.session_id = (
            await abase_request(
                self.aiohttp_session,
                method="GET",
                endpoint="/agentbox/start",
            )
        )["id"]
        return AgentBoxStatus(status="started")

    def status(self):
        return AgentBoxStatus(
            **self.agentbox_request(
                method="GET",
                endpoint="/",
            )
        )

    async def astatus(self):
        return AgentBoxStatus(
            **await self.aagentbox_request(
                method="GET",
                endpoint="/",
            )
        )

    def run(
        self, code: Optional[str] = None, file_path: Optional[PathLike] = None
    ) -> AgentBoxOutput:
        if not code and not file_path:  # R0801
            raise ValueError("Code or file_path must be specified!")

        if code and file_path:
            raise ValueError("Can only specify code or the file to read_from!")

        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

        return AgentBoxOutput(
            **self.agentbox_request(
                method="POST",
                endpoint="/run",
                body={"code": code},
            )
        )

    async def arun(
        self, code: str, file_path: Optional[PathLike] = None
    ) -> AgentBoxOutput:
        if file_path:  # TODO: Implement this
            raise NotImplementedError(
                "Reading from FilePath is not supported in async mode yet!"
            )

        return AgentBoxOutput(
            **await self.aagentbox_request(
                method="POST",
                endpoint="/run",
                body={"code": code},
            )
        )

    def upload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        return AgentBoxStatus(
            **self.agentbox_request(
                method="POST",
                endpoint="/upload",
                files={"file": (file_name, content)},
            )
        )

    async def aupload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        return AgentBoxStatus(
            **await self.aagentbox_request(
                method="POST",
                endpoint="/upload",
                files={"file": (file_name, content)},
            )
        )

    def download(self, file_name: str) -> AgentBoxFile:
        return AgentBoxFile(
            **self.agentbox_request(
                method="GET",
                endpoint="/download",
                body={"file_name": file_name},
            )
        )

    async def adownload(self, file_name: str) -> AgentBoxFile:
        return AgentBoxFile(
            **await self.aagentbox_request(
                method="GET",
                endpoint="/download",
                body={"file_name": file_name},
            )
        )

    def install(self, package_name: str) -> AgentBoxStatus:
        return AgentBoxStatus(
            **self.agentbox_request(
                method="POST",
                endpoint="/install",
                body={
                    "package_name": package_name,
                },
            )
        )

    async def ainstall(self, package_name: str) -> AgentBoxStatus:
        return AgentBoxStatus(
            **await self.aagentbox_request(
                method="POST",
                endpoint="/install",
                body={
                    "package_name": package_name,
                },
            )
        )

    def list_files(self) -> List[AgentBoxFile]:
        return [
            AgentBoxFile(name=file_name, content=None)
            for file_name in (
                self.agentbox_request(
                    method="GET",
                    endpoint="/files",
                )
            )["files"]
        ]

    async def alist_files(self) -> List[AgentBoxFile]:
        return [
            AgentBoxFile(name=file_name, content=None)
            for file_name in (
                await self.aagentbox_request(
                    method="GET",
                    endpoint="/files",
                )
            )["files"]
        ]

    def restart(self) -> AgentBoxStatus:
        return AgentBoxStatus(
            **self.agentbox_request(
                method="POST",
                endpoint="/restart",
            )
        )

    async def arestart(self) -> AgentBoxStatus:
        return AgentBoxStatus(
            **await self.aagentbox_request(
                method="POST",
                endpoint="/restart",
            )
        )

    def stop(self) -> AgentBoxStatus:
        return AgentBoxStatus(
            **self.agentbox_request(
                method="POST",
                endpoint="/stop",
            )
        )

    async def astop(self) -> AgentBoxStatus:
        status = AgentBoxStatus(
            **await self.aagentbox_request(
                method="POST",
                endpoint="/stop",
            )
        )
        if self.aiohttp_session:
            await self.aiohttp_session.close()
            self.aiohttp_session = None
        return status
