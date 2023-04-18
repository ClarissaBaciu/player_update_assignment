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

import os
import csv
import logging      #to log information for programmer
import requests     #for PUT request
import sys

logging.basicConfig(level=logging.DEBUG) #for logging information

#hardcoded for now, should be configgered for future use
CSV_FILE_NAME = "input_file.csv" #input file nmae
SERVER_URL = "https://temporaryurl.com/" #placeholder for server url

def generateToken():
    """
    Funtion that generates token, should be replaced by an expiring token in the future
    """
    logging.info("Generating authentification token.")
    return "temporary_token"

def parseMacAddresses(filename):
    """
    Parses through CSV file taken as input and returns a list of macAddresses 
    """
    logging.info(f"Parsing file for addresses: {filename}")
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),filename) #join filepath of current directory to filename
    try:
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            next(reader)            #skips header
            macAddresses = [row[0] for row in reader]
            return macAddresses
    except FileNotFoundError:
        logging.error(f"File not found for mac address parsing: {filepath}")
        raise FileNotFoundError() #for testing purposes
    
def parseVersions(filename):
    """
    Parses through the first row to collect each version (assuming each device is getting updated with the same version)
    (subject to change if payload is submitted as a JSON input to the program instead, may be more efficient this way)
    """
    logging.info(f"Parsing file for versions: {filename}")
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)   #join filepath of current directory to filename
    try:
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
        
    except FileNotFoundError:
        logging.error(f"File not found for version parsing: {filepath}")
        raise FileNotFoundError() #for testing purposes 
    

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
    logging.info(f"Sending PUT request: {url}")
    try: 
        response = requests.put(url,headers=header, json=payload)
        return response
    except requests.RequestException:
        logging.error(f"Error while sending request to {url}")
        return None #return none if exception has been raised
    



def updateAllPlayers(filename, serverUrl): 
    """
    Updates all players by parsing for the macAddresses and payload and then calling to updatePlayer() for every address
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
        tdict["version"] = value
        applicationList.append(tdict)

    #corresponds to specified request payload format
    body = {
        "profile": {
            "applications": applicationList 
        }
    }
    
    for macAddress in macAddresses:
        response = updatePlayer(macAddress, body, token, serverUrl)
        if (response is None):
            logging.error(f"Response is inexistant for {macAddress}")
            continue #continue to the next mac address
        logging.info(f'MAC Address: {macAddress} - Status: {response.status_code}')
        if (response.status_code!=200):                        #if response is not 200, log the error and error message
            if response.headers.get('Content-Type') == 'application/json':  #only log if the information is present in the response
                responseDict = response.json()
                logging.error(f'error: {responseDict["error"]}')
                logging.error(f'message: {responseDict["message"]}')





def main():
    if len(sys.argv) != 2:
        logging.error("Please input the following into the command line: python src/tool/player_update.py <server_url>")
        sys.exit(1)
     #getting arguments from command prompt
    server_url = sys.argv[1]
    logging.info(f"Starting update at the following server URL: {server_url}")

    
    updateAllPlayers(CSV_FILE_NAME, server_url)

    

if __name__ == "__main__":
    main()


