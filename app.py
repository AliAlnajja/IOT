from dash import Dash, html, Input, Output, dcc, ctx
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Freenove_DHT as DHT
from time import sleep # Import the sleep function from the time module
import dash_daq as daq
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED=17 
DHTPin=17
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
dht = DHT.DHT(DHTPin) #create a DHT class object    
chk = dht.readDHT11()

app = Dash(__name__)

app.layout = html.Div([
    html.Button(id='btn-nclicks-1', n_clicks=0),
    # html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    # html.Div(id='container-button-timestamp')
    html.Div([
    daq.Gauge(
        # id='my-gauge-1',
        label="Default",
        value=dht.temperature
    ),
    ]),
])

@app.callback(
    Output('btn-nclicks-1', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    # Output('my-thermometer-1', 'value'),
    # Input('thermometer-slider-1', 'value'),
    # Input('btn-nclicks-2', 'n_clicks'),
)

# @app.callback(Output('my-gauge-1', 'value'))

# @app.callback(
#     Output('my-thermometer-1', 'value'),
#     Input('thermometer-slider-1', 'value'),
#     # Input('btn-nclicks-2', 'n_clicks'),
# )

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

def update_output(value):
    return value


# def update_thermometer(value):
    
#         return value,
    # return value

     

if __name__ == '__main__':
    app.run_server(debug=True)
