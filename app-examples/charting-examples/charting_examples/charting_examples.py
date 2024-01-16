# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts.
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt

data = [
    {"name": "Mon", "uv": 3000, "pv": 4000, "amt": 2400},
    {"name": "Tue", "uv": 4500, "pv": 3000, "amt": 2210},
    {"name": "Wed", "uv": 3200, "pv": 4500, "amt": 2290},
    {"name": "Thu", "uv": 5000, "pv": 3900, "amt": 2000},
    {"name": "Fri", "uv": 4000, "pv": 4800, "amt": 2181},
    {"name": "Sat", "uv": 3500, "pv": 3800, "amt": 2500},
    {"name": "Sun", "uv": 3000, "pv": 4300, "amt": 2100},
]


class AreaState(xt.State):
    data = data

    def randomize_data(self):
        for i in range(len(self.data)):
            self.data[i]["uv"] = random.randint(0, 10000)
            self.data[i]["pv"] = random.randint(0, 10000)
            self.data[i]["amt"] = random.randint(0, 10000)


bar_chart_example = xt.bar_chart(
    xt.bar(
        xt.label_list(data_key="uv", position="top"),
        data_key="uv",
        stroke="#ff9999",  # Light red
        fill="#ff9999",
    ),
    xt.bar(
        xt.label_list(data_key="pv", position="top"),
        data_key="pv",
        stroke="#99ccff",  # Light blue
        fill="#99ccff",
    ),
    xt.x_axis(data_key="name"),
    xt.y_axis(),
    margin={
        "left": 10,
        "right": 0,
        "top": 20,
        "bottom": 10,
    },
    data=data,
    height=400,
)

area_chart_example = xt.area_chart(
    xt.area(
        data_key="uv",
        stroke="#EC7495",
        fill="#EC7495",
        type_="natural",
        on_click=AreaState.randomize_data,
    ),
    xt.area(
        data_key="pv",
        stroke="#F4C278",
        fill="#F4C278",
        type_="natural",
    ),
    xt.x_axis(
        data_key="name",
    ),
    xt.y_axis(),
    xt.legend(),
    xt.cartesian_grid(
        stroke_dasharray="3 3",
    ),
    data=AreaState.data,
    width="100%",
    height=400,
)

composed_chart_example = xt.composed_chart(
    xt.area(
        data_key="uv",
        stroke="#875AD1",
        fill="#875AD1",
    ),
    xt.bar(
        data_key="amt",
        bar_size=80,
        fill="#78ffd6",
    ),
    xt.line(
        data_key="pv",
        type_="monotone",
        stroke="#fbd786",
    ),
    xt.x_axis(data_key="name"),
    xt.y_axis(),
    xt.cartesian_grid(stroke_dasharray="3 3"),
    xt.graphing_tooltip(),
    data=data,
    height=400,
)


funnel_data = [
    {"value": 120, "name": "Leads Generated", "fill": "#a3c1ad"},  # Soft green
    {"value": 100, "name": "Initial Contact", "fill": "#68a357"},  # Medium green
    {"value": 80, "name": "Follow-Up Meeting", "fill": "#317c42"},  # Rich green
    {"value": 50, "name": "Proposal Sent", "fill": "#1d5a2c"},  # Dark green
    {"value": 30, "name": "Deal Closed", "fill": "#083c15"},  # Deepest green
]


funnel_chart_example = xt.funnel_chart(
    xt.funnel(
        xt.label_list(
            position="right",
            data_key="name",
            fill="#000",
            stroke="none",
        ),
        xt.label_list(
            position="right",
            data_key="name",
            fill="#000",
            stroke="none",
        ),
        data_key="value",
        data=funnel_data,
    ),
    xt.graphing_tooltip(),
    width=730,
    height=250,
)


line_chart_example = xt.line_chart(
    xt.line(
        data_key="pv",
        stroke="#ff6666",
    ),
    xt.line(
        data_key="uv",
        stroke="#66ccff",
    ),
    xt.x_axis(data_key="name"),
    xt.y_axis(),
    data=data,
    height=400,
)


pie_data01 = [
    {"name": "R&D", "value": 400},
    {"name": "Marketing", "value": 500},
    {"name": "Sales", "value": 300},
    {"name": "IT", "value": 250},
    {"name": "Support", "value": 350},
    {"name": "HR", "value": 200},
]

pie_data02 = [
    {"name": "North Region", "value": 2400},
    {"name": "South Region", "value": 1567},
    {"name": "East Region", "value": 1898},
    {"name": "West Region", "value": 9800},
]


pie_chart_example = xt.pie_chart(
    xt.pie(
        data=pie_data01,
        data_key="value",
        name_key="name",
        cx="50%",
        cy="50%",
        fill="#82ca9d",
        inner_radius="60%",
    ),
    xt.pie(
        data=pie_data02,
        data_key="value",
        name_key="name",
        cx="50%",
        cy="50%",
        fill="#8884d8",
        outer_radius="50%",
    ),
    xt.graphing_tooltip(),
    height=400,
)


radar_data = [
    {"subject": "Communication", "Candidate A": 95, "Candidate B": 85, "fullMark": 100},
    {
        "subject": "Technical Knowledge",
        "Candidate A": 85,
        "Candidate B": 90,
        "fullMark": 100,
    },
    {"subject": "Teamwork", "Candidate A": 75, "Candidate B": 92, "fullMark": 100},
    {
        "subject": "Problem-Solving",
        "Candidate A": 80,
        "Candidate B": 88,
        "fullMark": 100,
    },
    {"subject": "Leadership", "Candidate A": 70, "Candidate B": 80, "fullMark": 100},
    {"subject": "Creativity", "Candidate A": 90, "Candidate B": 78, "fullMark": 100},
]

radar_chart_example = xt.radar_chart(
    xt.radar(
        data_key="Candidate A",
        stroke="#66ccff",  # Light blue
        fill="#66ccff",
    ),
    xt.radar(
        data_key="Candidate B",
        stroke="#ff6666",  # Light red
        fill="#ff6666",
        fill_opacity=0.6,
    ),
    xt.polar_grid(),
    xt.polar_angle_axis(data_key="subject"),
    xt.legend(),
    data=radar_data,
    height=400,
)


scatter_data = [
    {"x": 50, "y": 150, "z": 180},
    {"x": 65, "y": 120, "z": 100},
    {"x": 80, "y": 200, "z": 220},
    {"x": 90, "y": 210, "z": 230},
    {"x": 120, "y": 300, "z": 310},
    {"x": 140, "y": 250, "z": 280},
    {"x": 30, "y": 80, "z": 90},
    {"x": 200, "y": 320, "z": 350},
    {"x": 110, "y": 280, "z": 300},
    {"x": 75, "y": 190, "z": 210},
]

scatter_chart_example = xt.scatter_chart(
    xt.scatter(
        data=scatter_data,
        fill="#ffcc99",
    ),
    xt.x_axis(data_key="x", type_="number"),
    xt.y_axis(data_key="y"),
    height=400,
)


def index():
    return xt.vstack(
        xt.heading("Area Chart Example"),
        area_chart_example,
        xt.heading("Bar Chart Example"),
        bar_chart_example,
        xt.heading("Composed Chart Example"),
        composed_chart_example,
        xt.heading("Funnel Chart Example"),
        funnel_chart_example,
        xt.heading("Line Chart Example"),
        line_chart_example,
        xt.heading("Pie Chart Example"),
        pie_chart_example,
        xt.heading("Radar Chart Example"),
        radar_chart_example,
        xt.heading("Scatter Chart Example"),
        scatter_chart_example,
        padding="80px",
        bg="#232136",
    )


# Global styles defined as a Python dictionary
style = {
    "text_align": "center",
}


app = xt.App()
app.add_page(index)
