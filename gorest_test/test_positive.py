from verification import *

class Test_GET_User:

    def test_GET_integrated(self, user_endpoint, timeout_threshold):
        """An integrated positive test for GET method to a /users endpoint

        This test verifies if server correctly handles a valid request. 
        In a single test it verifies the request's status code, the response's status 
        code, payload, and performance. A combination of errors (if any) is
        reported at the end of the test.
        """

        errors = []
        # GET request to endpoint
        response = requests.get(user_endpoint)
        response_dict = is_proper_json(response)

        # Verify Request was well taken by Server
        if response.status_code == requests.codes.ok:
            response_dict = response.json()

            # Verify request response code is what expected
            if response_dict['code'] != requests.codes.ok:
                errors.append("Status Code Error: received {}, expected 200".format(response_dict['code']))
            
            # Verify all user payloads have correct data types
            wrong_user_cnt = 0
            for user in response_dict['data']:
                if not is_user_datatypes(user):
                    wrong_user_cnt += 1
            if wrong_user_cnt > 0:
                errors.append("Payload Error: {} of the received users have wrong datatypes: ".format(wrong_user_cnt))
        
        # Show error if request was not well taken by Server
        else:
            errors.append('Request Error: Response is {}, Expected 200 '\
                    .format(response.status_code))

        # Verify request response arrived within expected time threshold
        if response.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response.elapsed.total_seconds()*1000, timeout_threshold*1000))

        # Report errors if any
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_GET_idempotency(self, user_endpoint):
        """A test of GET method's idempotency to a /users endpoint

        This test verifies that two subsequent GET requests to the same endpoint
        provide exactly the same response.
        """

        errors = []
        # Send to subsequent GET requests to users endpoint
        response1 = requests.get(user_endpoint)
        response2 = requests.get(user_endpoint)

        # Verify if responses are the same
        if not is_same_response(response1, response2):
            errors.append("Response JSONs are not the same")
        
        # Report errors if any
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_POST_integrated(self, user_endpoint, valid_payload,token, timeout_threshold):
        """An integrated positive test for POST method to a /users endpoint

        This test verifies that the server correctly handles a valid POST request. 
        In a single test it verifies the request's status code, the response's 
        status code, payload, and performance. 
        A combination of errors (if any) is reported at the end of the test.
        """

        errors = []
        url = user_endpoint

        # Only perform test if email is available.
        if make_email_free(url, valid_payload['email'], token):
            # Perform valid POST request
            access_token_header = "Bearer " + token
            response_post = requests.post(
                url = url,
                data = valid_payload,
                headers={"Authorization": access_token_header})
           
            # Verify Performance
            if response_post.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
            
             # Verify Request was well taken by Server
            if response_post.status_code == requests.codes.ok:
                # Verify status code in response
                response_post_dict = response_post.json()
                if response_post_dict['code'] != 201:\
                    errors.append("Status Code Error: Received {}.Expected 201"\
                        .format(response_post_dict['code']))

                # GET user that was just created
                user_id = str(response_post_dict['data']['id'])
                user_url = url + "/" + user_id
                response_get = requests.get(url= user_url)
                response_get_dict = response_get.json()
                if response_get_dict['code'] == requests.codes.ok:
                    # Verify GET response and payload are the same.
                    if not same_user(response_get_dict['data'],valid_payload):
                        errors.append('Payload Error: User data in database and payload is not the same')

                    # Delete user created by POST
                    if not user_resource_delete(url = user_url, token = token):
                        errors.append('Clean Up Error: Failed to delete created user (ID: {})'.format(user_id))
                # Show error if GET method fails.
                else:
                    errors.append('State Error: User could not be found at returned ID.')
            # Show error if request was not well taken by Server
            else:
                errors.append('Request Error: Response is {}, Expected 200 '\
                        .format(response_post.status_code))
        # Show error if test could be prepared correctly
        else:
            errors.append('Test Error: Could not verify testing email is free.')

        # Report errors (if any)    
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_PUT_User_Resource:

    def test_PUT_integrated(self, user_endpoint, valid_payload, token, timeout_threshold):
        """An integrated positive test for UPUT method to a /users/### endpoint

        This test verifies that the server correctly handles a valid PUT request
        to an existing resource. In a single test it verifies the request's status
        code, the response's status code, payload, and performance. 
        A combination of errors (if any) is reported at the end of the test.
        """
        
        errors = []
        # Get ID of an existing user to create valid URI
        user_id = str(get_valid_user_id(user_endpoint))

        # Prepare and send PUT request
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}
        response_put = requests.put(
            url = user_url,
            data = valid_payload,
            headers = access_token_header
        )
        
        # Verify PUT request was handled by server
        if response_put.status_code == requests.codes.ok:
            response_put_dict = response_put.json()
            if response_put_dict['code'] == requests.codes.ok:

                # Error if response and payload are the same.
                if not same_user(response_put_dict['data'],valid_payload):
                    errors.append('State Error: User data in database and payload are not the same')
            
            # Error if unexpected status code
            else:
                errors.append('Status Code Error: PUT method unsucessful. Received {}, Expected 200'\
                    .format(response_put_dict['code']))
            
            # Delete user created by POST
            if not user_resource_delete(url = user_url, token = token):
                errors.append('Clean Up Error: Failed to delete modified user (ID: {})'.format(user_id))
        
        # Error if request was not handled well by server
        else:
            errors.append("Server Error: PUT request Failed. Received {}, expected 200"\
                .format(response_put.status_code))

        # Report Errors (if any)    
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_PUT_idempotency(self, user_endpoint, valid_payload, token):
        """A test of PUT method's idempotency to a /users/### endpoint

        This test verifies that two subsequent PUT requests to the same endpoint
        perform exactly the same action.
        """

        errors = []
        # Get ID of an existing user to create valid URI
        user_id = str(get_valid_user_id(user_endpoint))

        # Prepare Request
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}

        # Perform two identical PUT requests
        response_put_1 = requests.put(
            url = user_url,
            data = valid_payload,
            headers = access_token_header
        )
        response_put_2 = requests.put(
            url = user_url,
            data = valid_payload,
            headers = access_token_header
        )

        # Verify if requests were well handled
        if response_put_1.status_code == response_put_2.status_code == requests.codes.ok:

            # Error if their response is not exactly the same
            if not is_same_response(response_put_1, response_put_2):
                errors.append("Response JSONs are not the same")
        
        # Error if any request as not well handled by server
        else:
            errors.append('Request Error: Server responded {} and {} respectively, expected 200 for both'\
                .format(response_put_1.status_code, response_put_2.status_code))
        
        # Delete user edited by PUT
            if not user_resource_delete(url = user_url, token = token):
                errors.append('Clean Up Error: Failed to delete modified user (ID: {})'.format(user_id))

        # Report Errors (if any)
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))