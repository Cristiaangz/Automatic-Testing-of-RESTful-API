from verification import *


class Test_GET_User:

    def test_missing_resource(self, user_endpoint, token, timeout_threshold):
        """A negative test using GET method on a missing /users endpoint

        This test verifies if server correctly handles a valid request that it
        cannot fulfill. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """

        errors = []

        # Randomly chooses a URI
        user_id = random.randint(1,999)
        url = user_endpoint + "/{}".format(user_id)
        
        # Ensures the resource is empty
        if make_resource_empty(url=url, token=token):

            # Perform GET method on empty resource
            response = requests.get(url)

            # Verify response as handled well by server
            if response.status_code == requests.codes.ok:
                response_dict = response.json()

                # Verify server reported the resource as non-existent
                if response_dict['code'] != 404:
                    errors.append("Status Code Error: received {}, expected 404".format(response_dict['code']))
            
            # Show error if request was not well taken by Server
            else:
                errors.append('Request Error: Response is {}, Expected 200 '\
                        .format(response.status_code))

            # Verify response performance
            if response.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Error if test could not be prepared properly
        else:
            errors.append("Test Error: Could not verify /public-api/user/{} is deleted")
        
        # Report errors if any
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_unauthorized(self, user_endpoint, valid_payload, token, invalid_token, timeout_threshold):
        """A negative test using POST method with an unauthorized token

        This test verifies if server correctly handles a valid POST request using
        an unauthorized token. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """
        
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
            
            # Verify Request was well handled by Server
            if response_post.status_code == requests.codes.ok:
                response_post_dict = response_post.json()

                # Verify status code in response
                if response_post_dict['code'] != 401:\
                    errors.append("Status Code Error: Received {}.Expected 401"\
                        .format(response_post_dict['code']))
            
            # Show error if request was not well taken by Server
            else:
                errors.append('Request Error: Response is {}, Expected 200 '\
                        .format(response_post.status_code))
        
        # Error if test could not be prepared properly
        else:
            errors.append('Test Error: Could not verify testing email is free.')

        # Report any errors    
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_empty_payload(self, user_endpoint, token, timeout_threshold):
        """A negative test using POST method with an empty payload

        A POST request with an empty payload is expected to be rejected (422).
        This test verifies if server correctly handles a valid POST request with an
        empty payload. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """

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
        
        # Verify Request was well taken by Server
        if response_post.status_code == requests.codes.ok:
            response_post_dict = response_post.json()

            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if not correct_empty_payload(response_post_dict['data']):
                errors.append('Payload Error: Did not receive expected error messages')
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_post.status_code))
        
        # Report any errors
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_missing_parameter(self, user_endpoint, missing_value_payload, token, timeout_threshold):
        """An negative test using POST method with a missing required parameter

        A POST request with an incomplete payload is expected to be rejected (422).
        This test verifies if server correctly handles a POST request with an
        incomplete payload. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """
        
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
        
        # Verify Request was well handled by Server
        if response_post.status_code == requests.codes.ok:
            response_post_dict = response_post.json()

            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if response_post_dict['data'] != [{'field': 'status', 'message': "can't be blank"}]:
                print(response_post_dict['data'])
                errors.append('Payload Error: Did not receive expected error messages')
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_post.status_code))

        # Report any errors    
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_wrong_datatype(self, user_endpoint, invalid_datatype_payload, token, timeout_threshold):
        """A negative test using POST method with payload of wrong datatype

        A POST request with an payload with wrong data types is expected to be
        rejected (422) and provide meaningful feedback. This test verifies if 
        server correctly handles a POST request with a payload of wrong data
        types. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors 
        (if any) is reported at the end of the test.
        """
        
        errors = []
        # Perform POST
        access_token_header = "Bearer " + token
        response_post = requests.post(
            url = user_endpoint,
            data = invalid_datatype_payload,
            headers={"Authorization": access_token_header})
        
        # Verify Performance
        if response_post.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Request was well handled by Server
        if response_post.status_code == requests.codes.ok:
            response_post_dict = response_post.json()

            # Verify status code in response
            if response_post_dict['code'] != 422:\
                errors.append("Status Code Error: Received {}.Expected 422"\
                    .format(response_post_dict['code']))
            
            # Verify correct error messages in data
            if response_post_dict['data'] != [{'field': 'status', 'message': 'can be Active or Inactive'}]:
                print(response_post_dict['data'])
                errors.append('Payload Error: Did not receive expected error messages')
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_post.status_code))
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_duplicate_request(self, user_endpoint, valid_payload,token, timeout_threshold):
        """A negative test using duplicate valid POST method

        When a server receives duplicate valid POST requests, it should accept 
        the first and reject the second as it already exists. This test verifies 
        if server correctly handles duplicate POST requests. In a single test it 
        verifies the request's status code, the response's status code, and 
        performance. 
        A combination of errors (if any) is reported at the end of the test.
        """
        
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
            
            # Verify Request was well handled by Server
            if response_post_1.status_code == requests.codes.ok:
                response_post_dict_1 = response_post_1.json()
                
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

            # Show error if request was not well taken by Server
            else:
                errors.append('Request Error: First POST Response {}, Expected 200 '\
                        .format(response_post_1.status_code))
        
        else:
            errors.append('Test Error: Could not verify testing email is free.')
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_PUT_User_Resource:

    def test_empty_resource(self, user_endpoint, valid_payload, token, timeout_threshold):
        """A negative test using PUT method to an empty resource

        When a server receives a valid PUT request to an inexistant resource,
        it should let the client know the resource was not found (404).
        This test verifies if server correctly handles this case. In a single
        test it verifies the request's status code, the response's status code, 
        and performance. 
        A combination of errors (if any) is reported at the end of the test.
        """
        
        errors = []
        user_url = user_endpoint + "/123"

        # Verify resource at target url is empty
        if make_resource_empty(user_url, token):

            # Send valid PUT request
            access_token_header = {"Authorization": "Bearer " + token}
            response_put = requests.put(
                url = user_url,
                data = valid_payload,
                headers = access_token_header
            )

            # Verify Request was well handled by Server
            if response_put.status_code == requests.codes.ok:
                response_put_dict = response_put.json()

                # Verify status code in response
                if response_put_dict['code'] != requests.codes.not_found:
                    errors.append("Status Code Error: Received {}, Expected 404".format(response_get_dict['code']))
            
            # Show error if request was not well taken by Server
            else:
                errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_put.status_code))
        
        # Error if test could not be prepared correctly
        else:
            errors.append("Test Error: Could not verify /public-api/user/{} is deleted")

        # Report any errors
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_unauthorized(self, user_endpoint, valid_payload, invalid_token, timeout_threshold):
        """A negative test using PUT method with an unauthorized token

        This test verifies if server correctly handles a valid PUT request using
        an unauthorized token. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """
        
        errors = []
        user_id = str(get_valid_user_id(user_endpoint))
        url = user_endpoint + "/" + user_id
        invalid_token_header = "Bearer " + invalid_token

        # Sends PUT request with unauthorized token
        response_put = requests.put(
            url = url,
            data = valid_payload,
            headers={"Authorization": invalid_token_header})
        
        # Verify Performance
        if response_put.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response_put.elapsed.total_seconds()*1000, timeout_threshold*1000))
        
        # Verify Request was well handled by Server
        if response_put.status_code == requests.codes.ok:
            response_put_dict = response_put.json()
            
            # Verify status code in response
            if response_put_dict['code'] != 401:\
                errors.append("Status Code Error: Received {}.Expected 401"\
                    .format(response_put_dict['code']))
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_put.status_code))
        
        # Report Any errors
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_wrong_datatype(self, user_endpoint, invalid_datatype_payload, token, timeout_threshold):
        """A negative test using PUT method with payload of wrong datatype

        A PUT request with an payload with wrong data types is expected to be
        rejected (422) and provide meaningful feedback. This test verifies if 
        server correctly handles a PUT request with a payload of wrong data
        types. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors 
        (if any) is reported at the end of the test.
        """
        
        errors = []
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}

        # PUT request with payload of invalid data types.
        response_put = requests.put(
            url = user_url,
            data = invalid_datatype_payload,
            headers = access_token_header
        )
        
        # Verify request was well handled by server
        if response_put.status_code == requests.codes.ok:
            response_put_dict = response_put.json()
            
            # Verify status code in response
            if response_put_dict['code'] != 422:
                print(response_put)
                errors.append('\nStatus Error: Received {}, Expected 422'\
                    .format(response_put_dict['code']))
            
            # Verify correct error messages in data
            elif response_put_dict['data'] != [{'field': 'status', 'message': 'can be Active or Inactive'}]:
                print(response_put_dict['data'])
                errors.append('\nPayload Error: Did not receive expected error messages')
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response_put.status_code))

        # Report any errors   
        assert not errors, "\nErrors Occured:\n{}".format("\n".join(errors))
    
    def test_empty_payload(self, user_endpoint, token, timeout_threshold):
        """A negative test using PUT method with an empty payload

        A PUT request with an empty payload is expected to work like a GET method.
        This test verifies if server correctly handles a valid POST request with an
        empty payload. In a single test it verifies the request's status code,
        the response's status code, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """

        errors = []
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id

        # Perform GET request
        response_get = requests.get(user_url)
        access_token_header = {"Authorization": "Bearer " + token}

        # Perform PUT request without payload
        response_put = requests.put(
            url = user_url,
            headers = access_token_header
        )

        # Verify Request was well taken by Server
        if response_put.status_code  == response_get.status_code == requests.codes.ok:
            
            # Verify GET and PUT responses are the same
            if not same_user(response_put.json()['data'], response_get.json()['data']):
                errors.append("Status Error: PUT response is not the same as GET")
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Server responded {} and {} respectively, expected 200 for both'\
                .format(response_put.status_code, response_get.status_code))

        # Report any errors
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))