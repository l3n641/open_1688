class AopError(Exception):
    """
    1. Failed before sending a request.
        e.g. Some of the required API parameters missing.
    2. Failed to parse the returned results.

    """
    pass


class ApiError(Exception):
    """
    The remote server returned error and the error messages were successfully recognized.

    Attributes
    ----------
    api : str
    error_code : str
    error_message : str
    exception : str
    request_id : str

    """

    def __init__(self, api, error_code='', error_message='', exception='', request_id=''):
        self.api = api
        self.error_code = error_code
        self.error_message = error_message
        self.exception = exception
        self.request_id = request_id

    def __str__(self, *args, **kwargs):
        return 'ApiError [api=%s; error_code=%s; error_message=%s; exception=%s; request_id=%s]' % \
               (self.api, self.error_code, self.error_message, self.exception, self.request_id)
