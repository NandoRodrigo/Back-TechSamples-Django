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
  
class InvalidResultValue(APIException):
  status_code = 400
  default_detail = {
      "error": [
          "Invalid value in result: must be a string of number or null "
      ]
  }
  
class InvalidBodyContent(APIException):
  status_code = 400
  default_detail = {
      "error": [
          "class_data key not given"
      ]
  }