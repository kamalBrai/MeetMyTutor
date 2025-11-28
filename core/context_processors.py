from requestapp.models import Requesting_tutor

def chat_requests(request):
    """
    Returns all chat requests for the logged-in user to display in the navbar.
    """
    if not request.user.is_authenticated:
        return {"chat_requests": []}

    if request.user.usertype == "student":
        requests = Requesting_tutor.objects.filter(student_user__user=request.user, status="accepted")
    else:
        requests = Requesting_tutor.objects.filter(tutor_user__user=request.user, status="accepted")

    return {"chat_requests": requests}
