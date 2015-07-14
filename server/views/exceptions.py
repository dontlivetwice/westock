from collections import namedtuple


class ApiError(Exception):
    error_code = None

    def __init__(self, detail_message=None, message_override=None,
                 response_attrs=None, objects=None, **kwargs):
        super(ApiError, self).__init__(detail_message)
        self.message_override = message_override
        self.response_attrs = response_attrs or []
        self.objects = objects
        for k, v in kwargs.iteritems():
            if v is not None:
                setattr(self, k, v)

    def to_api_dict(self, context):
        if self.message is None:
            message = unicode(self.message)
        elif isinstance(self.message, unicode):
            message = self.message
        else:
            message = unicode(self.message, 'utf8', 'replace')

        api_dict = {'message': message}
        if self.objects and context:
            context.process_response_data(self.objects)
            objects = context.filter_inactive_user_data(self.objects)
            api_dict['objects'] = objects
        for attr in self.response_attrs:
            try:
                api_dict[attr] = getattr(self, attr)
            except AttributeError:
                pass
        return api_dict

ResponseCode = namedtuple('ResponseCode',
                          ['numeric_code', 'http_status', 'message'])


class ResponseCodes:
    SUCCESS = ResponseCode(0, 200, "ok")
    CREATED = ResponseCode(900, 201, "ok")

    INVALID_PARAMETERS = ResponseCode(1, 400, "Invalid parameters.")
    AUTHENTICATION_FAILED = ResponseCode(2, 401, "Authentication failed.")
    AUTHORIZATION_FAILED = ResponseCode(3, 401, "Authorization failed.")
    METHOD_NOT_ALLOWED = ResponseCode(5, 405, "Method not allowed")

    FOLLOW_STOCK_FAILED = ResponseCode(6, 400, "Failed to follow stock")
    UNFOLLOW_STOCK_FAILED = ResponseCode(7, 400, "Failed to unfollow stock")


class InvalidParams(ApiError):
    error_code = ResponseCodes.INVALID_PARAMETERS


class AuthenticationFailed(ApiError):
    error_code = ResponseCodes.AUTHENTICATION_FAILED


class FollowStockFailed(ApiError):
    error_code = ResponseCodes.FOLLOW_STOCK_FAILED


class UnFollowStockFailed(ApiError):
    error_code = ResponseCodes.UNFOLLOW_STOCK_FAILED
