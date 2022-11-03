# Imports
from dash import Dash, html, Input, Output, dcc, ctx
import dash_daq as daq
import Database
import Email

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Freenove_DHT as DHT
from time import sleep # Import the sleep function from the time module

SENT = False
FAN_ON = False

# Pi Phase 2 Setup
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED=17 
DHTPin=12
enablePin = 13
leftPin = 19
rightPin = 26
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(enablePin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leftPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rightPin, GPIO.OUT, initial=GPIO.HIGH)
dht = DHT.DHT(DHTPin)    

# initial read of DHT data
dht.readDHT11()

# Main method to facilitate code structuring
def main():
    app = Dash(__name__)
    app.layout = html.Div([

        ## HTML CONTAINERS ##

        # Light Button
        html.Div([
            html.H1("hi"),
            html.Button(html.Img(src = app.get_asset_url('light.png')), id='btn-nclicks-1', n_clicks=0),
        ], className= "light-bulb"),
        
        # Gauges for Temperature and Humidity
        html.Div([
            daq.Gauge(
                id='temp-gauge',
                showCurrentValue=True,
                units="Degrees Celsius",
                label="Temperature",
                value=dht.temperature,
                max=30,
                min=0,
                className="temperature",
            ),
            daq.Gauge(
                id='humidity-gauge',
                showCurrentValue=True,
                units="Water Vapour/Units of Air",
                label="Humidity",
                value=dht.humidity,
                max=100,
                min=0,
                className="humidity",
            ),
            # Interval to update gauges live
            dcc.Interval(
                    id='temp-humidity-intervals',
                    interval=10*1000, # in milliseconds
                    n_intervals=0
            ),
        ]),

        # Fan Button
        html.Div([
            html.Button(id='btn-nclicks-2', n_clicks=0, className= "fan"),
            dcc.Interval(
                id='recieve-email_component',
                interval= 2 * 1000,  # in milliseconds
                n_intervals=0
            ),
            html.Div([
            daq.ColorPicker(
            id='my-color-picker-1',
            label='Color Picker',
            value=dict(hex='#119DFF'),
            className="colors",
            ),
        html.Div(id='color-picker-output-1')
        ], className="rgb"),
        ]),
    ])
    
    app.index_string = '''
    <!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div class="header">
            <h1>IOT DASHBOARD</h1>
            <span>
                <div class="left">
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider round"></span>
                    </label>
                </div>
            </span>
            
        </div>
        <div class="profile">
            <h2>USER PROFILE</h2>
            <img src="/assets/anonymousProfile.png" alt="Avatar">
            <div class="info">
            <p>Username</p>
            </br>
            <p>favorites</p>
            </br>
            <p>Temperature:</p>
            </br>
            <p>Humidity:</p>
            </br>
            <p>Light intensity:</p>
            </div>
        </div> 
        {%app_entry%}
            {%config%}
            {%scripts%}
            {%renderer%}
    </body>
</html>
    '''
    
    ## CALLBACKS ##

    # Callback for turnung the light on and off (Phase 1)
    @app.callback(Output('btn-nclicks-1', 'children'),
                Input('btn-nclicks-1', 'n_clicks'),
    )
    def displayLightClick(clicks):
        if (clicks % 2 == 0):
            GPIO.output(LED, GPIO.HIGH)
            sleep(1)
            return html.Img(src=app.get_asset_url('light.png'), width=200, height=200),
        else:
            GPIO.output(LED, GPIO.LOW)
            sleep(1)
            return html.Img(src=app.get_asset_url('lightOff.png'), width=200, height=200),

    # Callback for updating the temperature gauge
    @app.callback(Output('temp-gauge', 'value'),
                Input('temp-humidity-intervals', 'n_intervals'),
    )
    def updateTemp(value):
        global SENT
        dht.readDHT11()
        value = dht.temperature
        if value > 23 and not SENT: # If temp exceeds 24 degrees Celsius, send email
            send_email("Temperature is High", "Would You like to turn on the fan?\nPlease reply with \'Yes\' or \'No\'.")
            SENT = True
        elif receive_email() and not NOT_REFUSED: # If email is received, with a response of yes, turn on fan
            displayMotorClick(2)
            sleep(5)
            displayMotorClick(1)
        elif value < 22 and FAN_ON: # If temp is below 22 degrees Celsius, turn off fan
            SENT = False
            displayMotorClick(1)
        return value
    
    # Callback for updating the humidity gauge
    @app.callback(Output('humidity-gauge', 'value'),
                  Input('temp-humidity-intervals', 'n_intervals'),
    )
    def updateHumidity(value):
        sleep(0.5)
        value = dht.humidity
        return value

    # Callback for turning the fan on and off
    @app.callback(Output('btn-nclicks-2', 'children'),
                Input('btn-nclicks-2', 'n_clicks'),
    )
    def displayMotorClick(clicks):
        global FAN_ON
        if (clicks % 2 == 0):
            GPIO.output(enablePin, GPIO.HIGH)
            FAN_ON = True
            sleep(1)
            return html.Img(src=app.get_asset_url('motor_on.jpg'), width=200, height=200),
        else:
            GPIO.output(enablePin, GPIO.LOW)
            FAN_ON = False
            sleep(1)
            return html.Img(src=app.get_asset_url('motor_off.jpg'), width=200, height=200),
    
    # RGB Color
    @app.callback(
        Output('color-picker-output-1', 'children'),
        Input('my-color-picker-1', 'value')
    )
    # RGB Color
    def update_output(value):
        return f'The selected color is {value}.'
    
   
    ## RUN SERVER ##
    if __name__ == '__main__':
        app.run_server(debug=True)

main()
