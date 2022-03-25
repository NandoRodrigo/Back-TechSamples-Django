from rest_framework.exceptions import APIException

class InvalidParameterName(APIException):
  status_code = 400
  default_detail = {
      "error": [
          "Invalid parameter_name"
      ]
  }
  
class InvalidTypeName(APIException):
  status_code = 400
  default_detail = {
      "error": [
          "Invalid type_name"
      ]
  }