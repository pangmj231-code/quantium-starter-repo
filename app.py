import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# 1. Load data
df = pd.read_csv("formatted_output.csv")
# Ensure date column is datetime type for proper sorting
df["date"] = pd.to_datetime(df["date"])
# Sort by date
df = df.sort_values("date")

# 2. Create line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Trend (Before vs After Price Increase)"
)
# Add a vertical reference line marking the price increase date (2021-01-15)
fig.add_vline(x=pd.to_datetime("2021-01-15"), line_width=2, line_dash="dash", line_color="red")
# Add annotation
fig.add_annotation(
    x=pd.to_datetime("2021-01-15"),
    y=df["sales"].max(),
    text="Price Increase (2021-01-15)",
    showarrow=True,
    arrowhead=1
)
# Update axis labels
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x"
)

# 3. Create Dash app layout
app = Dash()

app.layout = html.Div([
    html.H1(
        children="Soul Foods Sales Data Dashboard",
        style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"}
    ),
    dcc.Graph(
        id="sales-trend-chart",
        figure=fig
    )
])

# 4. Run the app
if __name__ == "__main__":
    app.run(debug=True)