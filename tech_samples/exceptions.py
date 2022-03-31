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


class InvalidClassId(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "Invalid class_id"
        ]
    }


class NoneConsumable(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "Needs consumable items to make an analysis"
        ]
    }


class NotInStock(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "Item not in stock"
        ]
    }


class WrongAnalysisItem(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "Some consumable is not for this analysis"
        ]
    }


class InsufficientQuantity(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "Insufficient consumable items for this analysis"
        ]
    }


class InvalidBodyContent(APIException):
    status_code = 400
    default_detail = {
        "error": [
            "class_data key not given"
        ]
    }
