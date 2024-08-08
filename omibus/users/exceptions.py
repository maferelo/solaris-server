from rest_framework.exceptions import APIException


class InvalidCode(APIException):
    status_code = 400
    default_detail = "Invalid code"
    default_code = "invalid_code"
