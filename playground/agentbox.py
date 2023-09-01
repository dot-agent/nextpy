import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)
import openagent
from openagent.llms._openai import OpenAI as guidance_llm
from openagent.agent.chat import ChatAgent
from dotenv import load_dotenv
load_dotenv()

from jupyter_client import KernelManager
from IPython import display
import subprocess
import ast
import argparse
import threading


def agent():

    llm = guidance_llm(
        model="gpt-3.5-turbo"
    )

    chat_template = '''
                {{#user~}}
                I want to translate the following English text into Python code:
                QUERY: {{input}}
                {{~/user}}

                {{#assistant~}}
                Sure, I can assist with that. If I need more information, I'll ask for clarification.
                {{~/assistant}}

                {{#user~}}
                Yes, go ahead and write the complete code.
                {{~/user}}

                {{#assistant~}}
                {{gen 'response' temperature=0 max_tokens=3900}}
                {{~/assistant}}

                {{#assistant~}}
                If the context or the task is not clear, please provide additional information to clarify.
                {{~/assistant}}'''
    
    agent = ChatAgent(
        llm=llm,
        prompt_template=chat_template,
    )
    return agent


def install_dependencies(code):
    try:
        # Parse the code to extract import statements
        parsed_ast = ast.parse(code)
        imports = []

        for node in ast.walk(parsed_ast):
            if isinstance(node, ast.Import):
                imports.extend([name.name for name in node.names])
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name is not None:
                    imports.append(module_name)

        # Remove duplicate imports and filter out standard library modules
        imports = list(set(imports))
        # print("imports", imports)

        resolved_imports = set()
        for imp in imports:
            if '.' in imp:
                parent_module = imp.split('.')[0]
                resolved_imports.add(parent_module)
            else:
                resolved_imports.add(imp)
        
        # Remove duplicate imports and filter out standard library modules
        resolved_imports = list(resolved_imports)
        # print("resolved_imports", resolved_imports)

        third_party_dependencies = [dep for dep in resolved_imports if dep not in sys.modules]
        # print("third_party_dependencies", third_party_dependencies)

        if third_party_dependencies:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + third_party_dependencies)
            return True
        else:
            # print("No third-party dependencies detected.")
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
    timeout_seconds = 10
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
def main(gpt_prompt):
    res = agent().run(input=gpt_prompt)
    code = f"""{res.split('```')[1].replace('python', '')}"""
    print(code)

    # Install dependencies
    if install_dependencies(code):
        # Run the generated code in the Jupyter kernel
        run_python_code_in_kernel(code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Python code from the command line.')
    parser.add_argument("--gpt_prompt", help="Python code to be executed", default=None)
    args = parser.parse_args()
    gpt_prompt = args.gpt_prompt

    main(gpt_prompt)
