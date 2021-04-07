import pytest
import requests
import json
import datetime
from verification import *

def setup_module(module):
    global main_url
    global user_endpoint
    global user_123_endpoint
    main_url = "https://gorest.co.in"
    user_endpoint = "/public-api/users"
    user_123_endpoint = "/public-api/users/123"

class Test_GET_User:

    def test_statuscode(self):
        errors = []
        url = main_url + user_endpoint
        response = requests.get(main_url + user_endpoint)
        if response.status_code != 200:
            errors.append("Status Code is "+ str(response.status_code))
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_payload(self):
        errors = []
        url = main_url + user_endpoint
        response = requests.get(main_url + user_endpoint)
        response_dict = is_proper_json(response)
        if response_dict != False:
            wrong_user_cnt = 0
            for user in response_dict['data']:
                if not is_user_datatypes(user):
                    wrong_user_cnt += 1
            if wrong_user_cnt > 0:
                errors.append("Users with wrong datatypes: "+ str(wrong_user_cnt))
        else:
            errors.append("Received a malformed JSON")
        
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    
    def test_state(self):
        errors = []
        url = main_url + user_endpoint
        response1 = requests.get(main_url + user_endpoint)
        response2 = requests.get(main_url + user_endpoint)
        if not is_same_response(response1, response2):
            errors.append("Response JSONs are not the same")
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_min_performance(self):
        threshold = 1.000
        errors = []
        url = main_url + user_endpoint
        response = requests.get(main_url + user_endpoint)
        if response.elapsed.total_seconds() > threshold:
            errors.append("Response took {}ms, larger than {}ms threshold"\
                .format(str(response.elapsed.total_seconds()*1000), str(threshold*1000)))

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_statuscode(self):
        assert 1

    def test_payload(self):
        assert 1
    
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