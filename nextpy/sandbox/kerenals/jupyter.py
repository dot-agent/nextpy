# based on https://github.com/MrGreyfun/Local-Code-Interpreter/blob/main/src/jupyter_backend.py
import jupyter_client
import re

def delete_color_control_char(string):
    """
    Remove ANSI escape sequences from a string.

    ANSI escape sequences are used to control color and formatting in terminal outputs. 
    This function strips those sequences to return the plain text.

    Parameters:
    string (str): The string from which ANSI escape sequences will be removed.

    Returns:
    str: The cleaned string with no ANSI escape sequences.
    """
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', string)


class JupyterKernel:
    """
    A class for managing and interacting with a Jupyter notebook kernel.

    This class provides functionality to start a new Jupyter kernel, execute code within it,
    and retrieve the output. It is designed to work with Python code executions.

    Attributes:
    kernel_manager: Manager for the Jupyter kernel.
    kernel_client: Client for interacting with the Jupyter kernel.
    work_dir (str): The working directory for the kernel's operations.
    available_functions (dict): A mapping of available functions for code execution.
    """
    def __init__(self, work_dir):
        """
        Initialize the JupyterKernel with a specified working directory.

        Parameters:
        work_dir (str): The working directory to be set for the Jupyter kernel.
        """
    
        self.kernel_manager, self.kernel_client = jupyter_client.manager.start_new_kernel(kernel_name='python3')
        self.work_dir = work_dir
        self._create_work_dir()
        self.available_functions = {
            'execute_code': self.execute_code,
            'python': self.execute_code
        }

    def execute_code_(self, code):
        """
        Execute a given piece of code in the Jupyter kernel and collect outputs.

        This method executes code and captures different types of outputs like stdout, 
        execution results, and errors. It handles plain text, HTML, PNG, and JPEG outputs.

        Parameters:
        code (str): The Python code to be executed in the kernel.

        Returns:
        list: A list of tuples representing different types of outputs from the code execution.
        """
        msg_id = self.kernel_client.execute(code)

        # Get the output of the code
        iopub_msg = self.kernel_client.get_iopub_msg()

        all_output = []
        while True:
            if iopub_msg['msg_type'] == 'stream':
                if iopub_msg['content'].get('name') == 'stdout':
                    output = iopub_msg['content']['text']
                    all_output.append(('stdout', output))
                iopub_msg = self.kernel_client.get_iopub_msg()
            elif iopub_msg['msg_type'] == 'execute_result':
                if 'data' in iopub_msg['content']:
                    if 'text/plain' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['text/plain']
                        all_output.append(('execute_result_text', output))
                    if 'text/html' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['text/html']
                        all_output.append(('execute_result_html', output))
                    if 'image/png' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['image/png']
                        all_output.append(('execute_result_png', output))
                    if 'image/jpeg' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['image/jpeg']
                        all_output.append(('execute_result_jpeg', output))
                iopub_msg = self.kernel_client.get_iopub_msg()
            elif iopub_msg['msg_type'] == 'display_data':
                if 'data' in iopub_msg['content']:
                    if 'text/plain' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['text/plain']
                        all_output.append(('display_text', output))
                    if 'text/html' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['text/html']
                        all_output.append(('display_html', output))
                    if 'image/png' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['image/png']
                        all_output.append(('display_png', output))
                    if 'image/jpeg' in iopub_msg['content']['data']:
                        output = iopub_msg['content']['data']['image/jpeg']
                        all_output.append(('display_jpeg', output))
                iopub_msg = self.kernel_client.get_iopub_msg()
            elif iopub_msg['msg_type'] == 'error':
                if 'traceback' in iopub_msg['content']:
                    output = '\n'.join(iopub_msg['content']['traceback'])
                    all_output.append(('error', output))
                iopub_msg = self.kernel_client.get_iopub_msg()
            elif iopub_msg['msg_type'] == 'status' and iopub_msg['content'].get('execution_state') == 'idle':
                break
            else:
                iopub_msg = self.kernel_client.get_iopub_msg()

        return all_output

    def execute_code(self, code):
        """
        Execute code in the Jupyter kernel and return a simplified text representation.

        This method is the public interface for executing code. It processes the outputs 
        from `execute_code_` and returns a text representation along with detailed content.

        Parameters:
        code (str): The Python code to be executed in the kernel.

        Returns:
        tuple: A tuple containing a string of concatenated text outputs and the detailed content list.
        """
        execution_output_text = []
        content_to_display = self.execute_code_(code)
        for mark, out_str in content_to_display:
            if mark in ('stdout', 'execute_result_text', 'display_text'):
                execution_output_text.append(out_str)
            elif mark in ('execute_result_png', 'execute_result_jpeg', 'display_png', 'display_jpeg'):
                execution_output_text.append('[image]')
            elif mark == 'error':
                execution_output_text.append(delete_color_control_char(out_str))

        return '\n'.join(execution_output_text), content_to_display

    def _create_work_dir(self):
        """
        Create and set the working directory in the Jupyter environment.

        This private method is used to initialize the working directory for the kernel.
        """
        init_code = f"import os\n" \
                    f"if not os.path.exists('{self.work_dir}'):\n" \
                    f"    os.mkdir('{self.work_dir}')\n" \
                    f"os.chdir('{self.work_dir}')\n" \
                    f"del os"
        self.execute_code_(init_code)

    def restart_jupyter_kernel(self):
        """
        Restart the Jupyter kernel.

        This method shuts down the current kernel and starts a new one, resetting the working directory.
        """
        self.kernel_client.shutdown()
        self.kernel_manager, self.kernel_client = jupyter_client.manager.start_new_kernel(kernel_name='python3')
        self._create_work_dir()
