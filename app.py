# Imports
from dash import Dash, html, Input, Output, dcc, ctx
import dash_daq as daq
import Email
import Database
import RGB
import MQTT

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Freenove_DHT as DHT
from time import sleep # Import the sleep function from the time module
from datetime import datetime

global thisIntensity

# Global variables
SENT_LIGHT = False
SENT_EMAIL = False
FAN_ON = False

# Pi Phase 2 Setup
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
DHTPin=12
enablePin = 13
leftPin = 19
rightPin = 26
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
            html.Button(html.Img(src = app.get_asset_url('light.png')), id='btn-nclicks-1', n_clicks=0),
        ], className= "light-bulb"),
        
        # Light Intensity slider
        html.Div([
            daq.Gauge(
                id='light-gauge',
                showCurrentValue=True,
                units="Lumens",
                label="Light Intensity",
                # value=thisIntensity,
                value=52,
                max=1024,
                min=0,
                className="light",
            ),
            # Interval to update gauges live
            dcc.Interval(
                    id='light-intervals',
                    interval=3*1000, # in milliseconds
                    n_intervals=0
            ),
        ]),
        
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
            html.Div([
                html.Button(id='btn-nclicks-2', n_clicks=0, className= "fan"),
                dcc.Interval(
                    id='recieve-email_component',
                    interval= 2 * 1000,  # in milliseconds
                    n_intervals=0
                ),  
        ]),

        ]),
        html.Div([
            html.Button('Red Button', id='Red', n_clicks = 0),
        ], className = 'redButton'),  
        html.Div([
            html.Button('Green Button', id='Green', n_clicks = 0),
        ], className = "greenButton"),
        html.Div([
            html.Button('Blue Button', id='Blue', n_clicks = 0),
        ], className = "blueButton"),
        html.Div([
            html.Button('Yellow Button', id='Yellow', n_clicks = 0),
        ], className = "yellowButton"),
        html.Div([
            html.Button('Magenta Button', id='Magenta', n_clicks = 0),
        ], className = "magentaButton"),
        html.Div([
            html.Button('Cyan Button', id='Cyan', n_clicks = 0),
        ], className = "cyanButton"),
        html.Div([
            html.Button('White Button', id='White', n_clicks = 0),
        ], className = "whiteButton"),
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
            <h1>IOT DASHBOARD<IoTlab/termintensity/h1>
            <span>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider round"></span>
                    </label>
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
    
    @app.callback(Output('Red', 'children'),
                Input('Red', 'n_clicks'),
    )
    def redLight(n_clicks):
        if (LIGHT_ON):
            RGB.red()

    @app.callback(Output('Blue', 'children'),
                Input('Blue', 'n_clicks'),
    )
    def blueLight(n_clicks):
        if (LIGHT_ON):
            RGB.blue()
    
    @app.callback(Output('Green', 'children'),
                Input('Green', 'n_clicks'),
    )
    def greenLight(n_clicks):
        if (LIGHT_ON):
            RGB.green()

    @app.callback(Output('Yellow', 'children'),
                Input('Yellow', 'n_clicks'),
    )
    def yellowLight(n_clicks):
        if (LIGHT_ON):
            RGB.yellow()

    @app.callback(Output('Magenta', 'children'),
                Input('Magenta', 'n_clicks'),
    )
    def magentaLight(n_clicks):
        if (LIGHT_ON):
            RGB.magenta()

    @app.callback(Output('Cyan', 'children'),
                Input('Cyan', 'n_clicks'),
    )
    def cyanLight(n_clicks):
        if (LIGHT_ON):
            RGB.cyan()

    @app.callback(Output('White', 'children'),
                Input('White', 'n_clicks'),
    )
    def whiteLight(n_clicks):
        if (LIGHT_ON):
            RGB.white()

     # Callback for updating the light intensity
    @app.callback(Output('light-gauge', 'value'),
                Input('light-intervals', 'n_intervals'),
    )
    def updateLight(value):
        global SENT_LIGHT
        time = datetime.now()
        value = MQTT.lightIntensity
        if value <= 400 and not SENT_LIGHT:
            Email.send_email("Light update", "Light was turned on at " + str(time))
            SENT_LIGHT = True
        elif Email.receive_email():
            displayLightClick(2)
        elif value > 400 and LIGHT_ON: 
            SENT_LIGHT = False
            displayLightClick(1)
        return value
            
    # Callback for turning the light on and off
    @app.callback(Output('btn-nclicks-1', 'children'),
                Input('btn-nclicks-1', 'n_clicks'),
    )
    def displayLightClick(clicks):
        global LIGHT_ON
        if (clicks % 2 == 0):
            RGB.white()
            LIGHT_ON = True
            sleep(1)
            return html.Img(src=app.get_asset_url('light.png'), width=200, height=200),
        else:
            RGB.off()
            LIGHT_ON = False
            sleep(1)
            return html.Img(src=app.get_asset_url('lightOff.png'), width=200, height=200),

    # Callback for updating the temperature gauge
    @app.callback(Output('temp-gauge', 'value'),
                Input('temp-humidity-intervals', 'n_intervals'),
    )
    def updateTemp(value):
        global SENT_EMAIL
        dht.readDHT11()
        value = dht.temperature
        if value > 23 and not SENT_EMAIL: # If temp exceeds 24 degrees Celsius, send email
            Email.send_email("Temperature is High", "Would You like to turn on the fan?\nPlease reply with \'Yes\' or \'No\'.")
            SENT_EMAIL = True
        elif Email.receive_email() and not Email.NOT_REFUSED: # If email is received, with a response of yes, turn on fan
            displayMotorClick(2)
            sleep(5)
            displayMotorClick(1)
        elif value < 22 and FAN_ON: # If temp is below 22 degrees Celsius, turn off fan
            SENT_EMAIL = False
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
    
    ## RUN SERVER ##
    if __name__ == '__main__':
        app.run_server(debug=True)

main()
