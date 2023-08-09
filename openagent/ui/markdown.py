import os

from openagent.ui.logger import logger

# Default openagent.ui.md file created if none exists
DEFAULT_MARKDOWN_STR = """# Welcome to openagent_ui! 🚀🤖

Hi there, Developer! 👋 We're excited to have you on board. openagent_ui is a powerful tool designed to help you prototype, debug and share applications built on top of LLMs.

## Useful Links 🔗

- **Documentation:** 📚
- **Discord Community:** 💬

We can't wait to see what you create with openagent_ui! Happy coding! 💻😊

## Welcome screen

To modify the welcome screen, edit the `openagent.ui.md` file at the root of your project. If you do not want a welcome screen, just leave this file empty.
"""


def init_markdown(root: str):
    """Initialize the openagent.ui.md file if it doesn't exist."""
    openagent_ui_md_file = os.path.join(root, "openagent.ui.md")

    if not os.path.exists(openagent_ui_md_file):
        with open(openagent_ui_md_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_MARKDOWN_STR)
            logger.info(f"Created default openagent_ui markdown file at {openagent_ui_md_file}")


def get_markdown_str(root: str):
    """Get the openagent.ui.md file as a string."""
    openagent_ui_md_path = os.path.join(root, "openagent_ui.md")
    if os.path.exists(openagent_ui_md_path):
        with open(openagent_ui_md_path, "r", encoding="utf-8") as f:
            openagent_ui_md = f.read()
            return openagent_ui_md
    else:
        return None
