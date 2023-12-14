import pytest
import os
from nextpy.sandbox.sandbox import SandBox

def test_start_and_stop():
    box = SandBox()
    assert box.start() == "Jupyter Kernel started."
    assert box.stop() == "SandBox stopped."

def test_run_code():
    box = SandBox()
    box.start()
    assert box.run_code("print('Hello, World!')").strip() == "Hello, World!"
    box.stop()

def test_install_package():
    box = SandBox()
    # Replace 'example-package' with a real package for testing
    response = box.install_package('example-package')
    assert 'Successfully installed' in response or 'Requirement already satisfied' in response

def test_file_upload_and_download():
    box = SandBox()
    test_content = b"Test file content"
    test_filename = "testfile.txt"

    upload_response = box.upload_file(test_filename, test_content)
    assert upload_response == f"{test_filename} uploaded."

    downloaded_content = box.download_file(test_filename)
    assert downloaded_content == test_content

    # Clean up
    if os.path.exists(test_filename):
        os.remove(test_filename)

