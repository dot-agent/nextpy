import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from jupyter_client import KernelManager
from IPython import display
import subprocess
import ast
import time
import argparse
import textwrap
import threading




def install_dependencies(code):
    try:
        # Parse the code to extract import statements
        parsed_ast = ast.parse(code)
        imports = [node.names[0].name.split('.')[0] for node in ast.walk(parsed_ast) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
        
        # print(imports)
        if imports:
            subprocess.check_call(["pip", "install"] + imports)
            return True
        else:
            print("No dependencies detected.")
            return True
    except subprocess.CalledProcessError:
        print("Dependency installation failed.")
        return False


def run_python_code_in_kernel(code):
    # Create a kernel manager
    km = KernelManager(kernel_name='python3')  # Use the appropriate kernel name

    # Start the kernel
    km.start_kernel()

    # Connect to the kernel
    kc = km.client()
    kc.start_channels()

    # Execute the code in the kernel
    kc.execute(code)
    
    # print(kc)
    start_time = time.time()
    print("start_time ", start_time)

    # Create a thread for waiting on messages
    def wait_for_messages():
        try:
            while True:
                msg = kc.get_iopub_msg()
                msg_type = msg['header']['msg_type']
                if msg_type == 'display_data':
                    output_data = msg['content']['data']
                    if 'image/png' in output_data:
                        display.display_png(output_data['image/png'], raw=True)
                    elif 'image/jpeg' in output_data:
                        display.display_jpeg(output_data['image/png'], raw=True)
                elif msg_type == 'stream':
                    output_data = msg['content']['text']
                    output_data = output_data.split("\n")
                    for output in output_data[:-1]:
                        display.display(output)
        except asyncio.CancelledError:
            pass  # Ignore the exception
    
    # Start the message-waiting thread
    message_thread = threading.Thread(target=wait_for_messages)
    message_thread.start()

    # Wait for the specified timeout
    timeout_seconds = 5
    message_thread.join(timeout_seconds)

    # Check if the thread is still alive (indicating timeout)
    if message_thread.is_alive():
        print("Code execution completed")
    else:
        print("Code execution completed within the timeout.")

    # Stop the kernel
    kc.stop_channels()
    km.shutdown_kernel()

# Main function
def main(code):
#     code = """
# print("Below is graph is very useful")
# import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4, 6, 12])
# plt.show()
# """

    # code = """
    #         def fibonacci(n):
    #             if n <= 0:
    #                 return 'Invalid input. Please enter a positive integer.'
    #             elif n == 1:
    #                 return 0
    #             elif n == 2:
    #                 return 1
    #             else:
    #                 fib_sequence = [0, 1]
    #                 for i in range(2, n):
    #                     fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    #                 return fib_sequence
    #         fibonacci_20 = fibonacci(20)
    #         print(fibonacci_20)
    #     """

    # code = textwrap.dedent(code)

    # Install dependencies
    if install_dependencies(code):
        # Run the generated code in the Jupyter kernel
        run_python_code_in_kernel(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Python code from the command line.')
    parser.add_argument("--code", help="Python code to be executed", default=None)
    args = parser.parse_args()
    code = args.code

    main(code)
