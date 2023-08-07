
example="""
{{#user~}}
Current summary:
The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good.

New lines of conversation:
Human: Why do you think artificial intelligence is a force for good?
AI: Because artificial intelligence will help humans reach their full potential.

New summary:
{{~/user}}

{{#assistant~}}
The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good because it will help humans reach their full potential.
{{~/assistant}}
"""

SUMMARIZER_TEMPLATE = """
{{#system~}}
You are a helpful and terse assistant.
{{~/system}}

{{#user~}}
Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary.
{{~/user}}

{{#assistant~}}
Ok, I will do that. Let's do a practice round
{{~/assistant}}

"""+example+"""

{{#user~}}
That was great. Lets do another one.
Current summary:
{{summary}}

New lines of conversation:
{{ new_lines }}

New summary:
{{~/user}}

{{#assistant~}}
{{gen 'result' temperature=0}}
{{~/assistant}}
"""