<div align="center">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_light_theme.svg#gh-light-mode-only" alt="Nextpy Logo" width="320px">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_dark_theme.svg#gh-dark-mode-only" alt="Nextpy Logo" width="320px">
<hr>

<h3> Pythonic Web App framework: For Humans & LLMs</h3>
<p align="center"><i>Simple like Streamlit + Fast and Flexible like Next.js</i></p>
   

```diff
+ 🤖 Searching for 'OpenAMS' or 'OpenAgent'? They're now seamlessly integrated into Nextpy. +
```

</div>

## Q: Is it production-ready? 

Congratulations on discovering Nextpy before its public launch! 🧭 While the documented features are production-ready (powering our own systems!), some undocumented ones might have quirks. We're actively smoothing them out, and live  [Discord support](https://discord.com/invite/g9PFpVztZg) is just a ping away!

**Ready to Dive In?**

Ahoy, adventurer! 🏴‍☠️ We're thrilled to have you aboard. Let's create something extraordinary together! ✨

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## ⚡ What is Next.py ?
Nextpy is a Python Web App Framework designed for the Age of AI Agents. Built on the best ideas from prior frameworks, it's simple like Streamlit but has the perfomance and flexibility of Next.js.

### 💡 Key Features

#### Simplifying App Development:🧩
- **🐍 Unleash Python's Full Potential** - Eliminate complexities and build everything—frontend and backend—in Python, seamlessly integrating any Python library.
- **🎨 Rich UI Library** - Over 100 fully customizable built-in components for rapid UI development.
- **⚛️ Tap into React's Power with Pythonic Wrappers** - Harness the vast React ecosystem directly within Python, utilizing any React library **_without JavaScript knowledge._**
- **🚀 Built-in Performance Optimizations** - Deliver exceptional user experiences with automatic image, font, and script optimizations for lightning-fast loading speeds and responsiveness. See the difference for yourself at [nextpy.org](https://nextpy.org).

#### Better AI Generations: ‍🤖

- **🧠 More Effective Than Chaining or Prompt Engineering** - Next.py aligns with LLM processing patterns, enabling precise output control and optimal model utilization.
- **💡 Optimized for Code Generation** - Regardless of the LLMs, prompts, or fine-tuning used, the underlying app framework significantly impacts the efficiency of code generation. Next.py's architecture is specifically engineered to maximize efficiency.
- **💾 Session State with LLM** - Efficiently maintain state with LLMs, leveraging KV caches to convert multiple output tokens into prompt token batches. This approach reduces redundant generations, accelerating the handling of lengthy and intricate prompts. **_(only for open-source models)_**
- **🧪 Detect Syntax Errors**: Test LLM-generated code, identifying and correcting LLM hallucinations, invalid Nextpy methods, and automatically generating prompts for seamless fixes.

#### Developer-First: ❤️

- **📘 Transferable Knowledge** - Learning Next.py instills framework-agnostic fundamentals, enhancing your app development expertise and enabling you to excel across any frameworks.
- **🛠️ Extensible** - If you know how to do something in Python or plain English, you can integrate it with nextpy.

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## 🚀 Quick Start (2 mins)

**1. Installing Nextpy**

Open your terminal and prepare for an adventure of a lifetime!

```bash
pip install nextpy
```

**(Remember, Python 3.7 or later is required.)**

**2. Initializing Your App**

Navigate to the desired directory for your project in the terminal. Use the `nextpy init` command to initialize a template app in your new directory.

```bash
nextpy init
```

**3. Choose your template:**

For now, just press enter to automatically default to the blank template.
```md
    Blank Template: A simple single page template
    Base Template: A multi-page app with a sidebar
```

**4. Running the App**

In the same directory where you previously ran nextpy init, enter the following command:

```bash
nextpy run
```

**5. View the App:**

Check out your app by visiting [http://localhost:3000](http://localhost:3000)

> [!NOTE]
> Your application is now fully functional. To view the frontend, navigate to `localhost:3000`. The backend server is accessible at `localhost:8000`.
> While it's unlikely you'll ever directly interact with it, the backend API documentation can be found at `localhost:8000/docs`, and the openapi.json file is located at `localhost:8000/openapi.json`.


## 🎨 Start with a template!

We speedup your development with a [ever growing list of community templates](https://github.com/dot-agent/nextpy/tree/main/app-examples). Some examples:

<table border="0">
  <tr>
    <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429508/github_nextpy/glide_datagrid_2x_fdxoyy.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
    <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429508/github_nextpy/portfolio_2x_y4lzet.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
     <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429509/github_nextpy/chart_2x_eh0q9x.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
     <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429509/github_nextpy/chat_app_2x_cmsaht.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
     <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429509/github_nextpy/crud_2x_bcxiyp.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
     <td>
      <a target="_blank" href="https://nextpy.org/">
        <img src="https://res.cloudinary.com/doojikdqd/image/upload/v1703429508/github_nextpy/login_2x_hgjpo2.png" style="max-height:150px; width:auto; display:block;">
      </a>
    </td>
  </tr>
  <tr>
    <td>Powerful tables</td>
    <td>Portfolio Sites</td>
    <td>Interactive Charts</td>
    <td>AI chat</td>
    <td>Crud Apps</td>
    <td>Onboarding</td>
  </tr>
</table>

### Setting Up the Template
1. Copy the template files to your local folder.
2. Install necessary dependencies with **`pip install -r requirements.txt`**.
3. Initialize your app by running **`nextpy init`**.
4. Launch the app with **`nextpy run`** to see it in action. To check the site visit `localhost:3000`


# ➖ or ➖ 
---

### 🤣 Building a Joke Generator App (5 mins)

Edit `myapp/myapp.py` to create your app.

#### 1. Import Libraries

```python
import nextpy as xt
import pyjokes
```

Start by importing `nextpy` for development and `pyjokes` for random jokes.

#### 2. Set Up the App State

```python
class State(xt.State):
    joke: str = "Click the button to get a joke!"

    def generate_joke(self):
        self.joke = pyjokes.get_joke()
```

Create a `State` class with a `joke` variable. Use `generate_joke` to fetch new jokes.

#### 3. Design the Main Page

```python
def index():
    layout = xt.vstack(
        xt.text(State.joke, font_size="2em"),
        xt.button("Generate Joke", on_click=State.generate_joke),
    )
    return layout
```

The `index` function arranges a joke display and a button. `vstack` is used to stack components vertically, while `hstack` is used to stack components horizontally.

#### 4. Optional Styling
```md
def index():
    layout = xt.vstack(
        xt.text(State.joke, font_size="2em"),
        xt.button("Generate Joke", on_click=State.generate_joke),

        spacing="1em",
        align_items="center",
        justify_content="center",
        height="100vh",
   )
    return layout
```
The `spacing` attribute adds space between the `text` and `button` elements, while `align_items` and `justify_content` ensure that these elements are centered. The stack's `height` is set to 100% of the Viewport Height (`100vh`), which allows the vertical stack to fill the entire height of your screen.

#### 5. Setup the app

```python
app = xt.App()
app.add_page(index)

```

Set up the app, add the main page. To view the frontend, navigate to `localhost:3000`. 


![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)





## Why another framework?

In our quest to create apps that write themselves, we delved deep into a labyrinth of coding tools, frameworks, and libraries. Our experiments spanned all major large language models (LLMs), thousands of prompts, and every major web development framework, from React to Streamlit.


> [!TIP]
>During this process, we learned that regardless of the LLMs, prompts, or fine-tuning used, the underlying app framework can significantly impact the efficiency of code generation. 


Initially, reflex's flexibility seemed promising, aligning with several of our requirements. However, as we delved deeper into apps development, the absence of crucial features forced us to write large amounts of "glue code" to compensate, ultimately slowing down our development speed.

For months, we avoided reinventing the wheel, Frankenstein-ing disparate tools to stitch together our vision. However, the ROI no longer made sense after a certain point. So, we selectively picked the best ideas from prior frameworks and combined them to build a high-performance web app framework. It has the simplicity of streamlit and the speed and flexibility of Next.js. Our goal is to develop Next.py into the most efficeint app development framework for both humans and AI agents.

## 🙏 Thanks


Nextpy Framework is a state-of-the-art app development framerwork optimized for AI-based code generation, built on the open-source community’s spirit of cooperation. It integrates key components from landmark projects like Guidance, Llama-Index, FastAPI-Mail, LangChain, ReactPy, Reflex, Chakra, Radix, Numpy and Next.js, while also drawing insights from the React and Rust ecosystems. This fusion ideas has been pivotal in shaping Nextpy into a framework that's not just AI-friendly but also a trailblazer in generative web development tools.

We are deeply grateful to the open-source creators, contributors, and maintainers whose work has provided the basis for Nextpy. Your commitment to innovation and openness has been vital for shaping this framework. Your contributions have not only enhanced Nextpy but are also advancing the new era of AI-powered software development. Thank you for being the catalysts and enablers of this transformational journey.
