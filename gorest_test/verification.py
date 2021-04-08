import pytest
import requests
import json
import datetime
import sys

def setup_module(module):
    global main_url
    global user_endpoint
    global user_123_endpoint
    global token
    global valid_payload
    global timeout_threshold, user_123_payload
    main_url = "https://gorest.co.in"
    user_endpoint = "/public-api/users"
    user_123_endpoint = "/public-api/users/123"
    timeout_threshold = 1.000
    valid_payload = {
            "name": "Dan Doney",
            "email": "dan@securrency.com",
            "gender" : "Male",
            "status" : "Active",
        }

    user_123_payload = {
            "id" : 1,
            "name": "Ilya Shkapo",
            "email": "ilya@securrency.com",
            "gender" : "Male",
            "status" : "Inactive",
        }
    
    if os.path.isfile("token.txt"):
        f = open("token.txt", "r")
        token = f.readline()
        f.close()
    else:
        token = ''
        while token == '':
            token = input("\n\nToken file not found. Please enter gorest.co.in token:\n")
            if len(token) != 64:
                print("Error: Token must be 64 characters long")
                token = ''

# Valid ID must be a non-negative integer
def is_id(id):
    return isinstance(id, int) and id > 0

# Valid name must be a non-empty string
def is_name(name):
    return isinstance(name, str) and len(name) > 0

# Valid email must be a string containting '@' and lenght greater than 4 (min email: x@y.z)
def is_email(email):
    return isinstance(email, str) and len(email) >= 5 and ('@' in email)

# Valid gender must be a string either 'Male' or 'Female'
def is_gender(gender):
    return isinstance(gender, str) and gender == 'Male' or gender == 'Female'

# Valid status must be a string either 'Active' or 'Inactive'
def is_status(status):
    return isinstance(status, str) and status == 'Active' or status == 'Inactive'

# Valid time must be a string that can be turned into an datetime object.
def is_time(time):
    try:
        datetime.datetime.fromisoformat(time)
        return True
    except ValueError:
        return False

# Valid JSON will convert by .json() method
def is_proper_json(response):
    try:
        return response.json()
        
    except json.JSONDecodeError:
        return False

# Checks all parameters for a user dictionary
def is_user_datatypes(user):
    return all([
        is_id(user['id']),
        is_name(user['name']),
        is_email(user['email']),
        is_gender(user['gender']),
        is_status(user['status']),
        is_time(user['created_at']),
        is_time(user['updated_at'])
    ])

# Converts response JSONs into string form and verifies they are equal.
def is_same_response(response1, response2):
    response1_dict = is_proper_json(response1)
    response2_dict = is_proper_json(response2)
    if response1_dict != False and response2_dict != False:
        return str(response1_dict) ==  str(response2_dict)
    else:
        assert 0
        return False

# Converts response JSONs into string form and verifies they are equal.
def correctly_posted_user(response_get_dict, payload):
    return all([
        response_get_dict['name'] ==  payload['name'],
        response_get_dict['email'] ==  payload['email'],
        response_get_dict['gender'] ==  payload['gender'],
        response_get_dict['status'] ==  payload['status'],
    ])

def user_resource_exists(url):
    response = requests.get(url)
    return response.status_code == requests.codes.ok

def user_resource_delete(url, token):
    access_token_header = "Bearer " + token
    response = requests.delete(
        url = url,
        headers={"Authorization": access_token_header}
    )
    return response.status_code == requests.codes.ok

def verify_email_free(url, email):
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
                print('Result found. Attempting to delete')
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
    print("\nVerifying if {} exists".format(email))
    response = requests.get(url, params={'email': email})
    if response.status_code == requests.codes.ok:
        print("GET method successful")
        try:
            response_dict = response.json()
            if response_dict['code'] == requests.codes.not_found:
                print('{} is free'.format(email))
                return True
            else:
                print('Result found. Attempting to delete')
                return user_resource_delete(url = url, token = token)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            return False
    else:
        print("GET method was unsuccessful ({})".format(response.status_code))
        return False