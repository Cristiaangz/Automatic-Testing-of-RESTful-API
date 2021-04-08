from verification import *

class Test_GET_User:

    def test_GET_basic(self):
        errors = []
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
        if response.elapsed.total_seconds() > timeout_threshold:
            errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                .format(response.elapsed.total_seconds()*1000, timeout_threshold*1000))

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
        if make_email_free(url, valid_payload['email'], token):
            access_token_header = "Bearer " + token
            response_post = requests.post(
                url = url,
                data = valid_payload,
                headers={"Authorization": access_token_header})
            if response_post.elapsed.total_seconds() > timeout_threshold:
                errors.append("Performance Error: Response took {:.2f}ms. Threshold is {:.2f}ms"\
                    .format(response_post.elapsed.total_seconds()*1000, timeout_threshold*1000))
            
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
                if response_get.status_code == requests.codes.ok:
                    response_get_dict = response_get.json()
                    if not correctly_posted_user(response_get_dict['data'],valid_payload):
                        errors.append('Payload Error: User data in database and payload is not the same')
                    
                    if not user_resource_delete(url = user_url, token = token):
                        errors.append('Clean Up Error: Failed to delete created user (ID: {})'.format(user_id))
                else:
                    errors.append('State Error: User could not be found at returned ID.')
            else:
                errors.append("Payload Error: Received a malformed JSON")
        else:
            errors.append('Test Error: Could not verify testing email is free.')
            
        assert not errors, "Errors Occured:\n{}".format("\n".join(errors))

class Test_PUT_User_Resource:

    def test_PUT_basic(self):
        assert 1