# Engine   
   
The engine is designed to process prompts efficiently for large language models (LLMs), offering users the ability to create very controlled text generation . This tool integrates the flexibility of regular expressions and context-free grammars (CFGs) to restrict and guide output. Additionally, it provides mechanisms to interweave control structures like conditionals and loops with text generation, allowing for more complex interactions.  
   
For opensource models using key-value (KV) caches, the engine can maintain state across interactions with LLMs, which is particularly useful when dealing with long and complicated prompts. This stateful approach minimizes redundant generation steps, leading to faster responses when handling detailed prompts. 

This module furthers the development of what is now an depricated version of guidance. It leverages templating mechanisms to centralize the logic of prompt creation, leading to a workflow that is both more streamlined and maintainable. 
   
Key Features:  
- **Prompt Templates**: These are the core of the engine, allowing for dynamic text generation by using placeholders that can be filled with variable content.  
- **Handlebars-Based Syntax**: An intuitive and widely-used syntax that simplifies the creation of flexible templates.  
- **LLM Integration**: Direct and efficient interaction with state-of-the-art LLMs to produce high-quality text outputs.  
   
## Importing the engine
   
```python  
from nextpy.ai import engine  
   
api_key = "sk-api_key"  
model_35_turbo = engine.llms.OpenAI("gpt-3.5-turbo", chat_mode=True, api_key=api_key, caching=False)  
model_davinci = engine.llms.OpenAI("text-davinci-003", chat_mode=False, api_key=api_key, caching=False)  
```  
In this section, we import the `engine` from the `nextpy.ai` library. We also initialize the models that we will be using in this tutorial.  
   
## Basic Templating  
   
### Single Variable  
   
```python  
program = engine('''What is {{example}}?''')  
   
# this program has not been executed yet, so it still has the template placeholder in it  
program   
```  
In the example above, we define a `program` with a placeholder `{{example}}`. The program hasn't been executed yet, so the placeholder remains.  
   
```python  
# when we execute the program (by calling it) template placeholders are filled in  
# note that keyword arguments to the program become variables in the template namespace  
executed_program = program(example='truth')  
```  
When we execute the program by calling it and passing an argument (`example='truth'`), the placeholder is replaced with the argument.  
   
```python  
# all the variables used by the program are returned as part of the executed program  
executed_program['example']  
```  
All the variables used by the program are returned as part of the executed program.  
   
### Lists and Objects  
   
```python  
# define some variables we will use in the engine program  
people = ['John', 'Mary', 'Bob', 'Alice']  
ideas = [  
    {'name': 'truth', 'description': 'the state of being the case'},  
    {'name': 'love', 'description': 'a strong feeling of affection'}  
]  
   
# we can use the `each` block to iterate over a list  
program = engine('''List of people:  
{{#each people}}- {{this}}  
{{~! This is a comment. The ~ removes adjacent whitespace either before or after a tag, depending on where you place it}}  
{{/each~}}  
List of ideas:  
{{#each ideas}}{{this.name}}: {{this.description}}  
{{/each}}''')  
   
program(people=people, ideas=ideas)  
```  
In the example above, we use the `each` block to iterate over a list. The `each` block loops over an array or an iterable object and renders the block of code for each item.  
   
### Includes (including engine programs inside other programs)  
   
```python  
# define the program we will include  
program1 = engine('''List of people:  
{{#each people}}- {{this}}  
{{/each~}}''')  
   
# note that {{>prog_name}} is the same include syntax as in Handlebars  
program2 = engine('''{{>program1}}  
List of ideas:  
{{#each ideas}}{{this.name}}: {{this.description}}  
{{/each}}''')  
   
# we can pass program just like any other variable  
program2(program1=program1, people=people, ideas=ideas)  
```  
In the example above, we include one `engine` program inside another. This is done using the `{{>prog_name}}` syntax, which is the same as in Handlebars.   
  
### Generating text from an LLM  
   
```python  
# we can use the {{gen}} command to generate text from the language model  
# note that we used a ~ at the start of the command tag to remove the whitespace before it (just like in Handlebars)  
program = engine('''The best thing about the beach is {{~gen 'best' temperature=0.7 max_tokens=7}}''',llm = model_davinci)  
program()  
```  
In the example above, we use the `{{gen}}` command to generate text from the language model. The `~` character is used at the start of the command tag to remove the whitespace before it.  
   
### Flushing caches  
   
```python  
# you can flush a cache by calling the clear method  
# (this returns the number of items that were cleared)  
engine.llms.OpenAI.cache.clear()  
   
# you can also disable caching by passing caching=False to the LLM constructor  
# engine.llm = engine.llms.OpenAI("text-davinci-003", caching=False)  
```  
In the example above, we clear the cache by calling the `clear` method. We can also disable caching by passing `caching=False` to the LLM constructor.  
   
### Selecting alternatives with the LLM  
   
```python  
# the {{#select}} command allows you to use the LLM to select from a set of options  
program = engine('''Is the following sentence offensive? Please answer with a single word, either "Yes", "No", or "Maybe".  
Sentence: {{example}}  
Answer:{{#select "answer" logprobs='logprobs'}} Yes{{or}} No{{or}} Maybe{{/select}}''',llm = model_davinci )  
executed_program = program(example='I hate tacos')  
```  
In the example above, we use the `{{#select}}` command to allow the LLM to select from a set of options.   
  
```python  
# all the variables set by the program are returned as part of the executed program  
executed_program['logprobs']  
```  
All the variables set by the program are returned as part of the executed program.  
   
```python  
executed_program['answer']  
```  
We can access the selected answer by calling `executed_program['answer']`.  
   
```python  
# the example above used a block version of the select command, but you can also  
# use a non-block version and just pass in a list of options  
options = [' Yes', ' No', ' Maybe']  
program = engine('''Is the following sentence offensive? Please answer with a single word, either "Yes", "No", or "Maybe".  
Sentence: {{example}}  
Answer:{{select "answer" options=options}}''',llm = model_davinci)  
executed_program = program(example='I hate tacos', options=options)  
```  
In the example above, we use the non-block version of the `select` command, and just pass in a list of options.  
   
```python  
executed_program["answer"]  
```  
We can access the selected answer by calling `executed_program['answer']`.  
   
```python  
executed_program['response'], executed_program['answer']  
```  
We can access the response and the answer by calling `executed_program['response']` and `executed_program['answer']`.  
   
### Hidden  
   
```python  
# it is often useful to execute a part of the program, but then not include that part in later context  
# given to the language model. This can be done using the hidden=True argument. Several commands support  
# hidden=True, but here we use the {{#block}} command (which is just a generic block command that does  
# nothing other than what the arguments you pass to it do)  
program = engine('''{{#block hidden=True}}Generate a response to the following email:  
{{email}}.  
Response:{{gen "response"}}{{/block}}  
I will show you an email and a response, and you will tell me if it's offensive.  
Email: {{email}}.  
Response: {{response}}  
Is the response above offensive in any way? Please answer with a single word, either "Yes" or "No".  
Answer:{{#select "answer" logprobs='logprobs'}} Yes{{or}} No{{/select}}''',llm = model_davinci)  
   
executed_program = program(email='I hate tacos')  
```  
In the example above, we use the `{{#block}}` command with `hidden=True` argument. This allows us to execute a part of the program, but then not include that part in later context given to the language model.  
   
### Silent execution  
   
```python  
# if you want to run a program without displaying the output, you can use the silent=True argument  
executed_program = program(email='I hate tacos', silent=True)  
executed_program['answer']  
```  
In the example above, we run a program without displaying the output by using the `silent=True` argument.  
   
### Generating with `n>1`  
   
```python  
# the {{gen}} command the n=number argument to generate multiple completions  
# only the first completion is used for future context, but the variable set  
# by the command is a list of all the completions, and you can interactively  
# click through each completion in the notebook visualization  
program = engine('''The best thing about the beach is{{gen 'best' n=3 temperature=0.7 max_tokens=7}}''',llm = model_davinci)  
executed_program = program()  
```  
In the example above, we use the `{{gen}}` command with the `n=number` argument to generate multiple completions. Only the first completion is used for future context, but the variable set by the command is a list of all the completions.  
   
```python  
executed_program["best"]  
```  
We can access the generated completions by calling `executed_program['best']`.  
   
### Calling custom user defined functions  
   
```python  
# all the built in commands are functions from engine.library.* but you can also pass in your own functions  
def aggregate(best):  
    return '\n'.join(['- ' + x for x in best])  
   
# note that we use hidden=True to prevent the {{gen}} command from being included in the output, and instead  
# just use the variable it sets as an input to the aggregate function  
program = engine('''The best thing about the beach is{{gen 'best' n=3 temperature=0.7 max_tokens=7 hidden=True}}  
{{aggregate best}}''',llm = model_davinci)  
executed_program = program(aggregate=aggregate)  
```  
In the example above, we define a custom function `aggregate` that aggregates the best things about the beach. We then use this function in the `engine` program.  
   
### Await  
   
```python  
# sometimes you want to partially execute a program, the `await` command allows you to do this  
# it awaits a variable and then consumes that variables (so after the await command the variable)  
prompt = engine('''Generate a response to the following email:  
{{email}}.  
Response:{{gen "response"}}\n  
{{await 'instruction'}}\n  
{{gen 'updated_response'}}''', stream=True,llm = model_davinci )  
   
# note how the executed program is only partially executed, it stops at the await command  
# because the instruction variable is not yet set  
prompt = prompt(email='Hello there')  
```  
In the example above, we partially execute a program using the `await` command. The `await` command allows for partial execution of a program and awaits a variable before proceeding further.  
   
```python  
prompt2 = prompt(instruction='Please translate the response above to Portuguese.',llm = model_davinci)  
prompt2  
```  
The program can be continued by passing the awaited variable, as shown above.  
   
```python  
prompt2 = prompt(instruction='Please translate the response above to Chinese.')  
prompt2  
```  
The program can be continued further by passing another awaited variable.  
   
### Chat  
   
```python  
# to use role based chat tags you need a chat model, here we use gpt-3.5-turbo but you can use 'gpt-4' as well  
engine.llm = engine.llms.OpenAI("gpt-3.5-turbo")  
```  
In the example above, we use a chat model `gpt-3.5-turbo` to use role-based chat tags. You can also use 'gpt-4'.  
   
```python  
# note that we enclose all of the text in one of the valid role tags for the model  
# `system`, `user`, and `assistant` are just shorthand for {{#role name="system"}}...{{/role}}  
# the whitepace outside the role tags is ignored by gpt-4, the whitespace inside the role tags is not  
# so we use the ~ to remove the whitespace we don't want to give to the model (but want to keep in the code for clarity)  
program = engine('''The best thing about the beach is {{~gen 'best' temperature=0.7 max_tokens=7}}''',llm = model_davinci)  
program()  
```  
In the example above, we enclose all of the text in one of the valid role tags for the model. The role tags are `system`, `user`, and `assistant`.  
   
### Multistep  
   
```python  
experts = engine('''\n  
{{#system~}}\n  
You are a helpful assistant.\n  
{{~/system}}\n  
\n  
{{#user~}}\n  
I want a response to the following question:\n  
{{query}}\n  
Who are 3 world-class experts (past or present) who would be great at answering this?\n  
Please don't answer the question or comment on it yet.\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
{{gen 'experts' temperature=0 max_tokens=300}}\n  
{{~/assistant}}\n  
\n  
{{#user~}}\n  
Great, now please answer the question as if these experts had collaborated in writing a joint anonymous answer.\n  
In other words, their identity is not revealed, nor is the fact that there is a panel of experts answering the question.\n  
If the experts would disagree, just present their different positions as alternatives in the answer itself (e.g. 'some might argue... others might argue...').\n  
Please start your answer with ANSWER:\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
{{gen 'answer' temperature=0 max_tokens=500}}\n  
{{~/assistant}}''',llm = model_35_turbo)  
                     
experts(query='What is the meaning of life?')  
```  
In the example above, we create and guide multi-turn conversations by using a series of role tags.  
   
### Using tools  
   
```python  
def is_search(completion):  
    return '<search>' in completion  
   
def search(query):  
    # Fake search results  
    return [{'title': 'How do I cancel a Subscription? | Facebook Help Center',  
        'snippet': "To stop a monthly Subscription to a creator: Go to the creator's Facebook Page using the latest version of the Facebook app for iOS, Android or from a computer. Select Go to Supporter Hub. Select . Select Manage Subscription to go to the iTunes or Google Play Store and cancel your subscription. Cancel your Subscription at least 24 hours before ..."},  
        {'title': 'News | FACEBOOK Stock Price Today | Analyst Opinions - Insider',  
        'snippet': 'Stock | News | FACEBOOK Stock Price Today | Analyst Opinions | Markets Insider Markets Stocks Indices Commodities Cryptocurrencies Currencies ETFs News Facebook Inc (A) Cert Deposito Arg Repr...'},  
        {'title': 'Facebook Stock Price Today (NASDAQ: META) Quote, Market Cap, Chart ...',  
        'snippet': 'Facebook Stock Price Today (NASDAQ: META) Quote, Market Cap, Chart | WallStreetZen Meta Platforms Inc Stock Add to Watchlist Overview Forecast Earnings Dividend Ownership Statistics $197.81 +2.20 (+1.12%) Updated Mar 20, 2023 Meta Platforms shares are trading... find out Why META Price Moved with a free WallStreetZen account Why Price Moved'}]  
   
search_demo = engine('''Seach results:\n  
{{~#each results}}\n  
<result>\n  
{{this.title}}\n  
{{this.snippet}}\n  
</result>{{/each}}''')  
   
demo_results = [  
    {'title': 'OpenAI - Wikipedia', 'snippet': 'OpenAI systems run on the fifth most powerful supercomputer in the world. [5] [6] [7] The organization was founded in San Francisco in 2015 by Sam Altman, Reid Hoffman, Jessica Livingston, Elon Musk, Ilya Sutskever, Peter Thiel and others, [8] [1] [9] who collectively pledged US$ 1 billion. Musk resigned from the board in 2018 but remained a donor.'},  
    {'title': 'About - OpenAI', 'snippet': 'About OpenAI is an AI research and deployment company. Our mission is to ensure that artificial general intelligence benefits all of humanity. Our vision for the future of AGI Our mission is to ensure that artificial general intelligence—AI systems that are generally smarter than humans—benefits all of humanity. Read our plan for AGI'},   
    {'title': 'Ilya Sutskever | Stanford HAI', 'snippet': '''Ilya Sutskever is Co-founder and Chief Scientist of OpenAI, which aims to build artificial general intelligence that benefits all of humanity. He leads research at OpenAI and is one of the architects behind the GPT models. Prior to OpenAI, Ilya was co-inventor of AlexNet and Sequence to Sequence Learning.'''}  
]  
   
s = search_demo(results=demo_results)  
   
practice_round = [  
    {'role': 'user', 'content' : 'Who are the founders of OpenAI?'},  
    {'role': 'assistant', 'content': '<search>Who are the founders of OpenAI</search>'},  
    {'role': 'user', 'content': str(search_demo(results=demo_results))},  
    {'role': 'assistant', 'content': 'The founders of OpenAI are Sam Altman, Reid Hoffman, Jessica Livingston, Elon Musk, Ilya Sutskever, Peter Thiel and others.'},  
]  
   
program = engine('''\n  
{{#system~}}\n  
You are a helpful assistant.\n  
{{~/system}}\n  
\n  
{{#user~}}\n  
From now on, whenever your response depends on any factual information, please search the web by using the function <search>query</search> before responding. I will then paste web results in, and you can respond.\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
Ok, I will do that. Let's do a practice round\n  
{{~/assistant}}\n  
\n  
{{#each practice}}\n  
{{#if (== this.role "user")}}\n  
{{#user}}{{this.content}}{{/user}}\n  
{{else}}\n  
{{#assistant}}{{this.content}}{{/assistant}}\n  
{{/if}}\n  
{{/each}}\n  
\n  
{{#user~}}\n  
That was great, now let's do another one.\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
Sounds good\n  
{{~/assistant}}\n  
\n  
{{#user~}}\n  
{{user_query}}\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
{{gen "query" stop="</search>"}}{{#if (is_search query)}}</search>{{/if}}\n  
{{~/assistant}}\n  
\n  
{{#user~}}\n  
Search results: {{#each (search query)}}\n  
<result>\n  
{{this.title}}\n  
{{this.snippet}}\n  
</result>{{/each}}\n  
{{~/user}}\n  
\n  
{{#assistant~}}\n  
{{gen "answer"}}\n  
{{~/assistant}}\n  
''',llm = model_35_turbo)  
   
query = "What is Facebook's stock price right now?"  
   
program = program(  
    user_query=query,  
    search=search,  
    is_search=is_search,  
    practice=practice_round  
)  
```  
In the example above, the assistant uses a search engine to answer user questions. The entire system is defined in a single `engine` program.
