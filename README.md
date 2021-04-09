# Automatic Testing of RESTful API

## Description
This repository contains Python scripts performing automated endpoint verification for RESTful API using pytest. The current implementation queries the https://gorest.co.in server. It performs positive and negative tests for three endpoints: `GET /public-api/users`, `POST /public-api/users`, and `PUT /public-api/users/###` (where ### corresponds to the UUID of a valid user.)

All tests are contained in the gorest_test folder. A token.txt file containting a valid bearer token to the https://gorest.co.in server is needed to perform the tests. This text file should be automatically created after using the setup.py script. The tests are within the `test_poitive.py` and `test_negative.py` files respectively. They both depend on the `verification.py` which contains pytest fixtures and useful testing functions.

## Instructions
1) Confirm all required packages are installed by running `pip3 install -r requirements.txt`
2) Confirm token.txt file exists by running `python3 setup.py` and inputting a valid bearer token to the https://gorest.co.in server.
3) Run pytest from the main folder (NOT gorest_test folder)

## Testing Criteria
Each positive or negative test will perform specific combination of test actions. The list is:
1) *Validate Server Handling*: Confirm server handles request properly (No 500 response.)
2) *Validate Status Code*: Confirm server responds with expected status code.
3) *Validate Payload*: Confirm response payload has expected content.
4) *Validate State*: Confirm server status changes as per request (or remains the same when appropriate.)
5) *Validate Basic Performance*: Confirm server response is received within time threshold (1000ms as default)

## Test Descriptions

### GET /public-api/users

- `test_GET_integrated`: This test verifies if server correctly handles a valid request. In a single test it verifies the request's status code, the response's status code, payload, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_GET_idempotency`: This test verifies that two subsequent GET requests to the same endpoint provide exactly the same response.
- `test_missing_resource`: This test verifies if server correctly handles a valid request that it cannot fulfill. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.

### POST /public-api/users
- `test_POST_integrated`: This test verifies that the server correctly handles a valid POST request. In a single test it verifies the request's status code, the response's status code, payload, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_unauthorized`:This test verifies if server correctly handles a valid POST request using an unauthorized token. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_empty_payload`: A POST request with an empty payload is expected to be rejected (422). This test verifies if server correctly handles a valid POST request with an empty payload. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_missing_parameter`: A POST request with an incomplete payload is expected to be rejected (422). This test verifies if server correctly handles a POST request with an incomplete payload. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_wrong_datatype`: A POST request with an payload with wrong data types is expected to be rejected (422) and provide meaningful feedback. This test verifies if server correctly handles a POST request with a payload of wrong data types. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_duplicate_request`: When a server receives duplicate valid POST requests, it should accept the first and reject the second as it already exists. This test verifies if server correctly handles duplicate POST requests. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.

### PUT /public-api/users/###

- `test_PUT_integrated`: This test verifies that the server correctly handles a valid PUT request to an existing resource. In a single test it verifies the request's status code, the response's status code, payload, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_PUT_idempotency`: This test verifies that two subsequent PUT requests to the same endpoint perform exactly the same action.
- `test_empty_resource`: When a server receives a valid PUT request to an inexistant resource, it should let the client know the resource was not found (404). This test verifies if server correctly handles this case. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_unauthorized`: This test verifies if server correctly handles a valid PUT request using an unauthorized token. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_wrong_datatype`: A PUT request with an payload with wrong data types is expected to be rejected (422) and provide meaningful feedback. This test verifies if server correctly handles a PUT request with a payload of wrong data types. In a single test it verifies the request's status code, the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.
- `test_empty_payload`: A PUT request with an empty payload is expected to work like a GET method. This test verifies if server correctly handles a valid POST request with an empty payload. In a single test it verifies the request's status code,the response's status code, and performance. A combination of errors (if any) is reported at the end of the test.

## Limitations
Due to development time constraints, this repository was faced with many limitation. Hopefully, these will be addressed in the future.
1) *Parametrization*: Similar tests for different enpoints such as `test_empty_payload` and `test_unauthorized` are done for several endpoints. It is conceivable to modify the code such that it can take parametrized inputs and perform more tests with less code.
2) *Normalization*: Several pieces of feedback, such as error messages, vary from test to test. It would be ideal to have these error messages as functions or fixtures to ensure all error messages are consistent.
3) *Multi-step tests*: Multi-step tests, where a series of HTTP methods are sent to the server one after the other, would be an ideal next step to verify the robustness of the API.
