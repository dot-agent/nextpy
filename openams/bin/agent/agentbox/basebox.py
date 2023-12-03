""" Abstract Base Class for Isolated Execution Environments (AgentBox's) """

from abc import ABC, abstractmethod
from datetime import datetime
from os import PathLike
from queue import Queue
import threading
from typing import List, Optional
from uuid import UUID
from openams.schema import AgentBoxFile, AgentBoxOutput, AgentBoxStatus


class BaseBox(ABC):
    """AgentBox Abstract Base Class"""

    def __init__(self, session_id: Optional[UUID] = None) -> None:
        """Initialize the AgentBox instance"""
        self.session_id = session_id
        self.last_interaction = datetime.now()
        self.message_queue = Queue()
        self.message_thread = threading.Thread(target=self._message_handler)
        self.message_thread.start()

    def _update(self) -> None:
        """Update last interaction time"""
        self.last_interaction = datetime.now()

    @abstractmethod
    def start(self) -> AgentBoxStatus:
        """Startup the AgentBox instance"""

    @abstractmethod
    async def astart(self) -> AgentBoxStatus:
        """Async Startup the AgentBox instance"""
    
    @abstractmethod
    def _message_handler(self):
        """Abstract method for handling messages from the queue."""
        pass

    @abstractmethod
    def _send_message_to_kernel(self, message):
        """Abstract method for sending a message to the kernel."""
        pass

    @abstractmethod
    def status(self) -> AgentBoxStatus:
        """Get the current status of the AgentBox instance"""

    @abstractmethod
    async def astatus(self) -> AgentBoxStatus:
        """Async Get the current status of the AgentBox instance"""

    @abstractmethod
    def run(
        self, code: Optional[str] = None, file_path: Optional[PathLike] = None
    ) -> AgentBoxOutput:
        """Execute python code inside the AgentBox instance"""

    @abstractmethod
    async def arun(
        self, code: str, file_path: Optional[PathLike] = None
    ) -> AgentBoxOutput:
        """Async Execute python code inside the AgentBox instance"""

    @abstractmethod
    def upload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        """Upload a file as bytes to the AgentBox instance"""

    @abstractmethod
    async def aupload(self, file_name: str, content: bytes) -> AgentBoxStatus:
        """Async Upload a file as bytes to the AgentBox instance"""

    @abstractmethod
    def download(self, file_name: str) -> AgentBoxFile:
        """Download a file as AgentBoxFile schema"""

    @abstractmethod
    async def adownload(self, file_name: str) -> AgentBoxFile:
        """Async Download a file as AgentBoxFile schema"""

    @abstractmethod
    def install(self, package_name: str) -> AgentBoxStatus:
        """Install a python package to the venv"""

    @abstractmethod
    async def ainstall(self, package_name: str) -> AgentBoxStatus:
        """Async Install a python package to the venv"""

    @abstractmethod
    def list_files(self) -> List[AgentBoxFile]:
        """List all available files inside the AgentBox instance"""

    @abstractmethod
    async def alist_files(self) -> List[AgentBoxFile]:
        """Async List all available files inside the AgentBox instance"""

    @abstractmethod
    def restart(self) -> AgentBoxStatus:
        """Restart the jupyter kernel inside the AgentBox instance"""

    @abstractmethod
    async def arestart(self) -> AgentBoxStatus:
        """Async Restart the jupyter kernel inside the AgentBox instance"""

    @abstractmethod
    def stop(self) -> AgentBoxStatus:
        """Terminate the AgentBox instance"""
        self.message_queue.put("STOP")
        self.message_thread.join()
        return self._stop()
    
    @abstractmethod
    def _stop(self) -> AgentBoxStatus:
        """Abstract method for stopping the AgentBox instance"""
        pass

    @abstractmethod
    async def astop(self) -> AgentBoxStatus:
        """Async Terminate the AgentBox instance"""
        # Stop the message handling thread
        self.message_queue.put("STOP")
        await self.message_thread.join() 
        return await self._astop()

    @abstractmethod
    async def _astop(self) -> AgentBoxStatus:
        """Abstract method for asynchronously stopping the AgentBox instance"""
        pass

    def __enter__(self) -> "BaseBox":
        self.start()
        return self

    async def __aenter__(self) -> "BaseBox":
        await self.astart()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.astop()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.session_id}>"

    def __str__(self) -> str:
        return self.__repr__()
