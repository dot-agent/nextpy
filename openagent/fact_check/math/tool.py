import sys
import io
import yaml
import pdb

class python_executor:
    def __init__(self):
        pass

    def run_single(self, program):
        buffer = io.StringIO() # Create an in-memory buffer for the output
        stdout = sys.stdout # Save the original standard output
        sys.stdout = buffer # Redirect the standard output to the buffer
        try:
            exec(program)
        except Exception as e:
            # Handle the error here
            error_message = str(e)
            sys.stdout = stdout  # Restore the original standard output
            return error_message

        exec(program)
        sys.stdout = stdout # Restore the original standard output
        output = buffer.getvalue() # Get the output from the buffer
        return output

    def run(self, snippet):
        if snippet == None:
            return None
        exec_result = self.run_single(snippet)
        if exec_result and 'False' in exec_result:
            exec_result = 'False'
        else:
            exec_result = 'True'
        return exec_result