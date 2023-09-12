# AgentBox

AgentBox is not just a tool but a carefully crafted environment providing an interface to interact with a remote execution environment, optimized specifically for AI agents. It supports both synchronous and asynchronous operations, and allows users to perform a multitude of tasks such as checking the status, running code, managing Python packages, and handling file operations.

## Design Philosophy

AgentBox's philosophy is built on two foundational pillars:

### Nature vs. Nurture

Within AgentBox, the computing environment is more than infrastructure. It's a cradle where AI agents are nurtured. We believe the composition and architecture of this environment are integral to what the agents will become.

### The Watchful Companions with Continuous Reactivity

Agents are far from static tools waiting for instructions, they are ever-alert companions, processing a rich tapestry of information, such as emails and web findings, even during your downtime. Unlike conventional AI confined to prompt-response interactions, AgentBox is designed to enable agents to engage in a continuous, harmonious interaction with the digital world.

## v0.01 Features

- **Synchronous and Asynchronous Operations**: Seamlessly switch between real-time and delayed tasks.
- **Code Execution**: Run and manage code within the environment.
- **Python Package Management**: Install and handle Python packages effortlessly.
- **File Management**: Easy uploading, downloading, and listing of files.


# AgentBox Usage

## Methods Overview

- **Status**: `status()` / `astatus()`
  - Checks the status of the AgentBox.
- **Run Code**: `run(code)` / `arun(code)`
  - Executes the given code within the AgentBox.
- **Install Package**: `install(package_name)` / `ainstall(package_name)`
  - Installs a Python package in the AgentBox.
- **Upload File**: `upload(filename, content)` / `aupload(filename, content)`
  - Uploads a file with the given content to the AgentBox.
- **List Files**: `list_files()` / `alist_files()`
  - Lists the files present in the AgentBox.
- **Download File**: `download(filename)` / `adownload(filename)`
  - Downloads a file from the AgentBox.

**Note**: The methods with an "a" prefix are asynchronous versions of the corresponding synchronous methods.

## Example Usage

### Synchronous Example

```python
from agentboxapi import AgentBox

with AgentBox() as agentbox:
    agentbox.status()
    agentbox.run(code="print('Hello World!')")
    agentbox.install("python-package")
    agentbox.upload("test.txt", b"Hello World!")
    agentbox.list_files()
    agentbox.download("test.txt")
```

### Asynchronous Example

```python
from agentboxapi import AgentBox

async with AgentBox() as agentbox:
    await agentbox.astatus()
    await agentbox.arun(code="print('Hello World!')")
    await agentbox.ainstall("python-package")
    await agentbox.aupload("test.txt", b"Hello World!")
    await agentbox.alist_files()
    await agentbox.adownload("test.txt")
```
