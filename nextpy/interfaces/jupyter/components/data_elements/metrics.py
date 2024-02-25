import ipyvuetify as v

def metrics(label, value, delta=None, delta_color="normal"):
    children = [
        v.CardTitle(children=[label]),
        v.CardText(children=[str(value)], style_='font-size: 24px;'),
    ]
    if delta is not None:
        delta_value = float(delta.split()[0])  
        color = "green" if delta_value >= 0 else "red" if delta_color == "normal" else "gray"
        delta_text = f"{'↑' if delta_value >= 0 else '↓'} {delta}"
        children.append(v.CardText(style_="color: " + color, children=[delta_text]))
    
    card = v.Card(children=children)
    return card


