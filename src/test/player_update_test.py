#!/usr/bin/env python3

"""
Testing script for player_update.py and its interaction with the API. 
"""
__author__ = "Clarissa Baciu"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "clarissa.baciu@mail.mcgill.ca"
__status__ = "Production"

import unittest #for unit tests
from unittest.mock import patch,MagicMock

#temporary fix for the imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tool.player_update import *


class TestCase(unittest.TestCase):
    """
    class with methods to test each component of the tool 
    """
    def setUp(self) -> None:    #performed for each test
        #create test data for request and other tests
        self.testMacAddress1 = "a1:bb:cc:dd:ee:ff"
        self.testMacAddress2 = "a2:bb:cc:dd:ee:ff"
        self.testServerUrl = "https://temporaryurl.com/"
        self.testToken = "temporary_token"
        self.testBody = {"music_app":"v1.4.10", "diagnostic_app": "v1.2.6","settings_app": "v1.1.5"}
        self.testFilename = "input_file.csv"
        self.falseFilename = "inexistant_file.csv"
        self.expectedPayload = {"profile": 
                                {"applications": [
                                    {"applicationId": "music_app","version": "v1.4.10"},
                                    { "applicationId": "diagnostic_app","version": "v1.2.6"},
                                    {"applicationId": "settings_app","version": "v1.1.5" }
                                ] }
                              }


    def testGenerateToken(self):
        """
        test generate token function, implementation should be fixed
        """
        testToken = generateToken()
        """
        self.assertTrue(isValid(token))  #future implementation
        """
        self.assertTrue(testToken)  #just asserting the the token is not null

    def testParseMacAddresses(self):
        """
        testing readMacAddresses() function
        """
        expectedAddresses = ["a1:bb:cc:dd:ee:ff","a2:bb:cc:dd:ee:ff","a3:bb:cc:dd:ee:ff","a4:bb:cc:dd:ee:ff"]
        
        testMacAddresses = parseMacAddresses(self.testFilename)
        self.assertEqual(testMacAddresses, expectedAddresses)

    
    def testParseVersions(self):
        """
        testing readVersions() function
        """
        expectedVersions= {"music_app":"v1.4.10","diagnositc_app":"v1.2.6","settings_app":"v1.1.5" }
        testVersions = parseVersions(self.testFilename)
        self.assertEqual(testVersions, expectedVersions)
        
    def testFailedMacAddressParse(self):
        """
        test that the macAddressParser raises a file not found error when the file has the wrong name
        """
        self.assertRaises(FileNotFoundError,parseMacAddresses,self.falseFilename)  

    def testFailedVersionAddressParse(self):
        """
        test that the versionParser raises a file not found error when the file has the wrong name
        """
        self.assertRaises(FileNotFoundError,parseVersions,self.falseFilename)

    @patch("requests.put")
    def testUpdatePlayer200(self, mock_put):
        """
        test 200 response
        """
        #create mock response for put request
        response_200 = self.expectedPayload #since the request is simply sent back in the response
        mock_response = MagicMock(status_code=200)      #Create a magic mock object to mock PUT response
        mock_response.json.return_value = response_200   #assign response
        mock_put.return_value = mock_response             #assign to mock_put object
        
        response = updatePlayer(self.testMacAddress1, self.testBody, self.testToken, self.testServerUrl) #call function using class attributes
        self.assertEqual(response.status_code, 200)     #verify status code
        self.assertEqual(response.json(), response_200) #verify  body

    @patch("requests.put")
    def testUpdatePlayer401(self, mock_put):
        """
        test 401 response
        """
        #create mock response for put request
        response_401 = {
                    "statusCode": 401,
                    "error": "Unauthorized",
                    "message": "invalid clientId or token supplied"
                    }
        mock_response = MagicMock(status_code=401)      #Create a magic mock object to mock PUT response
        mock_response.json.return_value = response_401   #assign response
        mock_put.return_value = mock_response             #assign to mock_put object
        

        response = updatePlayer(self.testMacAddress1, self.testBody, self.testToken, self.testServerUrl) #call function using class attributes
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), response_401)

    @patch("requests.put")
    def testUpdatePlayer404(self, mock_put):
        """
        Test 404 response
        """
        #create mock response for put request
        response_404 = {
                    "statusCode": 404,
                    "error": "Not Found",
                    "message": "profile of client 823f3161ae4f4495bf0a90c00a7dfbff does not exist"
                    }
        mock_response = MagicMock(status_code=404)      #Create a magic mock object to mock PUT response
        mock_response.json.return_value = response_404  #assign response
        mock_put.return_value = mock_response             #assign to mock_put object
        
        response = updatePlayer(self.testMacAddress1, self.testBody, self.testToken, self.testServerUrl) #call function using class attributes
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), response_404)

    @patch("requests.put")
    def testUpdatePlayer409(self, mock_put):
        """
        Test 409 response
        """
        #create mock response for put request
        response_409 = {
                        "statusCode": 409,
                        "error": "Conflict",
                        "message": "child \"profile\" fails because [child \"applications\" fails because [\"applications\" is required]]"
                     }
                    
        mock_response = MagicMock(status_code=409)      #Create a magic mock object to mock PUT response
        mock_response.json.return_value = response_409  #assign response
        mock_put.return_value = mock_response             #assign to mock_put object
        
        response = updatePlayer(self.testMacAddress1, self.testBody, self.testToken, self.testServerUrl) #call function using class attributes
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), response_409)

    @patch("requests.put")
    def testUpdatePlayer500(self, mock_put):
        """
        Test 500 response
        """
        #create mock response for put request
        response_500 = {
                        "statusCode": 500,
                        "error": "Internal Server Error",
                        "message": "An internal server error occurred"
                        }
                    
        mock_response = MagicMock(status_code=500)      #Create a magic mock object to mock PUT response
        mock_response.json.return_value = response_500  #assign response
        mock_put.return_value = mock_response             #assign to mock_put object
        
        response = updatePlayer(self.testMacAddress1, self.testBody, self.testToken, self.testServerUrl) #call function using class attributes
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), response_500)


    @patch("tool.player_update.parseMacAddresses")
    @patch("tool.player_update.parseVersions")
    @patch("tool.player_update.generateToken")
    @patch("tool.player_update.updatePlayer")
    def testUpdateAllPlayers(self, mockUpdatePlayer, mockGenerateToken, mockParseVersions, mockParseMacAddresses):
        """
        function to update all players
        """
        #setting all return values for mocks
        mockUpdatePlayer.return_value = MagicMock(status_code=200)
        mockGenerateToken.return_value = self.testToken
        mockParseVersions.return_value = self.testBody
        mockParseMacAddresses.return_value = [self.testMacAddress1, self.testMacAddress2]

        updateAllPlayers(self.testFilename,self.testServerUrl) #call function

        #assert that all functions were called with the correct arguments
        mockParseMacAddresses.assert_called_with(self.testFilename)
        mockParseVersions.assert_called_with(self.testFilename)
        mockGenerateToken.assert_called()
        mockUpdatePlayer.assert_called_with(self.testMacAddress2, self.expectedPayload,mockGenerateToken.return_value,self.testServerUrl) #only check for last address
        self.assertEqual(mockUpdatePlayer.call_count,2)#    check that updatePlayer was called twice 



def main():
    unittest.main() #run all unit tests
    


if __name__ == "__main__":
    main()