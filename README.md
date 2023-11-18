```diff
+ Looking for 'openams'? Because of a little name clash, it's now called 'openams'. 🤖+
```
<p align="center"> 
<img src="https://res.cloudinary.com/dzznkbdrb/image/upload/c_scale,e_art:primavera,r_30,w_2294/a_0/v1697338678/github-cover-min_exhq8b.webp" />

</p>

## Question:

**I stumbled upon this repository. Is it production ready?**

## Answer:

Kudos on discovering this hidden treasure box! 🧭  While it's fairly stable and we're battle-testing it in our own production, we'd advise a bit of caution for immediate production use. It's got its quirks, and some of them have taken a cozy spot on our *'we'll-look-at-this-later'* list. Jump in, play with it, or use any part of our code. It's all good with the MIT license. 

---

**I'm diving in, quirks and all!**

Ahoy, adventurer! 🏴‍☠️ We're thrilled to have another daring coder join the fray. Here's to creating some coding magic together! ✨ 

<h1 id="-why-we-started-openams-"><strong>The Origin Tale of openams</strong></h1>

<p>Here's our dream: An open and democratic AGI, untouched by the sneaky controls and hush-hush censorship of corporate overlords masquerading under 'alignment'. Remember the good ol' web days? We lost that freedom to the mobile moguls and their cheeky 30% 'because-we-said-so' tax. 🙄</p>
<p>Our moonshot? 🚀 A harmonious ensemble of domain-specific AI agents, working in unison so well, you'd think it's AGI. Join us in opening up the LAST tech frontier for all!</p>

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)


<h1 id="what-is-openams-">Meet World's first AMS!</h1>

<p>Ever heard of an Agent Management System (AMS)? No? Well, probably because we believe we came up with it! 🎩✨ openams proudly wears the badge of being the world's first AMS (yep, we're patting ourselves on the back here). Drawing inspiration from the nifty microservices, it equips developers with a treasure trove of tools to craft sturdy, trusty AI applications and those cool experimental autonomous agents.</p>




<h2 id="modularity"> 🧱 Modularity</h2>
<ul>
<li><em><strong>Multiplatform:</strong></em> Agents do not have to run on a single location or machine. Different components can run across various platforms, including the cloud, personal computers, or mobile devices.</li>
<li><em><strong>Extensible:</strong></em> If you know how to do something in Python or plain English, you can integrate it with openams.</li>
</ul>
<h2 id="guardrails"> 🚧 Guardrails</h2>
<ul>
<li><em><strong>Set clear boundaries:</strong></em> Users can precisely outline what their agent can and cannot do. This safeguard guarantees that the agent remains a dynamic, self-improving system without overstepping defined boundaries.</li>
</ul>
<h2 id="greater-control-with-structured-outputs">🏗️ Greater control with Structured outputs</h2>
<ul>
<li><em><strong>More Effective Than Chaining or Prompting:</strong></em> The prompt compiler unlocks the next level of prompt engineering, providing far greater control over LLMs than few-shot prompting or traditional chaining methods.</li>
<li><em><strong>Superpowers to Prompt Engineers:</strong></em> It gives full power of prompt engineering, aligning with how LLMs actually process text. This understanding enables you to precisely control the output, defining the exact response structure and instructing LLMs on how to generate responses.</li>
</ul>
<h2 id="powerful-prompt-compiler">🏭 Powerful Prompt Compiler</h2>
<p>The philosophy is to handle more processing at compile time and maintain better session with LLMs.</p>
<ul>
<li><em><strong>Pre-compiling prompts:</strong></em> By handling basic prompt processing at compile time, unnecessary redundant LLM processing are eliminated.</li>
<li><em><strong>Session state with LLM:</strong></em> Maintaining state with LLMs and reusing KV caches can eliminate many redundant generations and significantly speed up the process for longer and more complex prompts. <em>(only for opensource models)</em></li>
<li><em><strong>Optimized tokens:</strong></em> Compiler can transform many output tokens into prompt token batches, which are cheaper and faster. The structure of the template can dynamically guide the probabilities of subsequent tokens, ensuring alignment with the template and optimized tokenization . <em><strong>(only for opensource models)</strong></em></li>
<li><em><strong><strong>Speculative sampling (WIP):</strong></strong></em> You can enhance token generation speed in a large language model by using a smaller model as an assistant. The method relies on an algorithm that generates multiple tokens per transformer call using a faster draft model. This can lead to upto 3x speedup in token generation .</li>
</ul>
<h2 id="-containerized-scalable-"><strong>📦 Containerized &amp; Scalable</strong></h2>
<ul>
<li>.🤖 <em><strong>files :</strong></em> Agents can be effortlessly exported into a simple .agent or .🤖 file, allowing them to run in any environment.</li>
<li><em><strong>Agentbox (optional):</strong></em> Agents should be able to optimize computing resources inside a sandbox. You can use Agentbox locally or on a cloud with a simple API, with cloud agentbox offering additional control and safety.</li>
</ul>

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)
## Installation


`pip install openams` 

## Common Errors

### SQLite3 Version Error

If you encounter an error like:



`Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.` 

This is a very common issue with Chroma DB. You can find instructions to resolve this in the [Chroma DB tutorial](https://docs.trychroma.com/troubleshooting#sqlite).

### Here's the code for a full stack chat app with UI, all in a single Python file! (37 lines)

 ```python
import openams.compiler as compiler
from openams.compiler._program import Log
from openams import memory
import chainlit as ui
from dotenv import load_dotenv
load_dotenv()

@ui.on_chat_start
def start_chat():
    compiler.llm = compiler.endpoints.OpenAI(model="gpt-3.5-turbo")


class ChatLog(Log):
    def append(self, entry):
        super().append(entry)
        print(entry)
        is_end = entry["type"] == "end"
        is_assistant = entry["name"] == "assistant"
        if is_end and is_assistant:
            ui.run_sync(ui.Message(content=entry["new_prefix"]).send())


memory = memory.SimpleMemory()

@ui.on_message
async def main(message: str):
    program = compiler(
        """
        {{#system~}}
        You are a helpful assistant
        {{~/system}}

        {{~#geneach 'conversation' stop=False}}
        {{#user~}}
        {{set 'this.user_text' (await 'user_text')  hidden=False}}
        {{~/user}}

        {{#assistant~}}
        {{gen 'this.ai_text' temperature=0 max_tokens=300}}
        {{~/assistant}}
        {{~/geneach}}""", memory = memory
    )

    program(user_text=message, log=ChatLog())


```
The UI will look something like this:
![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/chatapp_1_o3dypp.png)



<hr>
