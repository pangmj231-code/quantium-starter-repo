import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# 1. Load and prepare data
df = pd.read_csv("formatted_output.csv")
df["date"] = pd.to_datetime(df["date"])

# 2. Initialize the app
app = Dash()

# 3. Define color palette (using a nice blue palette)
colors = {
    "background": "#f4f6f9",
    "card": "#ffffff",
    "header": "#1e3a5f",
    "text": "#2c3e50",
    "accent": "#3498db",
    "line": "#2e86c1"
}

# 4. Create the app layout
app.layout = html.Div(
    style={
        "backgroundColor": colors["background"],
        "padding": "40px 20px",
        "fontFamily": "Arial, sans-serif",
        "minHeight": "100vh"
    },
    children=[
        # Header
        html.H1(
            children="Soul Foods Sales Dashboard",
            style={
                "textAlign": "center",
                "color": colors["header"],
                "marginBottom": "10px",
                "fontSize": "36px"
            }
        ),
        html.P(
            children="Explore Pink Morsel sales trends by region",
            style={
                "textAlign": "center",
                "color": colors["text"],
                "marginBottom": "30px",
                "fontSize": "18px"
            }
        ),
        # Region selection card
        html.Div(
            style={
                "backgroundColor": colors["card"],
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                "maxWidth": "400px",
                "margin": "0 auto 30px auto"
            },
            children=[
                html.Label(
                    children="Select Region:",
                    style={"fontWeight": "bold", "color": colors["text"], "marginRight": "15px"}
                ),
                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": " All", "value": "all"},
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"}
                    ],
                    value="all",
                    inline=True,
                    style={"color": colors["text"]}
                )
            ]
        ),
        # Graph
        dcc.Graph(
            id="sales-chart",
            config={"displayModeBar": True},
            style={"backgroundColor": colors["card"], "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"}
        )
    ]
)

# 5. Callback to update chart based on region selection
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):
    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Create line chart
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Trend ({selected_region.capitalize() if selected_region != 'all' else 'All Regions'})"
    )

    # Add vertical line for price increase date
    fig.add_vline(
        x=pd.to_datetime("2021-01-15"),
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top"
    )

    # Update chart layout with custom styling
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": colors["text"], "family": "Arial, sans-serif"},
        title={"font": {"size": 22, "color": colors["header"]}}
    )

    # Update axes styling
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e0e0e0",
        title_font={"size": 14, "color": colors["text"]}
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e0e0e0",
        title_font={"size": 14, "color": colors["text"]}
    )

    return fig

# 6. Run the app
if __name__ == "__main__":
    app.run(debug=True)