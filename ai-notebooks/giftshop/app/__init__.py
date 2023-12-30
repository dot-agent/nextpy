# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from flask import Flask

app = Flask(__name__)

import logging

from app import views

# Set up a specific logger with our desired output level
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger. Here, we define the logging format and add it to a StreamHandler,
# which simply logs the output to the console.
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
