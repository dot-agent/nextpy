<p align="center"> 
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Symbols/Blue%20Circle.png" alt="Blue Circle" width="50" height="50" />
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Robot.png" alt="Robot" width="175" height="175" />
</p>
<p><em>Hey there, Friend!
This project is still in the &quot;just for friends&quot; stage. If you want to see what we&#39;re messing with and have some thoughts, take a look at the code. Would love your thoughts or contributions .</em></p>

<h1 id="-why-we-started-dotagent-"><strong>Why we started dotagent?</strong></h1>

<p>We have a dream: Open and democratic AGI , from blackbox censorship and control imposed by private corporations under the disguise of alignment. We once had this with the web but lost this liberty to the corporate giants of the mobile era, whose duopoly has imposed a fixed 30% tax on all developers.</p>
<p>Our moonshot : A network of domain specific AI agents , collaborating so seamlessly that it feels like AGI. Contribute to democratizing the LAST technological frontier.</p>

![-----------------------------------------------------](https://github.com/dotagent-ai/openagent/blob/7a0ee18ee988da4d0d834d95702417b057d2722f/divider.gif)


<h1 id="what-is-openagent-">What is OpenAgent ?</h1>
<p>OpenAgent is a library of modular components and an orchestration framework. Inspired by a microservices approach, it gives developers all the components they need to build robust, stable &amp; reliable AI applications and experimental autonomous agents.</p>

![-----------------------------------------------------](https://github.com/dotagent-ai/openagent/blob/7a0ee18ee988da4d0d834d95702417b057d2722f/divider.gif)

<h1 id="features">Features</h1>
<h3 id="modularity">1. Modularity</h3>
<ul>
<li><em><strong>Multiplatform:</strong></em> Agents do not have to run on a single location or machine. Different components can run across various platforms, including the cloud, personal computers, or mobile devices.</li>
<li><em><strong>Extensible:</strong></em> If you know how to do something in Python or plain English, you can integrate it with OpenAgent.</li>
</ul>
<h3 id="guardrails">2. Guardrails</h3>
<ul>
<li><em><strong>Set clear boundaries:</strong></em> Users can precisely outline what their agent can and cannot do. This safeguard guarantees that the agent remains a dynamic, self-improving system without overstepping defined boundaries.</li>
</ul>
<h3 id="greater-control-with-structured-outputs">3. Greater control with Structured outputs</h3>
<ul>
<li><em><strong>More Effective Than Chaining or Prompting:</strong></em> The prompt compiler unlocks the next level of prompt engineering, providing far greater control over LLMs than few-shot prompting or traditional chaining methods.</li>
<li><em><strong>Superpowers to Prompt Engineers:</strong></em> It gives full power of prompt engineering, aligning with how LLMs actually process text. This understanding enables you to precisely control the output, defining the exact response structure and instructing LLMs on how to generate responses.</li>
</ul>
<h3 id="powerful-prompt-compiler">4. Powerful Prompt Compiler</h3>
<p>The philosophy is to handle more processing at compile time and maintain better session with LLMs.</p>
<ul>
<li><em><strong>Pre-compiling prompts:</strong></em> By handling basic prompt processing at compile time, unnecessary redundant LLM processing are eliminated.</li>
<li><em><strong>Session state with LLM:</strong></em> Maintaining state with LLMs and reusing KV caches can eliminate many redundant generations and significantly speed up the process for longer and more complex prompts. <em>(only for opensource models)</em></li>
<li><em><strong>Optimized tokens:</strong></em> Compiler can transform many output tokens into prompt token batches, which are cheaper and faster. The structure of the template can dynamically guide the probabilities of subsequent tokens, ensuring alignment with the template and optimized tokenization . <em><strong>(only for opensource models)</strong></em></li>
<li><em><strong><strong>Speculative sampling (WIP):</strong></strong></em> You can enhance token generation speed in a large language model by using a smaller model as an assistant. The method relies on an algorithm that generates multiple tokens per transformer call using a faster draft model. This can lead to upto 3x speedup in token generation .</li>
</ul>
<h3 id="-containerized-scalable-"><strong>5. Containerized &amp; Scalable</strong></h3>
<ul>
<li>.🤖 <em><strong>files :</strong></em> Agents can be effortlessly exported into a simple .agent or .🤖 file, allowing them to run in any environment.</li>
<li><em><strong>Sandboxed (optional):</strong></em> Agents should be able to optimize computing resources inside a sandbox. You can use Agentbox locally or on a cloud with a simple API, This can be deployed both locally or on the cloud through a straightforward API, offering additional control and safety.</li>
</ul>

<hr>
