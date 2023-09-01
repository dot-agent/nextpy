import asyncio
import os
import sys

import click
import nest_asyncio
import uvicorn

nest_asyncio.apply()

from openagent.gui.cache import init_lc_cache
from openagent.gui.cli.auth import login, logout
from openagent.gui.cli.deploy import deploy
from openagent.gui.cli.utils import check_file
from openagent.gui.config import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    PACKAGE_ROOT,
    config,
    init_config,
    load_module,
)
from openagent.gui.db import init_local_db, migrate_local_db
from openagent.gui.logger import logger
from openagent.gui.markdown import init_markdown
from openagent.gui.server import app, max_message_size, register_wildcard_route_handler
from openagent.gui.telemetry import trace_event


# Create the main command group for Gui CLI
@click.group(context_settings={"auto_envvar_prefix": "openagent"})
@click.version_option(prog_name="openagent")
def cli():
    return


# Define the function to run Gui with provided options
def run_gui(target: str):
    host = os.environ.get("GUI_HOST", DEFAULT_HOST)
    port = int(os.environ.get("GUI_PORT", DEFAULT_PORT))
    config.run.host = host
    config.run.port = port

    check_file(target)
    # Load the module provided by the user
    config.run.module_name = target
    load_module(config.run.module_name)

    register_wildcard_route_handler()

    # Create the gui.md file if it doesn't exist
    init_markdown(config.root)

    # Initialize the LangChain cache if installed and enabled
    init_lc_cache()

    # Initialize the local database if configured to use it
    init_local_db()

    log_level = "debug" if config.run.debug else "error"

    # Start the server
    async def start():
        config = uvicorn.Config(
            app,
            host=host,    // "@types/testing-library__jest-dom": "^6.0.0",
            port=port,
            log_level=log_level,
            ws_max_size=max_message_size,
        )
        server = uvicorn.Server(config)
        await server.serve()

    # Run the asyncio event loop instead of uvloop to enable re entrance
    asyncio.run(start())
    # uvicorn.run(app, host=host, port=port, log_level=log_level)


# Define the "run" command for Gui CLI
@cli.command("run")
@click.argument("target", required=True, envvar="RUN_TARGET")
@click.option(
    "-w",
    "--watch",
    default=False,
    is_flag=True,
    envvar="WATCH",
    help="Reload the app when the module changes",
)
@click.option(
    "-h",
    "--headless",
    default=False,
    is_flag=True,
    envvar="HEADLESS",
    help="Will prevent to auto open the app in the browser",
)
@click.option(
    "-d",
    "--debug",
    default=False,
    is_flag=True,
    envvar="DEBUG",
    help="Set the log level to debug",
)
@click.option(
    "-c",
    "--ci",
    default=False,
    is_flag=True,
    envvar="CI",
    help="Flag to run in CI mode",
)
@click.option(
    "--no-cache",
    default=False,
    is_flag=True,
    envvar="NO_CACHE",
    help="Useful to disable third parties cache, such as langchain.",
)
@click.option(
    "--db",
    type=click.Choice(["cloud", "local"]),
    help="Useful to control database mode when running CI.",
)
@click.option("--host", help="Specify a different host to run the server on")
@click.option("--port", help="Specify a different port to run the server on")
def gui_run(target, watch, headless, debug, ci, no_cache, db, host, port):
    if host:
        os.environ["GUI_HOST"] = host
    if port:
        os.environ["GUI_PORT"] = port
    if ci:
        logger.info("Running in CI mode")

        if db:
            config.project.database = db

        config.project.enable_telemetry = False
        no_cache = True
        from openagent.gui.cli.mock import mock_openai

        mock_openai()

    else:
        trace_event("gui run")

    config.run.headless = headless
    config.run.debug = debug
    config.run.no_cache = no_cache
    config.run.ci = ci
    config.run.watch = watch

    run_gui(target)


@cli.command("deploy")
@click.argument("target", required=True, envvar="GUI_RUN_TARGET")
@click.argument("args", nargs=-1)
def gui_deploy(target, args=None, **kwargs):
    trace_event("gui deploy")
    raise NotImplementedError("Deploy is not yet implemented")
    deploy(target)


@cli.command("hello")
@click.argument("args", nargs=-1)
def gui_hello(args=None, **kwargs):
    trace_event("gui hello")
    hello_path = os.path.join(PACKAGE_ROOT, "hello.py")
    run_gui(hello_path)


@cli.command("login")
@click.argument("args", nargs=-1)
def gui_login(args=None, **kwargs):
    trace_event("gui login")
    login()
    sys.exit(0)


@cli.command("logout")
@click.argument("args", nargs=-1)
def gui_logout(args=None, **kwargs):
    trace_event("gui logout")
    logout()
    sys.exit(0)


@cli.command("migrate")
@click.argument("args", nargs=-1)
def gui_migrate(args=None, **kwargs):
    trace_event("gui migrate")
    migrate_local_db()
    sys.exit(0)


@cli.command("init")
@click.argument("args", nargs=-1)
def gui_init(args=None, **kwargs):
    trace_event("gui init")
    init_config(log=True)
