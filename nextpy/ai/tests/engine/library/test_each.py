from nextpy.ai import engine

from ..utils import get_llm


def test_each():
    """Test an each loop."""
    prompt = engine("Hello, {{name}}!{{#each names}} {{this}}{{/each}}")
    assert (
        str(prompt(name="Compiler", names=["Bob", "Sue"])) == "Hello, Compiler! Bob Sue"
    )


def test_each_with_objects():
    """Test an each loop with objects."""
    prompt = engine("Hello, {{name}}!{{#each names}} {{this.name}}{{/each}}")
    out = prompt(name="Compiler", names=[{"name": "Bob"}, {"name": "Sue"}])
    assert str(out) == "Hello, Compiler! Bob Sue"


def test_missing_list():
    prompt = engine(
        """List of ideas:{{#each ideas}}test{{this}}{{/each}}""", await_missing=True
    )
    assert str(prompt()) == "List of ideas:{{#each ideas}}test{{this}}{{/each}}"
    # try:
    #     out = prompt()
    # except KeyError:
    #     return
    # assert False, "An error should have been raised because the list is missing!"


def test_each_after_await():
    """Test an each loop when we are not executing."""
    prompt = engine(
        "Hello, {{name}}!{{await 'some_var'}}{{#each names}} {{this}}{{/each}}"
    )
    assert (
        str(prompt(name="Compiler", names=["Bob", "Sue"]))
        == "Hello, Compiler!{{await 'some_var'}}{{#each names}} {{this}}{{/each}}"
    )


def test_each_over_an_await():
    """Test an each loop when we are not executing."""
    program = engine("Hello, {{name}}!{{#each (await 'names')}} {{this}}{{/each}}")
    partial_execution = program(name="Compiler")
    assert (
        str(partial_execution)
        == "Hello, Compiler!{{#each (await 'names')}} {{this}}{{/each}}"
    )
    full_execution = partial_execution(names=["Bob", "Sue"])
    assert str(full_execution) == "Hello, Compiler! Bob Sue"


def test_each_parallel():
    """Test an each loop run in parallel."""
    program = engine(
        "Hello, {{name}}!{{#each names parallel=True hidden=True}} {{this}}{{/each}}"
    )
    executed_program = program(name="Compiler", names=["Bob", "Sue", "Sam"])
    assert str(executed_program) == "Hello, Compiler!"


def test_each_parallel_with_gen():
    """Test an each loop run in parallel with generations inside."""
    llm = engine.llms.Mock(["Pizza", "Burger", "Salad"])

    program = engine(
        """Hello, {{name}}! Here are 5 names and their favorite food:
{{#each names parallel=True hidden=True}}{{this}}: {{gen 'foods' list_append=True}}
{{/each}}""",
        llm=llm,
    )
    executed_program = program(name="Compiler", names=["Bob", "Sue", "Sam"])
    assert (
        str(executed_program)
        == "Hello, Compiler! Here are 5 names and their favorite food:\n"
    )
    for food in executed_program["foods"]:
        assert food in ["Pizza", "Burger", "Salad"]


def test_each_parallel_with_gen_openai():
    """Test an each loop run in parallel with generations inside using OpenAI."""
    llm = get_llm("openai:text-curie-001")

    program = engine(
        """Hello, {{name}}! Here are 5 names and their favorite food:
{{#each names parallel=True hidden=True}}{{this}}: {{gen 'foods' list_append=True}}
{{/each}}""",
        llm=llm,
    )
    executed_program = program(name="Compiler", names=["Bob", "Sue", "Sam"])
    assert (
        str(executed_program)
        == "Hello, Compiler! Here are 5 names and their favorite food:\n"
    )
    assert len(executed_program["foods"]) == 3


# def test_with_stop():
#     """ Test an each loop when we are not executing.
#     """

#     token_count = 0
#     def token_limit(item, variables, template_context):
#         nonlocal token_count
#         tokenizer = template_context["@tokenizer"]
#         token_count += len(tokenizer.encode(item))
#         return token_count > 3

#     program = engine("""This is a list of names:
# {{set 'token_start' (len (tokenize prefix))~}}
# {{#each names stop=token_limit}} {{this}}
# {{~if (len (tokenize prefix)) - token_start > 100}}{{break}}{{/if~}}
# {{/each}}""", token_limit=token_limit)

#     program = engine("Hello, {{name}}!{{#each names)}} {{this}}{{/each}}")
#     executed_program = program(name="Compiler", names=["Bob", "Sue", "Sam"])
#     assert str(executed_program) == "Hello, Compiler! Bob Sue Sam"
