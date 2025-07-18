import dash
from dash import html, dcc, Input, Output, State, MATCH, Patch, callback, ALL, callback_context, ctx
from dash.exceptions import PreventUpdate
import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False)

# Khởi tạo app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # để deploy lên Render

app.layout = html.Div([
    html.H1("📝 To-Do List App"),
    dcc.Input(id='new-task', type='text', placeholder='Thêm task mới'),
    html.Button('Thêm', id='add-button', n_clicks=0),
    html.Hr(),
    html.Div(id='task-list'),
])

# ------------------------
# Add new task
@callback(
    Output('task-list', 'children'),
    Input('add-button', 'n_clicks'),
    State('new-task', 'value'),
)
def add_task(n_clicks, new_task):
    tasks = load_tasks()

    if new_task:
        tasks.append(new_task.strip())
        save_tasks(tasks)

    children = [
        html.Div([
            html.Span(task),
            html.Button('❌', id={'type': 'delete-button', 'index': i}, n_clicks=0, style={'marginLeft': '10px'})
        ]) for i, task in enumerate(tasks)
    ]

    return children

# # ------------------------
# # Delete task
@callback(
    Output('task-list', 'children', allow_duplicate=True),
    Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
    # State('task-store', 'data'),
    prevent_initial_call="initial_duplicate",
)
def delete_task(n_clicks_list):
    print(n_clicks_list)
    if sum(n_clicks_list) == 0:
        raise PreventUpdate
    else:
        tasks = load_tasks()
        
        triggered_id = ctx.triggered_id
        if not isinstance(triggered_id, dict):
            raise PreventUpdate

        idx = triggered_id.get('index')
        if isinstance(idx, int) and 0 <= idx < len(tasks):
            tasks.pop(idx)
            save_tasks(tasks)

        children = [
            html.Div([
                html.Span(task),
                html.Button('❌', id={'type': 'delete-button', 'index': i}, n_clicks=0, style={'marginLeft': '10px'})
            ]) for i, task in enumerate(tasks)
        ]

        return children

if __name__ == '__main__':
    app.run(debug=True)
