# app.py
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import datetime

# Sample dynamic data
def get_data():
    now = datetime.datetime.now()
    df = pd.DataFrame({
        "Time": [now - datetime.timedelta(minutes=i) for i in range(10)],
        "Value": [i * 2 for i in range(10)]
    })
    return df

app = dash.Dash(__name__)
server = app.server  # ← Quan trọng cho Render

app.layout = html.Div([
    html.H1("Dash App trên Render"),
    dcc.Graph(id="graph"),
    dcc.Interval(id="interval", interval=5 * 1000, n_intervals=0)
])

@app.callback(
    dash.Output("graph", "figure"),
    dash.Input("interval", "n_intervals")
)
def update_graph(n):
    df = get_data()
    fig = px.line(df, x="Time", y="Value", title="Giá trị cập nhật theo thời gian")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
