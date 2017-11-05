import time
import serial
import RPi.GPIO as GPIO
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from subprocess import call

debounce = False



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "8Io3115fUzjdW7rO9LCtoZcaC"
consumer_secret = "49PbEkSmcjn9qFQBqOQqQ4ESFgWhMvEHwdl05IfDr0wf6EGO7g"


# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "926923317038190592-4nX5H1PVQekRaiVromLAVBqg3Ad7NXT"
access_token_secret = "f8yLW6hHnf7J2jIpC02X5iy4WCNQnHYYoP5Y2hkM3EomX"

user_names = ['realDonaldTrump','FoxNews','senrobportman','SenWarren','HillaryClinton','SenSanders','SarahPalinUSA','AnnCoulter','tim38996','wei2gao']
users = []


GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.add_event_detect(21,GPIO.RISING)

ser = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

class StdOutListener(StreamListener):

    def on_status(self, status):
        global ser
        
        if status.author.id_str in users:
            print(status.author.id_str)
            ser.write('twote\n'.encode())
            print(status.text)
            call(["espeak",status.text])
        

    def on_error(self, status):
        print(status)
        



def tweeted(self):
    global debounce
    if not debounce:
        debounce = True
        ser.write('twote'.encode())
        print('twote\r\n')
        debounce = False
    
    
GPIO.add_event_callback(21,tweeted)

if __name__ == '__main__':

    print("ready")
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    for name in user_names:
        user = api.get_user(screen_name = name)
        users.append(str(user.id))

    print(users)
    print(user_names)
    
    stream = Stream(auth, l)
    stream.filter(follow=users,track="")

while True:
    try:
        rcv = ser.readline()
        print(rcv)
    except KeyboardInterrupt:
        break

GPIO.cleanup()
ser.close()


