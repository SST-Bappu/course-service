from django.contrib.messages import SUCCESS


def get_client_ip(request):
    # Utility method to get client IP address
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def success_response(data, msg="Request was successful"):
    response = {
        "status" : "SUCCESS",
        "message": msg,
        "data": data
    }
    return response