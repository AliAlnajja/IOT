# Imports
from dash import Dash, html, Input, Output, dcc, ctx
import dash_daq as daq

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Freenove_DHT as DHT
from time import sleep # Import the sleep function from the time module

import smtplib
import imaplib
import easyimap as imap

# GLOBAL VARIABLES
EMAIL_ADDRESS = 'noreply.piservice@gmail.com'
PASSWORD = 'bvlg sbug wars xozh'
RECEIVER_ADDRESS = 'tonynadeau03@gmail.com'
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
            html.Button(html.Img(src = app.get_asset_url('light.png')), id='btn-nclicks-1', n_clicks=0),
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
            ),
            daq.Gauge(
                id='humidity-gauge',
                showCurrentValue=True,
                units="Water Vapour/Units of Air",
                label="Humidity",
                value=dht.humidity,
                max=100,
                min=0,
            ),
            # Interval to update gauges live
            dcc.Interval(
                    id='temp-humidity-intervals',
                    interval=5*1000, # in milliseconds
                    n_intervals=0
            ),
        ]),

        # Fan Button
        html.Div([
            html.Button(id='btn-nclicks-2', n_clicks=0),
            dcc.Interval(
                id='recieve-email_component',
                interval= 2 * 1000,  # in milliseconds
                n_intervals=0
            ),
        ]),
    ])

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
        if value > 24 and not SENT: # If temp exceeds 24 degrees Celsius, send email
            send_email("Temperature is High", "Would You like to turn on the fan?\nPlease reply with \'Yes\' or \'No\'.")
            SENT = True
        elif receive_email(): # If email is received, with a response of yes, turn on fan
            displayMotorClick(2)
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

   
    ## RUN SERVER ##
    if __name__ == '__main__':
        app.run_server(debug=True)


## INDEPENDENT PYTHON METHODS ##

# Method to send email
def send_email(subject, body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, PASSWORD)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, RECEIVER_ADDRESS, msg)


# Method to delete email
def delete_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ADDRESS, PASSWORD)

    mail.select("inbox")
    # typ, data = mail.search(None, 'SUBJECT "hello"')  # Filter by subject
    # typ, data = mail.search(None, 'FROM "example@gmail.com"')  # Filter by sender
    # typ, data = mail.search(None, 'SINCE "015-JUN-2020"')  # Filter by date
    typ, data = mail.search(None, "ALL")  # Filter by all

    for num in data[0].split():
        mail.store(num, '+FLAGS', r'(\Deleted)')

    mail.expunge()
    mail.close()
    mail.logout()


# Method to receive email
def receive_email():
    server = imap.connect('imap.gmail.com', EMAIL_ADDRESS, PASSWORD)

    for mail in server.listids():
        email = server.mail(mail)
        response =  (email.title + " " + email.body).lower()
        if "yes" in response:
            delete_email()
            return True
    else:
        server.quit()
        delete_email()
        return False

# Call to main to run the application
main()
