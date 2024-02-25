import ipywidgets as widgets
from IPython.display import display, Javascript

def chat_input(placeholder='Say something', button_text='Send'):
    text = widgets.Text(placeholder=placeholder)
    button = widgets.Button(description=button_text)

    def on_send(b):
        user_input = text.value
        print(f"User has sent the following prompt: {user_input}")
        text.value = ''  # Clear the input field

    button.on_click(on_send)
    
    # Custom JavaScript to simulate pressing the button when Enter is pressed in the text input.
    js = Javascript("""
    (function(element){
        var text = element.querySelector('input[type="text"]');
        var button = element.querySelector('button');
        
        text.addEventListener('keydown', function(e){
            if (e.keyCode === 13) {  // 13 is the key code for Enter
                button.click();
            }
        });
    })(element);
    """)

    box = widgets.HBox([text, button])
    display(box, js)