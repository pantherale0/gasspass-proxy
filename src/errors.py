
class HTTPError(Exception):
    """Generic HTTP Error."""
    def __init__(self, response_code, error_code, error_message) -> None:
        super().__init__()
        self.details = {
            "code": error_code,
            "message": error_message
        }
        self.response = response_code

class NotFound(HTTPError):
    """Not Found Exception."""
    def __init__(self) -> None:
        super().__init__(404, "not_found", "The resource at this location was not found.")

class InvalidRequest(HTTPError):
    """Invalid Request Error."""
    def __init__(self) -> None:
        super().__init__(400, "invalid_request", "The service at this location does not accept this type of request.")
