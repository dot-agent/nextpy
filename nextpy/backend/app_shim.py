# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Shims the real nextpy app module for running backend server (uvicorn or gunicorn).
Only the app attribute is explicitly exposed.
"""
from nextpy import constants
from nextpy.build.prerequisites import get_compiled_app

if "app" != constants.CompileVars.APP:
    raise AssertionError("unexpected variable name for 'app'")
app = getattr(get_compiled_app(), constants.CompileVars.APP)

# ensure only "app" is exposed.
del get_compiled_app
del constants
