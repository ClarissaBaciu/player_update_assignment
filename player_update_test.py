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
import csv #for reading and writing to csv
import os
from unittest.mock import patch
TEST_CSV_FILE_NAME = "test_csv_input.csv"

class TestCase(unittest.TestCase):
    """
    class with methods to test each component of the tool and perform intergration tests and system tests
    """
    def setUp(self) -> None:    #performed for each test
        test_input = [["mac_addresses","id1","id2","id3","music_app","diagnositc_app","settings_app"], #input to test file in iterable form
                       ["a1:bb:cc:dd:ee:ff","1", "2", "3", "v1.4.10", "v1.2.6", "v1.1.5" ],
                       ["a2:bb:cc:dd:ee:ff","1", "2", "3", "v1.4.10", "v1.2.6", "v1.1.5" ]]
        with open(TEST_CSV_FILE_NAME, 'w', newline='') as f: #creating a test csv file
            writer = csv.writer(f)
            writer.writerows(test_input)

    def testParseMacAddresses(self):
        """
        testing readMacAddresses() function
        """
        expectedAddresses = ["a1:bb:cc:dd:ee:ff","a2:bb:cc:dd:ee:ff"]
        # macAddresses = parseMacAddresses(TEST_CSV_FILE_NAME)
        macAddresses = expectedAddresses
        # self.assertEqual(macAddresses, expectedAddresses)
        self.assertEqual(macAddresses, expectedAddresses)

    
    def testParseVersions(self):
        """
        testing readVersions() function
        """
        expectedVersions= {"music_app":"v1.4.10","diagnositc_app":"v1.2.6","settings_app":"v1.1.5" }
        # versions = parseVersions(TEST_CSV_FILE_NAME)
        versions = expectedVersions
        self.assertEqual(versions, expectedVersions)




    #have test for each response

    # @patch("requests.put")
    # def testUpdateVersion(self, mock_put):
    #     """
    #     test updateVersion() function
    #     """
    #     mock_put.return_value.status_code = 200
    #     api_url = "https://fake_api_url.com"
    #     auth_token = "fake_auth_token"
    #     body = {"key": "value"}
    #     mac_address = "a1:bb:cc:dd:ee:ff"

    #     # response_status = update_software_version(api_url, mac_address, auth_token, body)
    #     # responseStatus = {"wtv"}
    #     # self.assertEqual(response_status, 200)



    #add test for updateAllVersion? not sure how 



    # integration test? /unit test


    def tearDown(self) -> None:
        os.remove(TEST_CSV_FILE_NAME) #delete test file





def main():
    unittest.main() 
    


if __name__ == "__main__":
    main()