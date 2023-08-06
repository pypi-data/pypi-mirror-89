# Getting started

API for Markdown Notes app.

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=MdNotes-Python)


## How to Use

The following section explains how to use the MdNotesRopc SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=MdNotes-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=MdNotes-Python&projectName=md_notes_ropc)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=MdNotes-Python&projectName=md_notes_ropc)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=MdNotes-Python&projectName=md_notes_ropc)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from md_notes_ropc.md_notes_ropc_client import MdNotesRopcClient
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=MdNotes-Python&libraryName=md_notes_ropc.md_notes_ropc_client&projectName=md_notes_ropc&className=MdNotesRopcClient)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=MdNotes-Python&libraryName=md_notes_ropc.md_notes_ropc_client&projectName=md_notes_ropc&className=MdNotesRopcClient)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| o_auth_client_id | OAuth 2 Client ID |
| o_auth_client_secret | OAuth 2 Client Secret |
| o_auth_username | OAuth 2 Resource Owner Username |
| o_auth_password | OAuth 2 Resource Owner Password |



API client can be initialized as following.

```python
# Configuration parameters and credentials
o_auth_client_id = 'o_auth_client_id' # OAuth 2 Client ID
o_auth_client_secret = 'o_auth_client_secret' # OAuth 2 Client Secret
o_auth_username = 'o_auth_username' # OAuth 2 Resource Owner Username
o_auth_password = 'o_auth_password' # OAuth 2 Resource Owner Password

client = MdNotesRopcClient(o_auth_client_id, o_auth_client_secret, o_auth_username, o_auth_password)
```


You must now authorize the client.

### Authorizing your client

This SDK uses *OAuth 2.0 authorization* to authorize the client.

The `authorize()` method will exchange the user's credentials for an *access token*.
The access token is an object containing information for authorizing client requests and refreshing the token itself.

You must pass the *[scopes](#scopes)* for which you need permission to access.

```python
try:
    client.auth.authorize(scope=[OAuthScopeEnum.NOTES_READ])
except OAuthProviderException as ex:
    # handle exception
```

The client can now make authorized endpoint calls.

### Scopes

Scopes enable your application to only request access to the resources it needs while enabling users to control the amount of access they grant to your application. Available scopes are defined in the `md_notes_ropc.models.o_auth_scope_enum.OAuthScopeEnum` enumeration.

| Scope Name | Description |
| --- | --- |
| `NOTES_READ` | Notes read access |

### Refreshing token

An access token may expire after some time. To extend its lifetime, you must refresh the token.

```python
if client.auth.token_expired():
    try:
        client.auth.refresh_token()
    except OAuthProviderException as ex:
        # handle exception
```

If a token expires, the SDK will attempt to automatically refresh the token before the next endpoint call requiring authentication.

### Storing an access token for reuse

It is recommended that you store the access token for reuse.

You can store the access token in a file or a database.

```python
# store token
save_token_to_database(client.config.o_auth_token)
```
 
However, since the the SDK will attempt to automatically refresh the token when it expires, it is recommended that you register a *token update callback* to detect any change to the access token.

```python
client.config.o_auth_callback = save_token_to_database
```

The token update callback will be fired upon authorization as well as token refresh.

### Creating a client from a stored token

To authorize a client from a stored access token, just set the access token after creating the client:

```python
client = MdNotesRopcClient()
client.config.o_auth_token = load_token_from_database()
```

### Complete example

```python
from md_notes_ropc.md_notes_ropc_client import MdNotesRopcClient
from md_notes_ropc.models.o_auth_scope_enum import OAuthScopeEnum
from md_notes_ropc.exceptions.o_auth_provider_exception import OAuthProviderException

# function for storing token to database
def save_token_to_database(token):
    # code to save the token to database

# function for loading token from database
def load_token_from_database():
    # load token from database and return it (return None if no token exists)

# Configuration parameters and credentials
o_auth_client_id = 'o_auth_client_id' # OAuth 2 Client ID
o_auth_client_secret = 'o_auth_client_secret' # OAuth 2 Client Secret
o_auth_username = 'o_auth_username' # OAuth 2 Resource Owner Username
o_auth_password = 'o_auth_password' # OAuth 2 Resource Owner Password

#  create a new client
client = MdNotesRopcClient(o_auth_client_id, o_auth_client_secret, o_auth_username, o_auth_password)

# callback for storing token for reuse when token is updated
client.config.o_auth_callback = save_token_to_database

# obtain access token, needed for client to be authorized
previous_token = load_token_from_database()
if previous_token:
    # restore previous access token
    client.config.o_auth_token = previous_token
else:
    # obtain new access token
    try:
        client.auth.authorize([OAuthScopeEnum.NOTES_READ])
    except OAuthProviderException as ex:
        # handle exception

# the client is now authorized and you can use controllers to make endpoint calls
# client will automatically refresh the token when it expires and call the token update callback
```


# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [ServiceController](#service_controller)
* [UserController](#user_controller)

## <a name="service_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ServiceController") ServiceController

### Get controller instance

An instance of the ``` ServiceController ``` class can be accessed from the API Client.

```python
 service_controller = client.service
```

### <a name="get_status"></a>![Method: ](https://apidocs.io/img/method.png ".ServiceController.get_status") get_status

> TODO: Add a method description

```python
def get_status(self)
```

#### Example Usage

```python

result = service_controller.get_status()

```


[Back to List of Controllers](#list_of_controllers)

## <a name="user_controller"></a>![Class: ](https://apidocs.io/img/class.png ".UserController") UserController

### Get controller instance

An instance of the ``` UserController ``` class can be accessed from the API Client.

```python
 user_controller = client.user
```

### <a name="get_user"></a>![Method: ](https://apidocs.io/img/method.png ".UserController.get_user") get_user

> TODO: Add a method description

```python
def get_user(self)
```

#### Example Usage

```python

result = user_controller.get_user()

```


[Back to List of Controllers](#list_of_controllers)



