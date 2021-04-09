from verification import *

class Test_GET_User:

    def test_GET_integrated(self, user_endpoint, timeout_threshold):
        errors = []
        response = requests.get(user_endpoint)
        response_dict = is_proper_json(response)
        if response_dict != False:
            if response_dict['code'] != requests.codes.ok:
                errors.append("Status Code Error: received {}, expected 200".format(response_dict['code']))
            wrong_user_cnt = 0
            for user in response_dict['data']:
                if not is_user_datatypes(user):
                    wrong_user_cnt += 1
            if wrong_user_cnt > 0:
                errors.append("Payload Error: {} of the received users have wrong datatypes: ".format(wrong_user_cnt))
        else:
            errors.append("Server Error: Received a malformed JSON")
        if response.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response.elapsed.total_seconds()*1000, timeout_threshold*1000))

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))
    
    def test_GET_idempotency(self, user_endpoint):
        errors = []
        response1 = requests.get(user_endpoint)
        response2 = requests.get(user_endpoint)
        if not is_same_response(response1, response2):
            errors.append("Response JSONs are not the same")
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_POST_User:

    def test_POST_integrated(self, user_endpoint, valid_payload,token, timeout_threshold):
        errors = []
        url = user_endpoint

        # Only perform test if email is available.
        if make_email_free(url, valid_payload['email'], token):
            # Perform POST
            access_token_header = "Bearer " + token
            response_post = requests.post(
                url = url,
                data = valid_payload,
                headers={"Authorization": access_token_header})
            # Verify Performance
            if response_post.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
            
            # Verify Response is a well-formed JSON
            response_post_dict = is_proper_json(response_post)
            if response_post_dict != False:
                # Verify status code in response
                if response_post_dict['code'] != 201:\
                    errors.append("Status Code Error: Received {}.Expected 201"\
                        .format(response_post_dict['code']))

                # GET user that was just created
                user_id = str(response_post_dict['data']['id'])
                user_url = url + "/" + user_id
                response_get = requests.get(url= user_url)
                # Verify GET was well taken
                response_get_dict = response_get.json()
                if response_get_dict['code'] == requests.codes.ok:
                    # Verify GET response and payload are the same.
                    if not correctly_posted_user(response_get_dict['data'],valid_payload):
                        errors.append('Payload Error: User data in database and payload is not the same')

                    # Delete user created by POST
                    if not user_resource_delete(url = user_url, token = token):
                        errors.append('Clean Up Error: Failed to delete created user (ID: {})'.format(user_id))
                else:
                    errors.append('State Error: User could not be found at returned ID.')
            else:
                errors.append("Server Error: Received a malformed JSON")
        else:
            errors.append('Test Error: Could not verify testing email is free.')
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_PUT_User_Resource:

    def test_PUT_integrated(self, user_endpoint, valid_payload2, token, timeout_threshold):
        errors = []
        # PUT new user information to user created by POST
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}
        response_put = requests.put(
            url = user_url,
            data = valid_payload2,
            headers = access_token_header
        )
        print('Response: '.format(response_put))
        
        # Verify PUT status code
        response_put_dict = is_proper_json(response_put)
        if response_put_dict != False:
            print('\nResponse PUT:\n{}'.format(response_put_dict))
            if response_put_dict['code'] == requests.codes.ok:

                # Verify GET response and payload are the same.
                if not correctly_put_user(response_put_dict['data'],valid_payload2):
                    errors.append('State Error: User data in database and payload is not the same')
            else:
                errors.append('Error: PUT method unsucessful. Received {}, Expected 200'\
                    .format(response_put_dict['code']))
            
            # Delete user created by POST
            if not user_resource_delete(url = user_url, token = token):
                errors.append('Clean Up Error: Failed to delete modified user (ID: {})'.format(user_id))
        else:
            errors.append("Server Error: Received a malformed JSON")
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

    def test_PUT_idempotency(self, user_endpoint, valid_payload2, token):
        errors = []
        # PUT new user information to user created by POST
        user_id = str(get_valid_user_id(user_endpoint))
        user_url = user_endpoint + "/" + user_id
        access_token_header = {"Authorization": "Bearer " + token}
        response_put_1 = requests.put(
            url = user_url,
            data = valid_payload2,
            headers = access_token_header
        )
        response_put_2 = requests.put(
            url = user_url,
            data = valid_payload2,
            headers = access_token_header
        )
        if response_put_1.status_code == response_put_2.status_code == requests.codes.ok:

            if not is_same_response(response_put_1, response_put_2):
                errors.append("Response JSONs are not the same")
        else:
            errors.append('Request Error: Server responded {} and {} respectively, expected 200 for both')\
                .format(response_put_1.status_code, response_put_2.status_code)
        
        # Delete user created by POST
            if not user_resource_delete(url = user_url, token = token):
                errors.append('Clean Up Error: Failed to delete modified user (ID: {})'.format(user_id))

        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))