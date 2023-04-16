#!/usr/bin/env python3

"""
Python script designed to send PUT requests to an API that enables the update of thousands of music players. 
Takes as input a CSV file and outputs a PUT request.
"""
__author__ = "Clarissa Baciu"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "clarissa.baciu@mail.mcgill.ca"
__status__ = "Production"


import csv
import os           #to find current file path
import logging      #to log information for programmer
import requests     #for PUT request
import json         #to convert dictionnary to json for header/payload body
import jwt

#hardcoded for now, should be configgered for future use
CSV_FILE_NAME = "input_file.csv" #input file nmae
INPUT_FOLDER_NAME = "input"     #folder containing input file(s)
SERVER_URL = "https://temporaryurl.com/" #placeholder for server url

def generateToken():
    """
    Funtion that generates token using HS256 hashing algorithm
    """
    return "abcd"

def parseMacAddresses(filename):
    """
    Parses through CSV file taken as input and returns a list of macAddresses 
    """
    filepath = os.path.join(os.path.dirname(__file__),INPUT_FOLDER_NAME,filename) #joins path to input directory to filename
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        next(reader)            #skips header
        macAddresses = [row[0] for row in reader]
    return macAddresses

def parseVersions(filename):
    """
    Parses through the first row to collect each version (assuming each device is getting updated with the same version)
    (subject to change if payload is submitted as a JSON input to the program instead, may be more efficient this way)
    """
    filepath = os.path.join(os.path.dirname(__file__),INPUT_FOLDER_NAME,filename) #joins path to input directory to filename
    with open(filepath, newline='') as f:
        reader = csv.reader(f)   
        header = next(reader)   #retrieve header
        #enumerate returns a tupple containing the index and column name
        #only selecting for columns that have the app substring since it means it is an app whose version needs to updated
        selectedCol = [(index,colName) for index,colName in enumerate(header) if "app" in colName] 
        firstRow = next(reader) #retrieve the first row
        versionDict = {} #return dictionnary
        for index,colName in selectedCol:
            versionDict[colName] = firstRow[index]  #column name = key, version number = value
        return versionDict

def updatePlayer(macAddress, payload, token, serverUrl): 
    """
    Sends PUT request to update one player object, takes as input the specific macAddress, the payload (body of the request)
    """
    #since every header is specific to the player, create header in this function
    header = {
        "Content-Type" : "applicatino/json",
        "x-client-id" : macAddress,         #let client id = macAddress since it is unique for every device
        "x-authentication-token" : token,
    }
    url = f"{serverUrl}/profiles/clientId:{macAddress}"
    response = requests.put(url,headers=header, json=payload)
    
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())




def updateAllPlayers(filename, serverUrl): 
    """
    Updates all players by parsing for the macAddresses and payload and then calling to updatePlayre() for every address
    Takes filename for input csv file and server url as input
    """
    macAddresses = parseMacAddresses(filename)
    versionDict = parseVersions(filename)
    token = generateToken()
    

    #configure version dictionnary to match json format

    #create list of dictionnaries to match value attribute to "applications" key in body
    applicationList = []
    for key,value in versionDict.items():
        tdict = {}   #temporary dictionnary to hold items
        tdict["applicationId"] = key
        tdict["versions"] = value
        applicationList.append(tdict)

    body = {
        "profile": {
            "applications": applicationList 
        }
    }


    for macAddress in macAddresses:
        responseStatus = updatePlayer(macAddress, body, token, serverUrl)
        print(f'MAC Address: {macAddress} - Update status: {responseStatus}')


    


  



def main():
    updateAllPlayers(CSV_FILE_NAME, SERVER_URL)

    

if __name__ == "__main__":
    main()



# # Making a PUT request
# r = requests.put('https://httpbin.org / put', data ={'key':'value'})
 
# # check status code for response received
# # success code - 200
# print(r)
 
# # print content of request
# print(r.content)

