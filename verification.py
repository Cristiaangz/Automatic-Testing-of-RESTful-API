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
    return is_id(user['id']) and is_name(user['name']) and is_email(user['email']) and \
        is_gender(user['gender']) and is_status(user['status']) and is_time(user['created_at'])\
            and is_time(user['updated_at'])

# Converts response JSONs into string form and verifies they are equal.
def is_same_response(response1, response2):
    response1_dict = is_proper_json(response1)
    response2_dict = is_proper_json(response2)
    if response1_dict != False and response2_dict != False:
        return str(response1_dict) ==  str(response2_dict)
    else:
        assert 0
        return False
    