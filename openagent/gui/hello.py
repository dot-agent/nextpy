# This is a simple example of a gui app.

from openagent.gui import AskUserMessage, Message, on_chat_start


@on_chat_start
async def main():
    res = await AskUserMessage(content="What is your name?", timeout=30).send()
    if res:
        await Message(
            content=f"Your name is: {res['content']}.\nGui installation is working!\nYou can now start building your own gui apps!",
        ).send()
