import pytest
import requests
import json
import datetime

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