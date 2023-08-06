

# Import modules
import csv
from random import randrange
import pathlib
import os
import requests
import sys
import random
import urllib

import time
# import play_sound

# First get the absolute path of this file. 
file_dir_path = pathlib.Path(__file__).parent.absolute()
from scrapper import send_email, play_sound

# The 'Data' folder which contains the user_agents.csv can be found relative to this path
csv_file_path = os.path.join(file_dir_path,"Data/","user_agents.csv")

# This function first loads a csv file containing user_agents and then returns a random one from them
def get_usr_agnts(path = csv_file_path):
    '''
    This function first loads a csv file containing user_agents and then returns a random one from them
    '''
    try:
        usr_agnts  = list(csv.DictReader(open(path)))
        user_agent = {'User-Agent': usr_agnts[randrange(0,len(usr_agnts)-1)]['user_agent']}
    except Exception as err:
        print("Error while loading user agent file:", err)
        user_agent = ""
    return user_agent


# You can input a list of urls here. This function will randomly hit the URL if random numer generated < probability_threshold. wait_time is waiting time between another hit
def rand_hit_url(url_ls = ["https://www.google.com", "https://www.facebook.com"], probability_threshold = 50, HEADER = "", wait_time = 1.0):
    '''
    You can input a list of urls here. This function will randomly hit the URL if random numer generated < probability_threshold. 
    wait_time is waiting time between another hit
    '''
    # print("length of list is",len(url_ls))
    for (i, url) in enumerate(url_ls):
        rand_num = random.randint(0,100)
        # print(rand_num)
        if(rand_num <= probability_threshold):
            try:
                time.sleep(wait_time)
                r = requests.get(url, headers = HEADER)
                print(f'Status code \t\t {url} \t\t {r.status_code}')
                status = r.status_code
            except Exception as err:
                print(err)
                status = err
            finally:
                return status
            
        else: 
            print(f'Not hit \t\t {url}')
            pass


# print(rand_hit_url(wait_time=3))
# raises alert using emial and/or sound. Check if this works in Windows or not
def raise_alert(alert_using = ['email', 'sound'],email_subject = "Alert Generated", email_mssg = "Execution Completed"):
    '''
    Mention method(s) in which you would like to get alert. First configure the email setup using config file in send_email.py
    '''
    for alrt in alert_using:
        if(alrt == 'sound'):
            # audio_path = os.path.join(file_dir_path,"Audio/",audio_name)
            #### Check if audio file exists or not ###
            play_sound.play_beep()
            # print("alert sounded with", audio_name)
            next
        
        elif(alrt == 'email'):
            send_email.send_mail(email_subject, email_mssg)
            next
        
        else:
            if(type(alert_using) != list):
                print("alert_using is not a list")
                break
            else:
                print("Alert Mechanism not found")
                break

# print(raise_alert(['sound']))