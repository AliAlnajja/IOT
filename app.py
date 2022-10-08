# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, Input, Output, ctx
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED=17 
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

app = Dash(__name__)

app.layout = html.Div([
    html.Button(id='btn-nclicks-1', n_clicks=0),
    # html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    # html.Div(id='container-button-timestamp')
])

@app.callback(
    Output('btn-nclicks-1', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    # Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(clicks):
    # msg = "None of the buttons have been clicked yet"
    if (clicks % 2 == 0): 
        GPIO.output(LED, GPIO.HIGH) # Turn on
        sleep(1) 
        # msg = "LED is ON"
        return html.Img(src = app.get_asset_url('light.png'), width=200, height=200),
        # while True:
    else:
        GPIO.output(LED, GPIO.LOW) # Turn off
        sleep(1) # Sleep for 1 second 
        # msg = "LED is OFF"
        return html.Img(src = app.get_asset_url('lightOff.png'), width= 200, height=200),
        # while True:
    # html.Div(clicks)

import dash_daq as daq
daq.Thermometer(
    value=5,
    label='Current temperature',
    labelPosition='top'
)    

if __name__ == '__main__':
    app.run_server(debug=True)
    
