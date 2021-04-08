import pytest
import requests
import json
import datetime
import random
import os.path
from verification import *

def setup_module(module):
    global main_url
    global user_endpoint
    global user_123_endpoint
    global token
    global valid_payload
    main_url = "https://gorest.co.in"
    user_endpoint = "/public-api/users"
    user_123_endpoint = "/public-api/users/123"
    valid_payload = {
            "name": "Dan Doney",
            "email": "dan@securrency.com",
            "gender" : "Male",
            "status" : "Active",
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

class Test_GET_User:

    def test_GET_basic(self):
        errors = []
        threshold = 1.000
        url = main_url + user_endpoint
        response = requests.get(main_url + user_endpoint)
        if response.status_code != requests.codes.ok:
            errors.append("Status Code Error: received {}, expected 200".format(response.status_code))
        response_dict = is_proper_json(response)
        if response_dict != False:
            wrong_user_cnt = 0
            for user in response_dict['data']:
                if not is_user_datatypes(user):
                    wrong_user_cnt += 1
            if wrong_user_cnt > 0:
                errors.append("Payload Error: {} of the received users have wrong datatypes: ".format(wrong_user_cnt))
        else:
            errors.append("Payload Error: Received a malformed JSON")
        if response.elapsed.total_seconds() > threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response.elapsed.total_seconds()*1000, threshold*1000))

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_GET_idempotency(self):
        errors = []
        url = main_url + user_endpoint
        response1 = requests.get(main_url + user_endpoint)
        response2 = requests.get(main_url + user_endpoint)
        if not is_same_response(response1, response2):
            errors.append("Response JSONs are not the same")
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_POST_basic(self):
        errors = []
        url = main_url + user_endpoint
        access_token_header = "Bearer " + token
        response_post = requests.post(
            url = url,
            data = valid_payload,
            headers={"Authorization": access_token_header})
        
        if response_post.status_code != requests.codes.ok:
            errors.append("Status Code Error: received {} code".format(response_post.status_code))
        response_post_dict = is_proper_json(response_post)
        if response_post_dict != False:
            
            if response_post_dict['code'] != 201:\
                errors.append("Response Access Code is {}.Expected 201"\
                    .format(response_post_dict['code']))
            
            user_id = str(response_post_dict['data']['id'])
            user_url = url + "/" + user_id
            response_get = requests.get(url= user_url)
            response_get_dict = response_get.json()
            if not correctly_posted_user(response_get_dict['data'],valid_payload):
                errors.append('Payload Error: User data in database and payload is not the same')
            
            if not user_resource_delete(url = user_url, token = token):
                errors.append('Clean Up Error: Failed to delete created user (ID: {})'.format(user_id))
        else:
            errors.append("Payload Error: Received a malformed JSON")
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_state(self):
        assert 1
    
    def test_min_performance(self):
        assert 1

class Test_GET_User_123:

    def test_statuscode(self):
        assert 1

    def test_payload(self):
        assert 1
    
    def test_state(self):
        assert 1
    
    def test_min_performance(self):
        assert 1

class Test_PUT_User_123:

    def test_statuscode(self):
        assert 1

    def test_payload(self):
        assert 1
    
    def test_state(self):
        assert 1
    
    def test_min_performance(self):
        assert 1

class Test_DELETE_User_123:

    def test_statuscode(self):
        assert 1

    def test_payload(self):
        assert 1
    
    def test_state(self):
        assert 1
    
    def test_min_performance(self):
        assert 1