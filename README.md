

<div align="center">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_light_theme.svg#gh-light-mode-only" alt="ReNextpyflex Logo" width="320px">
<img src="https://raw.githubusercontent.com/dotagent-ai/assets/main/nextpy_logo_dark_theme.svg#gh-dark-mode-only" alt="Nextpy Logo" width="320px">

<hr>

<h3> The Python Framework for Next-Gen Web Apps. </h3>


```diff
+ 🤖 Searching for 'OpenAMS' or 'OpenAgent'? They have now been seamlessly integrated into Nextpy.+
```
</div>

<p align="center"> 


</p>



## Q: Is it production ready?

Kudos on discovering this before its's beta launch! 🧭  While it's fairly stable and we're battle-testing it in our own production, we'd advise a bit of caution for immediate production use.   It comes with its unique quirks and low-priority bugs, all of which are currently residing in our 'Array of Minor Annoyances' list

---

**I'm diving in, quirks and all!**

Ahoy, adventurer! 🏴‍☠️ We're excited to have you on board. Together, let's create something truly extraordinary! ✨!✨  

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## ⚙️ Installation

Open a terminal and run (Requires Python 3.7+):

```bash
pip install nextpy
```
## 🚀 Quick Start with Nextpy

Here's a simplified guide to get your first Nextpy app up and running:

### Setting Up

1. **Make a New Directory:**
   Open your terminal and create a directory for your app:

   ```bash
   mkdir myapp
   ```

2. **Go to Your New Directory:**
   Change to your new app's directory:

   ```bash
   cd myapp
   ```

3. **Start Your Nextpy App:**
   Run the following to initialize your app:

   ```bash
   nextpy init
   ```

   Choose from:
   - **Blank Template**: Start from scratch.
   - **Base Template**: Use a basic pre-setup.

### Running Your App

1. **Run the App:**
   Inside your app's directory, type:

   ```bash
   nextpy run
   ```

2. **See Your App:**
   Open [http://localhost:3000](http://localhost:3000) in a browser.

Let's create a simple joke generator app by editing myapp/myapp.py

![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## Quickstart

### Let's create a Joke Generator App

#### Importing Libraries
```python
import nextpy as xt
import pyjokes
```
First, we import two libraries: `nextpy` to build our app and `pyjokes` to get random jokes.

#### Setting Up the App State
```python
class State(xt.State):
    joke: str = "Click the button to get a joke!"

    def generate_joke(self):
        self.joke = pyjokes.get_joke()
```
We create a `State` class with a `joke` variable that starts with a message. The `generate_joke` function changes `joke` to a new random joke.

#### Designing the Main Page
```python
def index():
    return xt.vstack(
        xt.text(State.joke, font_size="2em"),
        xt.button(
            "Generate Joke",
            on_click=State.generate_joke,
        ),
        spacing="1em",
        align_items="center",  # Aligns items horizontally
        justify_content="center",  # Aligns items vertically
        height="100vh",  # Fills the height of the screen
    )
```
The `index` function creates the app's layout. It arranges a text box to show jokes and a button to get new ones, centering them on the screen.

#### Building and Running the App
```python
app = xt.App()
app.add_page(index)
app.compile()
```
Lastly, we set up the app, add our main page, and get it ready to run.

That's it! Our app is complete in under 25 lines of code. You can view the app's interface at `localhost:3000` and the server runs at `localhost:8000`.


![-----------------------------------------------------](https://res.cloudinary.com/dzznkbdrb/image/upload/v1694798498/divider_1_rej288.gif)

## 🙏 Thanks 

Nextpy Framework is a state-of-the-art app development framerwork optimized for AI-based code generation, built on the open-source community’s spirit of cooperation. It integrates key components from landmark projects like Guidance, Llama-Index, FastAPI-Mail, LangChain, ReactPy, Reflex, Chakra, Radix, Numpy and Next.js, while also drawing insights from the React and Rust ecosystems. This fusion ideas has been pivotal in shaping Nextpy into a framework that's not just AI-friendly but also a trailblazer in generative web development tools.

We are deeply grateful to the open-source creators, contributors, and maintainers whose work has provided the basis for Nextpy. Your commitment to innovation and openness has been vital for shaping this framework. Your contributions have not only enhanced Nextpy but are also advancing the new era of AI-powered software development. Thank you for being the catalysts and enablers of this transformational journey.
