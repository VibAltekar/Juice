# COMMAND LINE VERSION (most texting and server stuff has been replaced
# with print statements and/or deleted/commented)

# this is just something I threw together during midterms week during my downtime
# Ideally have an intel edison or RPi connected to the Juicero somehow (I dont have access to juicero API or hardware)
# Basically a way to tell the user what nutritional information they had in their juice
# As well as a way to keep texting back to the server updating it with the
# carbs,protein, calories, and fats consumed at a particular time.
# The user can essentially know how much of their daily intake of a particular
# nutritional element they have consumed in that day.

# EXAMPLE:
# Microcontroller(MCU) texts "you have drank juice X with 10 grams protein -> 20% of daily intake"
# User eats some food and texts back "protein 20"
# MCU respones "You have consumed 60% of your daily protein intake" (10g+20g) / 50g total daily limit
# User eats some food and texts "protein 30"
# MCU responds "you have consumed more than your daily intake"

# To implement text based system (instead of command line), just replace all
# print statements with function "textback()" with the print string as the parameter
# which does the twilio function client.message.create()
import urllib
import bs4
from bs4 import BeautifulSoup
import requests
from twilio import twiml
import os
import time
import sys
import matplotlib
import numpy
from twilio.rest import TwilioRestClient
import socket
from flask import Flask, request, redirect
import twilio.twiml

# Set up flask server on my own terminal and later on VM to test
#app = Flask(serverfor_me) then app.run()

def textback(text):
    resp = twilio.twiml.Response()
    resp.message(str(text))
    return True

def IP_Address():
    IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP.connect(("8.8.8.8", 5000))
    IPval = IP.getsockname()[0]
    IP2 = socket.gethostbyname(socket.gethostname())
    if IP2 == IPval:
        return True
    return False

#On Intel Edison check if ipconfig is set up and working (tendency to disconnect randomly)
def IntelEdisonInit():
    if IP_Address() != True:
        print("Check intel edison connection to server")
    f2 = requests.get("https://localhost:5000/")
    soup = BeautifulSoup(f2.text,"html.parser")
    #scrape responses because of trial Account (NEED TO FIX)
    #Juicero.com seems to give 403 error
    reply = soup.find('span', attrs={'class': 'name'})
    replye = reply.text.strip()
    print(replye)

#attempt to scrape juicero for nutrition information but kept getting 403 error
#come back to later
def scraper():
    juices = ["green-zing","just-greens","sweet-greens","spicy-greens","carrot-beat","sweet-roots","beta-glow","root-renewal"]

    #r  = requests.get("https://www.juicero.com/the-packs/green-zing/)
    for i in juices:
        url  = requests.get("https://www.juicero.com/the-packs/"+ i + "/")
    return False


#class modified slightly for interview to make it command line based incase
#interviewer wants to test it

class NutritionCounter:
    dailyCarb = 310
    dailyProtein = 50
    dailyFats = 70
    dailyCalories = 2250


    def IsCorrect(self):
        print("Is this aspect and value correct? (y/n)")
        inp = input()
        if inp == "y":
            return True
        if inp == "n":
            return main()
        return self.iscorrect()

    def check(self,nutrition):
        if nutrition[0:4] == "carb" or nutrition[0:3] =="cal" or nutrition[0:3] =="pro" or nutrition[0:3] == "fat":
            return nutrition
        print("\nPlease enter again (Carbs or Fat or Protein and the amount)\n")
        #client.messages.create(to = MYNUMBER,from_ = TWILIO_NUMBER, body = "please enter again")
        #textback("please enter again")
        return self.check(input())

    def carbs(self,nutrition,amount):
        if nutrition[0:4] != "carb":
            return
        global dailyCarb
        self.todayscarb += int(amount)
        perc = float((100*float(self.todayscarb)/float(NutritionCounter.dailyCarb)))
        percv = format(perc, '.2f')
        print("You have consumed " + str(percv) + "% of your daily carb intake\n")
        if int(float(percv)) > 100:
            print("You have crossed your daily intake!\n")
        return self.calories()

    def proteins(self,nutrition,amount):
        if nutrition[0:3] != "pro":
            return
        global dailyProtein
        self.todayspro += int(amount)
        perc = float((100*float(self.todayspro)/float(NutritionCounter.dailyProtein)))
        percv = format(perc, '.2f')
        print("You have consumed " + str(percv) + "% of your daily protein intake\n")
        if int(float(percv)) > 100:
            print("You have crossed your daily intake!\n")
        return self.calories()

    def fats(self,nutrition,amount):
        if nutrition[0:3] != "fat":
            return
        global dailyFats
        self.todaysfat += int(amount)
        perc = float((100*float(self.todaysfat)/float(NutritionCounter.dailyFats)))
        percv = format(perc, '.2f')
        print("You have consumed " + str(percv) + "% of your daily fat intake \n")
        if int(float(percv)) > 100:
            print("You have crossed your daily intake! \n")
        return self.calories()

    def calories(self):
        print("And how many calories was meal? \n ")
        x = 1
        while x == 1:
            amount = input()
            if amount.isdigit() == True:
                x = 0
                break
            else:
                print("Please enter an integer\n")

        self.todayscal += int(amount)
        perc = float((100*float(self.todayscal)/float(NutritionCounter.dailyCalories)))
        percv = format(perc, '.2f')
        print("You have consumed " + str(percv) + "% of your daily calorie intake")
        if int(float(percv)) > 100:
            print("You have crossed your daily intake!\n")
        return

    def __init__(self):
        self.todayscarb = 0
        self.todayspro = 0
        self.todaysfat = 0
        self.todayscal = 0
        while True:
            print("--------------------------------------------------------------")
            print("Eat anything? Enter the nutritional aspect and amount in grams\n")
            inp = input()
            str(inp)
            #IsCorrect()
            nutrition = self.check(inp)
            space = nutrition.find(" ")
            if space == -1:
                x = 1
                while x == 1:
                    amount = input("Enter an amount\n")
                    if amount.isdigit() == True:
                        int(amount)
                        x = 0
                        break
                    else:
                        print("Please enter an integer\n")
            else:
                amount = nutrition[space+1:]

            self.carbs(nutrition,amount)
            self.proteins(nutrition,amount)
            self.fats(nutrition,amount)



if __name__ == '__main__':
    #twilio account info. (commented out because on public Github)
    twilaccount_SID = '#####'
    twilaccount_TOKEN = '######'
    twilnumber = "#####"
    mynumber = "######"3
    #client = TwilioRestClient(twilaccount_SID, twilaccount_TOKEN)
    v = NutritionCounter()
    print(IP_Address())
