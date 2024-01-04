# 🚀 Quick Install (2 mins)

[![Build a python webapp in 3 minutes](https://github.com/anubrag/nextpy/assets/25473195/c41ea5b7-d270-451a-a0d0-8308ff9dbfdc)](https://www.youtube.com/watch?v=5Ex-c9wwiYE)

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


## 🛣️ Project Roadmap

**🌟 Upcoming Features**

1. **Frontend Magic Components**
   - 🪄 **PDF Resume to Personal Site**: Create a "magic component" that converts PDF resumes into customizable, full-stack personal websites.

2. **Backend Modules**
   - 🔐 **User Authentication and Email Integration**: Add modules for robust login functionality and email subscription.
   - 🛒 **Modules for Blogging and E-commerce**: Add backend modules to facilitate blog management and e-commerce webapps.

3. **Build and Performance Optimization**
   - 🔧 **Compiler Enhancement with Rust or mojo**: Transitioning our existing compiler to Rust or mojo to achieve faster performance.

4. **Generative AI**
   - 🐍 **Nextpy LLM**: Build the best Python LLM.
   - 💬 **End-User Copilot Feature**: A chat-based copilot for app users that lets them interact with your product and do things by text. We have all the modules ready for this, we just need to simplify the abstraction. Just set `copilot = True` in xtconfig and you’re should be good to go.

## 🤗 Get Involved

**We welcome contributors of all skill levels! 🤝**

Want to make a difference? Start by forking our repository and sending in your pull requests. We're excited to welcome you to our community. Together, we'll craft something truly remarkable! ✨
