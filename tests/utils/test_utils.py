import logging

import requests

logger = logging.getLogger("bdd-tests")


def check_response(response: requests.Response, operation: str) -> None:
    """
    Check response status and handle errors consistently.
    Args:
        response: Response from API call
        operation: Description of the operation being performed
    Raises:
        AssertionError: If the response status code is not 200
    """
    if response.status_code != 200:
        error_message = (
            f"{operation} failed.\n"
            f"Status code: {response.status_code}\n"
            f"Response body: {response.text}"
        )
        logger.error(error_message)
        raise AssertionError(error_message)
