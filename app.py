# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, Input, Output, ctx

app = Dash(__name__)

app.layout = html.Div([
    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
    html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    html.Div(id='container-button-timestamp')
])

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(btn1, btn2):
    msg = "None of the buttons have been clicked yet"
    if "btn-nclicks-1" == ctx.triggered_id:
        msg = "Button 1 was most recently clicked"
    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "Button 2 was most recently clicked"
    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)