import dash
from dash import html

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Hello Dash!"),
    html.P("Ứng dụng Dash đơn giản.")
])

server = app.server  # Quan trọng để Render nhận diện

if __name__ == '__main__':
    app.run_server(debug=True)
