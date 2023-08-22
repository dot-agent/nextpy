import os

from openagent.gui.logger import logger

# Default gui.md file created if none exists
DEFAULT_MARKDOWN_STR = """# Welcome to Gui! 🚀🤖

Hi there, Developer! 👋 We're excited to have you on board. Gui is a powerful tool designed to help you prototype, debug and share applications built on top of LLMs.

## Useful Links 🔗

- **Documentation:** Get started with our comprehensive [Gui Documentation](https://docs.gui.io) 📚
- **Discord Community:** Join our friendly [Gui Discord](https://discord.gg/ZThrUxbAYw) to ask questions, share your projects, and connect with other developers! 💬

We can't wait to see what you create with Gui! Happy coding! 💻😊

## Welcome screen

To modify the welcome screen, edit the `gui.md` file at the root of your project. If you do not want a welcome screen, just leave this file empty.
"""


def init_markdown(root: str):
    """Initialize the gui.md file if it doesn't exist."""
    gui_md_file = os.path.join(root, "gui.md")

    if not os.path.exists(gui_md_file):
        with open(gui_md_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_MARKDOWN_STR)
            logger.info(f"Created default gui markdown file at {gui_md_file}")


def get_markdown_str(root: str):
    """Get the gui.md file as a string."""
    gui_md_path = os.path.join(root, "gui.md")
    if os.path.exists(gui_md_path):
        with open(gui_md_path, "r", encoding="utf-8") as f:
            gui_md = f.read()
            return gui_md
    else:
        return None
