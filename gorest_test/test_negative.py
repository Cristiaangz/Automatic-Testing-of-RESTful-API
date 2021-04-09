from verification import *


class Test_GET_User:

    def test_missing_resource(self, user_endpoint, token, timeout_threshold):
        errors = []
        user_id = random.randint(1,999)
        url = user_endpoint + "/{}".format(user_id)
        if make_resource_empty(url=url, token=token):
            response = requests.get(url)
            response_dict = is_proper_json(response)
            if response_dict != False:
                if response_dict['code'] != requests.codes.not_found:
                    errors.append("Status Code Error: received {}, expected 404".format(response_dict['code']))
            else:
                errors.append("Payload Error: Received a malformed JSON")
            if response.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response.elapsed.total_seconds()*1000, timeout_threshold*1000))
        else:
            errors.append("Test Error: Could not verify /public-api/user/{} is deleted")
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_unauthorized(self, user_endpoint, valid_payload, token, invalid_token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Only perform test if email is available.
        if make_email_free(url, valid_payload['email'], token):
            # Perform POST
            invalid_token_header = "Bearer " + invalid_token
            response_post = requests.post(
                url = url,
                data = valid_payload,
                headers={"Authorization": invalid_token_header})
            # Verify Performance
            if response_post.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
            
            # Verify Response is a well-formed JSON
            response_post_dict = is_proper_json(response_post)
            if response_post_dict != False:
                # Verify status code in response
                if response_post_dict['code'] != 401:\
                    errors.append("Status Code Error: Received {}.Expected 401"\
                        .format(response_post_dict['code']))
            else:
                errors.append("Server Error: Received a malformed JSON")
        else:
            errors.append('Test Error: Could not verify testing email is free.')
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_empty_payload(self, user_endpoint, token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Perform POST
        access_token_header = "Bearer " + token
        response_post = requests.post(
            url = url,
            data = {},
            headers={"Authorization": access_token_header})
        # Verify Performance
        if response_post.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Response is a well-formed JSON
        response_post_dict = is_proper_json(response_post)
        if response_post_dict != False:
            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if not correct_empty_payload(response_post_dict['data']):
                errors.append('Payload Error: Did not receive expected error messages')
        else:
            errors.append("Server Error: Received a malformed JSON")
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_missing_parameter(self, user_endpoint, missing_value_payload, token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Perform POST
        access_token_header = "Bearer " + token
        response_post = requests.post(
            url = url,
            data = missing_value_payload,
            headers={"Authorization": access_token_header})
        # Verify Performance
        if response_post.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Response is a well-formed JSON
        response_post_dict = is_proper_json(response_post)
        if response_post_dict != False:
            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if response_post_dict['data'] != [{'field': 'status', 'message': "can't be blank"}]:
                print(response_post_dict['data'])
                errors.append('Payload Error: Did not receive expected error messages')
        else:
            errors.append("Server Error: Received a malformed JSON")
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_wrong_datatype(self, user_endpoint, invalid_datatype_payload, token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Perform POST
        access_token_header = "Bearer " + token
        response_post = requests.post(
            url = url,
            data = invalid_datatype_payload,
            headers={"Authorization": access_token_header})
        # Verify Performance
        if response_post.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Response is a well-formed JSON
        response_post_dict = is_proper_json(response_post)
        if response_post_dict != False:
            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if response_post_dict['data'] != [{'field': 'status', 'message': 'can be Active or Inactive'}]:
                print(response_post_dict['data'])
                errors.append('Payload Error: Did not receive expected error messages')
        else:
            errors.append("Server Error: Received a malformed JSON")
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_duplicate_request(self, user_endpoint, valid_payload,token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Only perform test if email is available.
        if make_email_free(url, valid_payload['email'], token):
            # Perform POST
            access_token_header = "Bearer " + token
            response_post_1 = requests.post(
                url = url,
                data = valid_payload,
                headers={"Authorization": access_token_header})
            # Verify Performance of first request
            if response_post_1.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response_post_1.elapsed.total_seconds()*1000, timeout_threshold*1000))
            
            # Verify Response is a well-formed JSON
            response_post_dict_1 = is_proper_json(response_post_1)
            if response_post_dict_1 != False:
                # Verify status code in response
                if response_post_dict_1['code'] != 201:\
                    errors.append("Status Error: Couldn't create first copy. Received {}.Expected 201"\
                        .format(response_post_dict_1['code']))

                ## Perform Second Request
                response_post_2 = requests.post(
                    url = url,
                    data = valid_payload,
                    headers={"Authorization": access_token_header})
                # Verify Performance of second request
                if response_post_2.elapsed.total_seconds() > timeout_threshold:
                    errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                        .format(response_post_2.elapsed.total_seconds()*1000, timeout_threshold*1000))
                # Verify second request is rejected.
                response_post_dict_2 = is_proper_json(response_post_2)
                if response_post_dict_2 != False:
                    if response_post_dict_2['code'] != 422:\
                        errors.append("Status Code Error: Received {}.Expected 422"\
                            .format(response_post_dict_2['code']))
                    
                    # Verify correct error messages in data
                    if response_post_dict_2['data'] != [{'field': 'email', 'message': 'has already been taken'}]:
                        errors.append('Payload Error: Did not receive expected error messages')
                
                # Delete user created by POST
                user_id = str(response_post_dict_1['data']['id'])
                user_url = url + "/" + user_id
                if not user_resource_delete(url = user_url, token = token):
                    errors.append('Clean Up Error: Failed to delete created user (ID: {})'.format(user_id))

            else:
                errors.append("Server Error: Received a malformed JSON")
        else:
            errors.append('Test Error: Could not verify testing email is free.')
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_PUT_User_Resource:

    def test_empty_resource(self, user_endpoint, valid_payload, token, timeout_threshold):
        errors = []

        # PUT new user information to user created by POST
        user_url = user_endpoint + "/123"
        if make_resource_empty(user_url, token):
            response_get = requests.get(user_url)
            access_token_header = {"Authorization": "Bearer " + token}
            response_put = requests.put(
                url = user_url,
                data = valid_payload,
                headers = access_token_header
            )
            if response_put.status_code == requests.codes.ok:
                response_get_dict = response_get.json()
                if response_get_dict['code'] != requests.codes.not_found:
                    errors.append("Status Code Error: Received {}, Expected 404".format(response_get_dict['code']))
            else:
                errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_put.status_code))
        else:
            errors.append("Test Error: Could not verify /public-api/user/{} is deleted")

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_unauthorized(self, user_endpoint, valid_payload, invalid_token, timeout_threshold):
        errors = []
        user_id = str(get_valid_user_id(user_endpoint))
        url = user_endpoint + "/" + user_id
        invalid_token_header = "Bearer " + invalid_token
        response_put = requests.put(
            url = url,
            data = valid_payload,
            headers={"Authorization": invalid_token_header})
        # Verify Performance
        if response_put.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_put.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Response is a well-formed JSON
        response_put_dict = is_proper_json(response_put)
        if response_put_dict != False:
            # Verify status code in response
            if response_put_dict['code'] != 401:\
                errors.append("Status Code Error: Received {}.Expected 401"\
                    .format(response_put_dict['code']))
        else:
            print("Server Error")
            errors.append("Server Error: Received a malformed JSON")
        
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_wrong_datatype(self, user_endpoint, invalid_datatype_payload, token, timeout_threshold):
        errors = []
        # PUT new user information to user created by POST
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}
        response_put = requests.put(
            url = user_url,
            data = invalid_datatype_payload,
            headers = access_token_header
        )
        
        # Verify PUT status code
        if response_put.status_code == requests.codes.ok:
            response_put_dict = response_put.json()
            if response_put_dict['code'] != 422:
                print(response_put)
                errors.append('\nStatus Error: Received {}, Expected 422'\
                    .format(response_put_dict['code']))
            # Verify correct error messages in data
            elif response_put_dict['data'] != [{'field': 'status', 'message': 'can be Active or Inactive'}]:
                print(response_put_dict['data'])
                errors.append('\nPayload Error: Did not receive expected error messages')
        else:
            errors.append("\nServer Error: PUT request Failed. Received {}, expected 200"\
                .format(response_put.status_code))
            
        assert not errors, "\nErrors Occured:\n{}".format("\n".join(errors))
    
    def test_empty_payload(self, user_endpoint, token, timeout_threshold):
        errors = []
        # PUT new user information to user created by POST
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id
        response_get = requests.get(user_url)
        access_token_header = {"Authorization": "Bearer " + token}
        response_put = requests.put(
            url = user_url,
            headers = access_token_header
        )
        if response_put.status_code  == response_get.status_code == requests.codes.ok:
            if not same_user(response_put.json()['data'], response_get.json()['data']):
                errors.append("Status Error: PUT response is not the same as GET")
        else:
            errors.append('Request Error: Server responded {} and {} respectively, expected 200 for both'\
                .format(response_put.status_code, response_get.status_code))

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))