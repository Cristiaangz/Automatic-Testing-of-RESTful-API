import pytest
import requests
import json
import datetime
import sys
import random
import os.path


@pytest.fixture(scope='session')
def main_url():
    """A simple pytest fixture that returns the main url of the resources being tested."""
    return "https://gorest.co.in"

@pytest.fixture(scope='session')
def user_endpoint():
    """A simple pytest fixture that returns the URL of the users resource."""
    return "https://gorest.co.in/public-api/users"

@pytest.fixture(scope='session')
def timeout_threshold():
    """A simple pytest fixture that returns the minimum performance expected from an HTTP method."""
    return 1.000

@pytest.fixture(scope='session')
def valid_payload():
    """A simple pytest fixture that returns a dictionary for a valid payload to the users endpoint."""
    payload = {
        "name": "Dan Doney",
        "email": "dan@safemoney.com",
        "gender" : "Male",
        "status" : "Active"
    }
    return payload

@pytest.fixture(scope='session')
def missing_value_payload():
    """A simple pytest fixture that returns a dictionary for a payload to the users endpoint a one missing category."""
    payload = {
        "name": "Patrick Campos",
        "email": "pat@safemoney.com",
        "gender" : "Male"
    }
    return payload

@pytest.fixture(scope='session')
def invalid_value_payload():
    """A simple pytest fixture that returns a dictionary for a payload to the users endpoint with an unaccounted gender field."""
    payload = {
        "name": "John Doe",
        "email": "john@safemoney.com",
        "gender" : "Nonbinary",
        "status" : "Active"
    }
    return payload

@pytest.fixture(scope='session')
def invalid_datatype_payload():
    """A simple pytest fixture that returns a dictionary for a payload to the users endpoint with an unaccounted status field."""
    payload = {
        "name": "Jeff Truitt",
        "email": "jeff@safemoney.com",
        "gender" : "Male",
        "status" : 1,
    }
    return payload

@pytest.fixture(scope='session')
def token():
    """A simple pytest fixture that returns the bearer token needed for some HTTP requests."""
    if os.path.isfile("token.txt"):
        f = open("token.txt", "r")
        token = f.readline()
        f.close()
        return token
    else:
        pytest.exit('Token file not found. Hint: run setup.py again')

@pytest.fixture(scope='session')
def invalid_token():
    """A simple pytest fixture that returns an invalid bearer token."""
    return '90a5606d1cc51be7d824fdd9c19201273b890961e8e4720d8045b9476de020da'

def is_id(id):
    """A simple function that returns if the value is a valid ID datatype."""
    # Valid ID must be a non-negative integer
    return isinstance(id, int) and id > 0


def is_name(name):
    """A simple function that returns if the value is a valid name datatype."""
    # Valid name must be a non-empty string
    return isinstance(name, str) and len(name) > 0

def is_email(email):
    """A simple function that returns if the value is a valid email datatype."""
    # Valid email must be a string containting '@' and lenght greater than 4 (min email: x@y.z)
    return isinstance(email, str) and len(email) >= 5 and ('@' in email)


def is_gender(gender):
    """A simple function that returns if the value is a valid gender datatype."""
    # Valid gender must be a string either 'Male' or 'Female'
    return isinstance(gender, str) and gender == 'Male' or gender == 'Female'


def is_status(status):
    """A simple function that returns if the value is a valid status datatype."""
    # Valid status must be a string either 'Active' or 'Inactive'
    return isinstance(status, str) and status == 'Active' or status == 'Inactive'


def is_time(time):
    """A simple function that returns if the value is a valid time datatype."""
    try:
        # Valid time must be a string that can be turned into an datetime object.
        datetime.datetime.fromisoformat(time)
        return True
    except ValueError:
        return False

def is_proper_json(response):
    """A simple function that safely converts a response into a dictionary and returns it. Returns False if it fails"""
    try:
        # Valid JSON will convert by .json() method
        return response.json()
        
    except json.JSONDecodeError:
        return False


def is_user_datatypes(user):
    """A simple function that checks if all datatypes from GET response dictionary are valid"""
    # Checks all parameters for a user dictionary
    return all([
        is_id(user['id']),
        is_name(user['name']),
        is_email(user['email']),
        is_gender(user['gender']),
        is_status(user['status']),
        is_time(user['created_at']),
        is_time(user['updated_at'])
    ])

def is_same_response(response1, response2):
    """A simple function that checks if two responses are exactly the same"""
    response1_dict = is_proper_json(response1)
    response2_dict = is_proper_json(response2)
    if response1_dict != False and response2_dict != False:
        # Converts response JSONs into string form and verifies they are equal.
        return str(response1_dict) ==  str(response2_dict)
    else:
        assert 0
        return False

def same_user(response_1_dict, response_2_dict):
    """A simple function that returns if two user dictionaries have the same mandatory values"""
    # Converts response JSONs into string form and verifies they are equal.
    return all([
        response_1_dict['name'] ==  response_2_dict['name'],
        response_1_dict['email'] ==  response_2_dict['email'],
        response_1_dict['gender'] ==  response_2_dict['gender'],
        response_1_dict['status'] ==  response_2_dict['status'],
    ])

def user_resource_exists(url):
    """A simple function that confirms if url points to a an existing resource"""
    response = requests.get(url)
    return response.status_code == requests.codes.ok

def user_resource_delete(url, token):
    """A simple function that deletes resource at url. Returns true if successful."""
    access_token_header = "Bearer " + token
    response = requests.delete(
        url = url,
        headers={"Authorization": access_token_header}
    )
    return response.status_code == requests.codes.ok

def verify_email_free(url, email):
    """A simple function that returns if an email address is free."""
    print("\nVerifying if {} exists".format(email))
    response = requests.get(url, params={'email': email})
    if response.status_code == requests.codes.ok:
        print("GET method successful")
        try:
            response_dict = response.json()
            if response_dict['meta']['pagination']['total'] != 1:
                print('{} is free'.format(email))
                return True
            elif response_dict['data'][0]['email'] == email:
                return False
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            return False
    else:
        print("GET method was unsuccessful ({})".format(response.status_code))
        return None

def make_email_free(url, email, token):
    """A function that ensures an email address is free in the database. Returns True if successful."""
    print("\nVerifying if {} exists".format(email))
    response = requests.get(url, params={'email': email})
    if response.status_code == requests.codes.ok:
        print("GET method successful")
        try:
            response_dict = response.json()
            if response_dict['meta']['pagination']['total'] != 1:
                print('{} is free'.format(email))
                return True
            elif response_dict['data'][0]['email'] == email:
                print('Result found {}. Attempting to delete'.format(response_dict['data'][0]['email']))
                user_id = response_dict['data'][0]['id']
                user_url = url + '/{}'.format(user_id)
                return user_resource_delete(url = user_url, token=token)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            return False
    else:
        print("GET method was unsuccessful ({})".format(response.status_code))
        return False

def make_resource_empty(url, token):
    """A function that ensures a resource is empty in the database. Returns True if successful."""
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        try:
            response_dict = response.json()
            if response_dict['code'] == requests.codes.not_found:
                print('\n{} is free'.format(url))
                return True
            else:
                print('\nResult found. Attempting to delete')
                return user_resource_delete(url = url, token = token)
        except:
            print ("\nUnexpected error:", sys.exc_info()[0])
            return False
    else:
        print("\nGET method was unsuccessful ({})".format(response.status_code))
        return False

def correct_empty_payload(received_payload):
    """A simple function that returns if the received payload dictionary corresponds to expected error messages."""
    expected = [
        {'field': 'email','message': "can't be blank"},
        {'field': 'name', 'message': "can't be blank"},
        {'field': 'gender', 'message': "can't be blank"},
        {'field': 'status', 'message': "can't be blank"}
    ]
    return expected == received_payload

def get_valid_user_id(user_endpoint):
    """ A simple function that returns an ID from a valid user at the specified endpoint."""
    response = requests.get(user_endpoint)
    response_dict = is_proper_json(response)
    if response_dict != False:
        user_id = response_dict['data'][0]['id']
        return user_id
    else:
        return False
