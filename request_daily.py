#Author: Aidan Mellin

import requests
import os
from dotenv import load_dotenv

load_dotenv()
REQ_URL = os.getenv('REQUEST_URL')
TOKEN = os.getenv('TOKEN')
POOL = os.getenv('POOL')

def request():
    
    req = requests.get("https://dailyhealth.rit.edu/")
    post = req.post()
    
request()


"""
Probably have to simulate all steps of process (5 of them)
    All below are GET (type:json)
    dispatch?method=%s&token= 
        getUserInfo
        fetchLatestAssessment
        fetchCheckinsByUser
        logAssessment
        fetchLatestAssessment
    
method=getUserInfo
token=TOKEN
pool=POOL

GET /default/dispatch?method=getUserInfo&token=TOKEN&pool=POOL HTTP/1.1
Host: fnydcwnof2.execute-api.us-east-1.amazonaws.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://dailyhealth.rit.edu/?login=true
Origin: https://dailyhealth.rit.edu
Connection: keep-alive


{"statusCode":200,"header":{"Content-Type":"application/json","Access-Control-Allow-Origin":"*"},"body":{"q0":"no","id":"1f621ef0-90c5-4fd5-bc93-770119d95d81","user":"rit_355003358-atm3232","role":"STUDENT","email":"rit_355003358-atm3232","status":"APPROVED","installation":"RIT","created":1613320365,"created-reverse":-1613320365,"userName":"rit_355003358-atm3232","firstName":"Aidan","lastName":"Mellin"}}

"""