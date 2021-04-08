from verification import *


class Test_GET_User:

    def test_missing_resource(self):
        user_id = random.randint(1,999)
        url = main_url + user_endpoint + "/{}".format(user_id)
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

    def test_unauthorized(self):
        assert 1
    
    def test_empty_payload(self):
        assert 1

    def test_missing_parameter(self):
        assert 1

    def test_wrong_datatype(self):
        assert 1
    
    def test_duplicate_request(self):
        assert 1

class Test_PUT_User_Resource:

    def test_empty_resource(self):
        assert 1