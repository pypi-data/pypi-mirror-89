class NoargsError(Exception):
    "If your missing a arg"
    pass

class ResponseError(Exception):
    "A request error"
    pass


errors = {
    101: ResponseError('Switching Protocols.'),
    204: ResponseError("No Content Found."),
    400: ResponseError("Bad Request"),
    404: ResponseError("The page was not found, please report this."),
    408: ResponseError("Their was a request Timeout."),
    413: ResponseError("playload was to large."),
    423: ResponseError("Requested page is locked :("),
    429: ResponseError('You are being rate limited!'),
    444: ResponseError("The requested page had no response."),
    500: ResponseError('There is a server error, Try again later.'),
    504: ResponseError("There is a Gateway timeout."),
    599: ResponseError("Your network has a timeout, Try again later.")

}
