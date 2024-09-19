from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

# You can configure a logger if you need to log errors
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)
    # Now add your custom error response logic.
    if response is None:
        # Handle non-DRF exceptions (e.g., custom exceptions, generic errors)
        return Response(
            {
                "error": "An unexpected error occurred.",
                "details": str(exc)  # Optional: Include the exception details in the response
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # For DRF-related exceptions, we can customize the response format here.
    response_data = {
        "error": str(exc),
        "status_code": response.status_code,
        "details": response.data  # You can customize this further based on the exception
    }

    return Response(response_data, status=response.status_code)
