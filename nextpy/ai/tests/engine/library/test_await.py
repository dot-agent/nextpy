from nextpy.ai import engine


def test_await():
    """Test the behavior of `await`."""
    prompt = engine(
        """Is Everest very tall?
User response: '{{set 'user_response' (await 'user_response') hidden=False}}'"""
    )
    waiting_prompt = prompt()
    assert str(waiting_prompt) == str(prompt)
    out = waiting_prompt(user_response="Yes")
    assert str(out) == "Is Everest very tall?\nUser response: 'Yes'"
