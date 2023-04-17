# Player Developer Tech Assignment


This project involves creating a production-ready tool that facilitates the update of thousands of music players simultaneously. It does so by using an API that sends PUT requests to a server that the music players query every 15 minutes to see if a new update has presented itself. The tool takes one CSV file as input, which contains the MAC addresses for each music player, and it then outputs the HTTP request.


# Table of Contents
1. [Request Format](#request-format)
2. [Requirements](#requirements)
3. [Assumptions and Design Decisions](#assumptions-and-design-decisions)
4. [User Documentation](#user-documentation)
5. [Developper Documentation](#developper-documentation)
6. [Future Improvements](#future-improvements)




## Request Format

#### Request

```
Headers
Content-Type: application/json
x-client-id: required
x-authentication-token: required
Body
{
  "profile": {    
    "applications": [
      {
        "applicationId": "music_app"
        "version": "v1.4.10"
      },
      {
        "applicationId": "diagnostic_app",
        "version": "v1.2.6"
      },
      {
        "applicationId": "settings_app",
        "version": "v1.1.5"
      }
    ]
  }
}
```



## Requirements
- The project should be compatible with all operating systems.
- Only one CSV file can be used as input to the tool. 
- The CSV file contains, at minimum, a column for the MAC addresses, always in the first column.
- All client-IDs should be unique for each device.


## Assumptions and Design Decisions

- Python was chosen for the assignment as it is compatible with all operating systems and allows an intuitive implementation of REST APIs.

- The client-ID will be the MAC address of each device as they are unique for each client.

- For the time being, the token is a hardcoded string. In the next stage, the token will have to be replaced with a time dependant token, and a test function will have to be written to ensure the token is still valid after a certain period.

- Since each player is querying simultaneously for a new version, we are assuming all player applications are getting updated with the same version. Therefore, only the first row of the CSV file is parsed.

- The CSV file is assumed to be in the same folder and the filename is currently hardcoded into the main script. It was not added as an argument as the assignment specified that only one CSV file could be used as an input.

- Because only one input was permitted, no additional input was added for the payload of the request. Therefore, the app names and version numbers were added as columns to the CSV file and parsed in the main script. 





## User Documentation

1. Make sure Python is installed on your computer. Otherwise it can be retrieved on the Python official [download](https://www.python.org/downloads/) page.

2. Open terminal and run the following command : ```python3 -m pip install requests``` to install the requests library.

3. Download or clone this repository ```git clone git@github.com:ClarissaBaciu/player_update_assignment.git ```.

4. Navigate to the project folder.

3. Make sure to have the following information on hand: mac addresses for each device to update, the application names and version numbers, and the server URL. Create a CSV file like the following and save it as *input_file.csv*:


### input_file.csv
```
mac_addresses,     id1,    id2,     id3,    music_app,  diagnositc_app, settings_app
a1:bb:cc:dd:ee:ff,  1,      2,       3,     v1.4.10,        v1.2.6,         v1.1.5
a2:bb:cc:dd:ee:ff,  1,      2,       3,     v1.4.10,        v1.2.6,         v1.1.5
a3:bb:cc:dd:ee:ff,  1,      2,       3,     v1.4.10,        v1.2.6,         v1.1.5
a4:bb:cc:dd:ee:ff,  1,      2,       3,     v1.4.10,        v1.2.6,         v1.1.5
```

4. Make sure to save the CSV file input in the same folder as the player_update.py file in the src/tool folder.  

5. Run the following script replacing server_url by the appropriate url: ```python src/tool/player_update.py {server_url}```


### Troubleshoot

- If a *File not found* message appears, it signifies the input file has not been named or saved properly.
- If a *Error while handling request* message appears, the API request has not been properly configured which may be attributed to the input being improperly configured or the server url being innacurate.
- If a *Response is inexistant* message appears, there may be a problem with the URL provided.



## Developper Documentation


### Player_update.py
Main program file. Situated in *src > tool*. Can be run as specified in step 5 of the user documentation.

Imports:  
- os library for configuring paths
- csv library for parsing the input csv file
- logging library for loggin error information
- requests library for sending HTTP request
- sys library for retrieving command line arguments

Functions:

```generateToken()```
- Parameters: None
- Output: A token in the form of a string
- Description: The token is used in the header of the request and should expire in real life, for now it is temporarily hardcoded.

```parseMacAddresses(filename)```
- Parameters: CSV file
- Output: List of MAC addresses
- Description: Parses through CSV file taken as input and returns a list of macAddresses.

```parseMacAddresses(filename)```
- Parameters: Input CSV filename
- Output: List of MAC addresses
- Description: Obtains the list of MAC addresses from the first column of the CSV file.


```parseVersions(filename)```
- Parameters: Input CSV filename
- Output: Dictionnary where the keys are the application names and the values are the version numbers
- Description: Searches for the columns for the updated applications and gets all application versions from the first row of the CSV file. Should be replaced by a JSON file in the future.

```updatePlayer(macAddress, payload, token, serverUrl)```
- Parameters: MAC address of the player to update, the payload of the request, the authentification token and the URL of the server we are sending the request to
- Output: The request response
- Description: Creates a header file using the MAC address and authentification token of the current device and sends a PUT request to the URL provided.

```updateAllPlayers(filename, serverUrl)```
- Parameters: Filename of the input CSV file and server URL
- Output: None
- Description: Wrapper function for all other functions. Retrieves MAC addresses, version dictionnary and authentification token from the functions above, configures a body for the request using the format specified in the Request Format section of this document, iterates through the list of MAC addresses and calls updatePlayer() for every device.


### Player_update_test.py

The test script was written before the main tool script. This is a more inutitive approach since the inputs and outputs of each function must be determined from the start. Each unit was tested independantly using the Unittest library and mocks were created to replace nested functions. Situated in *src > test*. Run using the following: ```python src/test/player_update_test.py```.

Imports:  
- Unittest library for configuring unit tests
- Patch and MagickMock from unittest for creating mock return values and mocking API requests 
- All functions from tool.player_update for testing purposes

Class
```TestCase(unittest.TestCase)```
- Inherits from unittest.TestCase and contains methods for testing each function from player_update.py. It also has class attributes for all test parameters.


Functions:

```setUp(self)```
- Description: Function called before every unit test. Specifies all test strings and parameters.

```testGenerateToken(self)```
- Description: Tests that a token has indeed been generated.

```testParseMacAddresses(self)```
- Description: Asserts that the parseMacAddress() function successfully parses through the CSV file and obtains the right MAC addresses.

```testParseVersions(self)```
- Description: Asserts that the parseVersions() function successfully parses through the CSV file and obtains the right application names and version numbers.



```testFailedMacAddressParse(self)```
- Description: Asserts a file not found exception is thrown when the filename is incorrect.


``` testFailedVersionAddressParse(self):```
- Description: Asserts a file not found exception is thrown when the filename is incorrect.

``` testUpdatePlayer200/401/404/409/500(self, mock_put)```
- Description: Mocks the PUT request and asserts that the response for each type has the appropriate status code and JSON. 

```testUpdateAllPlayers(self, mockUpdatePlayer, mockGenerateToken, mockParseVersions, mockParseMacAddresses)```
- Description: Mocks all other functions and asserts that they are called with the appropriate parameters and the appropriate number of times.
















## Future Improvements

- An expirable token generating function should be implemented.

- Coming from a C and Java background, CamelCase was chosen as the naming convention. In the future, underscore could be used for more compatibility with Python's build-in functions. 

- It would optimize complexity and efficiency to add the payload as a separate input file in the form of a JSON file.  

- Otherwise, instead of adding an input to the function, a GET request could be used to get the current versions of each application from the API and the appropriate application could be updated according to the scope of the update.
