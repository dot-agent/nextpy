import ipyvuetify as v
from IPython.display import display

def create_container_with_layout_and_card(card_contents):
    # Use user-defined content to create cards dynamically
    cards = [
        v.Card(class_='ma-2', children=[
            v.CardTitle(class_='headline', children=[content['title']]),
            v.CardText(children=[content['text']])
        ]) for content in card_contents
    ]
    
    layout = v.Layout(row=True, wrap=True, children=cards)
    
    container = v.Container(fluid=True, children=[layout])
    
    return container