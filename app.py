# Imports
from dash import Dash, html, Input, Output, dcc, ctx
import dash_daq as daq

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Freenove_DHT as DHT
from time import sleep # Import the sleep function from the time module

import smtplib
import imaplib
import easyimap as imap

EMAIL_ADDRESS = 'noreply.piservice@gmail.com'
PASSWORD = 'bvlg sbug wars xozh'
RECEIVER_ADDRESS = EMAIL_ADDRESS
SENT = False

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
LED=17 
DHTPin=17
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
dht = DHT.DHT(DHTPin) #create a DHT class object    

# Motor1 = 27
# Motor2 = 18
# Motor3 = 22
# GPIO.setup(Motor1, GPIO.OUT)
# GPIO.setup(Motor2, GPIO.OUT)
# GPIO.setup(Motor3, GPIO.OUT)

dht.readDHT11()

def main():
    app = Dash(__name__)
    app.layout = html.Div([
        # html.Button(id='btn-nclicks-1', n_clicks=0),
        # html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
        # html.Div(id='container-button-timestamp')
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
        dcc.Interval(
                id='interval-component',
                interval=5*1000, # in milliseconds
                n_intervals=0
        ),
        ]),
        html.Div([
            daq.Gauge(
            id='humidity-gauge',
            showCurrentValue=True,
            units="Degrees Celsius",
            label="Humidity",
            value=dht.humidity,
            max=100,
            min=0,
        ),
        dcc.Interval(
                id='interval-components',
                interval=5*1000, # in milliseconds
                n_intervals=0
        ),
        ]),
        # html.Div([
        # dict(
        #     id="fan-img"
        #     source=fan_image,
        #     width=200,
        #     height=200,)
        # ),
        # dcc.Interval(
        #         id='interval-components',
        #         interval=5*1000, # in milliseconds
        #         n_intervals=0
        # ),
    ])


    @app.callback(Output('temp-gauge', 'value'),
                Input('interval-component', 'n_intervals'),
    )

    @app.callback(Output('humidity-gauge', 'value'),
                Input('interval-components', 'n_intervals'),
    )
    def updateTemp(value):
        global SENT
        dht.readDHT11()
        value = dht.temperature
        if value > 24 and not SENT:
            send_email("Temperature is High", "Would You like to turn on the fan?\nPlease reply with \'Yes\' ot \'No\'.")
            SENT = True
        return value

    # @app.callbacl(Output('fan-img', 'source'),
    #             Input('interval-compomemts', 'n_intervals'),
    # )

    # Method to turn fan on or off based on user input with image output
    # def control_motor(response): #need to parse email response for yes or no
    #     if receive_email() == "yes":
    #         GPIO.output(Motor1, GPIO.HIGH)
    #         GPIO.output(Motor2, GPIO.LOW)
    #         GPIO.output(Motor3, GPIO.HIGH)
    #         fan_image = html.Img(src = app.get_asset_url('motor_on.jpg'), width=200, height=200)
    #         return fan_image
    #     else:
    #         GPIO.output(Motor1, GPIO.LOW)
    #         GPIO.output(Motor2, GPIO.LOW)
    #         GPIO.output(Motor3, GPIO.LOW)
    #         fan_image = html.Img(src = app.get_asset_url('motor_off.jpg'), width=200, height=200)
    #         return fan_image


    
    '''
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
    '''

    if __name__ == '__main__':
        app.run_server(debug=True)

def send_email(subject, body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, PASSWORD)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, RECEIVER_ADDRESS, msg)


def receive_email():
    server = imap.connect('imap.gmail.com', EMAIL_ADDRESS, PASSWORD)

    for mail in server.listids():
        email = server.mail(mail)
        print(email.sender)
        print(email.date)
        print(email.title)
        print(email.from_addr)
        print(email.body)
        # response = email.title
        # response += email.body
        # response = response.lower()
        # return response
    else:
        server.quit()


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
    print("Successfully deleted email")

    mail.expunge()
    mail.close()
    mail.logout()

main()