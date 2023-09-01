import click
from pathlib import Path
import logging
from openagent.gui.cli import run_gui  # Ensure this import is correct

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@click.group()
def cli():
    pass

@click.command()
@click.option('--gui', is_flag=True, help='Run the GUI code.')
@click.argument('filename', type=Path)
def run(gui, filename):
    try:
        logging.info(f"Running command with GUI flag: {gui} and filename: {filename}")
        
        if gui:
            logging.info(f"Running GUI with file {filename}")
            run_gui(filename)  # Ensure this function is implemented
            logging.info("GUI run completed.")
            print("GUI run completed.")  # Feedback to user
        else:
            logging.info(f"Running {filename} without GUI")
            print(f"Running {filename} without GUI")
            # TODO: Add the code that runs the script without the GUI
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")  # Feedback to user

cli.add_command(run)

if __name__ == '__main__':
    logging.info("Starting CLI.")
    cli()
    logging.info("CLI execution completed.")