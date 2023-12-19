<div align="center">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_light_theme.svg#gh-light-mode-only" alt="Nextpy Logo" width="320px">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_dark_theme.svg#gh-dark-mode-only" alt="Nextpy Logo" width="320px">
<hr>

<h3> Pythonic Web App framework: For Humans & LLMs</h3>

```diff
+ 🤖 Searching for 'OpenAMS' or 'OpenAgent'? They're now seamlessly integrated into Nextpy. +
```

</div>

## Q: Is it production-ready?

Congratulations on discovering Nextpy before its beta launch! 🧭 While it's stable and we're rigorously testing it in our own production, we recommend a cautious approach for immediate production use. Be aware of its unique quirks and minor bugs, currently on our 'Array of Minor Annoyances' list.

**Ready to Dive In?**

Ahoy, adventurer! 🏴‍☠️ We're thrilled to have you aboard. Let's create something extraordinary together! ✨

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## Origin tale of Next.py

In our quest to create apps that write themselves, we delved deep into a labyrinth of coding tools, frameworks, and libraries. Our experiments spanned all major large language models (LLMs), thousands of prompts, and every major web development framework, from React to Streamlit. 


> [!TIP]
>During this process, we learned that regardless of the LLMs, prompts, or fine-tuning used, the underlying app framework can significantly impact the efficiency of code generation. 


Initially, reflex's flexibility seemed promising, aligning with several of our requirements. However, as we delved deeper into apps development, the absence of crucial features forced us to write large amounts of "glue code" to compensate, ultimately slowing down our development speed.

For months, we avoided reinventing the wheel, Frankenstein-ing disparate tools to stitch together our vision. However, the ROI no longer made sense after a certain point. So, we selectively picked the best ideas from prior frameworks and combined them to build a high-performance web app framework. It has the simplicity of streamlit and the speed and flexibility of Next.js. Our goal is to develop Next.py into the premier framework for both humans and AI agents.




![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## ⚙️ Installation

To install, open a terminal and run (Python 3.7 or higher required):

```bash
pip install nextpy
```

## 🚀 Quickstart (5 mins)

Kickstart your first Nextpy app with this easy guide. We'll guide you through the essential steps to get a Nextpy app running quickly.

For a more in-depth project, explore our app examples.

### Setting Up

1. **Create a New Directory:**
   Open a terminal and create a new directory for your app:

   ```bash
   mkdir myapp
   ```

2. **Navigate to Your Directory:**
   Switch to your newly created directory:

   ```bash
   cd myapp
   ```

3. **Initialize Your App:**
   Start your app with this command:
   ```bash
   nextpy init
   ```
   Choose from:
   - **Blank Template:** For a fresh start.
   - **Base Template:** For a pre-setup experience.

### Running Your App

1. **Start the App:**
   Inside your app's directory, run:

   ```bash
   nextpy run
   ```

2. **View the App:**
   Check out your app by visiting [http://localhost:3000](http://localhost:3000) in a browser.

---

### Building a Joke Generator App

Edit `myapp/myapp.py` to create your app.

#### Import Libraries

```python
import nextpy as xt
import pyjokes
```

Start by importing `nextpy` for development and `pyjokes` for random jokes.

#### Set Up the App State

```python
class State(xt.State):
    joke: str = "Click the button to get a joke!"

    def generate_joke(self):
        self.joke = pyjokes.get_joke()
```

Create a `State` class with a `joke` variable. Use `generate_joke` to fetch new jokes.

#### Design the Main Page

```python
def index():
    return xt.vstack(
        xt.text(State.joke, font_size="2em"),
        xt.button(
            "Generate Joke",
            on_click=State.generate_joke,
        ),
        spacing="1em",
        align_items="center",
        justify_content="center",
        height="100vh",
    )
```

The `index` function arranges a joke display and a button, centered on the screen.

#### Build and Run the App

```python
app = xt.App()
app.add_page(index)
app.compile()
```

Set up the app, add the main page, and prepare it for launch.

> [!NOTE]
> Your app, completed in under 25 lines, will be accessible at `localhost:3000` with the server running on `localhost:8000`.

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## 🙏 Thanks

Nextpy Framework is a state-of-the-art app development framerwork optimized for AI-based code generation, built on the open-source community’s spirit of cooperation. It integrates key components from landmark projects like Guidance, Llama-Index, FastAPI-Mail, LangChain, ReactPy, Reflex, Chakra, Radix, Numpy and Next.js, while also drawing insights from the React and Rust ecosystems. This fusion ideas has been pivotal in shaping Nextpy into a framework that's not just AI-friendly but also a trailblazer in generative web development tools.

We are deeply grateful to the open-source creators, contributors, and maintainers whose work has provided the basis for Nextpy. Your commitment to innovation and openness has been vital for shaping this framework. Your contributions have not only enhanced Nextpy but are also advancing the new era of AI-powered software development. Thank you for being the catalysts and enablers of this transformational journey.
