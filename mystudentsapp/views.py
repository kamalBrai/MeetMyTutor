from django.shortcuts import render, redirect
from profileapp.models import Profile_Tutor
from requestapp.models import Requesting_tutor
from django.contrib import messages
from mytutorapp.models import Feedback
from django.db.models import Exists, OuterRef

# ---------------------------
# Ongoing students (incomplete)
# ---------------------------
def mystudents(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    # Only accepted and ongoing sessions for this tutor
    data = Requesting_tutor.objects.filter(
        status='accepted',
        tutor_user=tutor,
        is_complete=False
    )
    context = {
        'data': data,
        'active_tab': 'incomplete',
    }
    return render(request, 'student/incomplete_tutor_students.html', context)


# ---------------------------
# Mark a session as complete
# ---------------------------
def is_complete_view(request, id):
    try:
        data = Requesting_tutor.objects.get(id=id)
        if request.method == 'POST':
            data.is_complete = True
            data.save()
            return redirect('mystudents')
    except Exception as e:
        messages.error(request, f'{str(e)}')
        return redirect('mystudents')


# ---------------------------
# Completed sessions
# ---------------------------
def completed_view(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    # Only accepted and completed sessions
    value = Requesting_tutor.objects.filter(
        status='accepted',
        is_complete=True,
        tutor_user=tutor
    ).annotate(
        feedback_given=Exists(
            Feedback.objects.filter(
                req_tutor=OuterRef('pk'),
                tutor_user=tutor
            )
        )
    )
    context = {
        'value': value,
        'active_tab': 'completed'
    }
    return render(request, 'student/complete_tutor_students.html', context)


# ---------------------------
# All students (accepted requests)
# ---------------------------
def all_students(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    value = Requesting_tutor.objects.filter(
        status='accepted',
        tutor_user=tutor
    ).annotate(
        feedback_given=Exists(
            Feedback.objects.filter(
                req_tutor=OuterRef('pk'),
                tutor_user=tutor
            )
        )
    )
    context = {
        'value': value,
        'active_tab': 'all_students',
    }
    return render(request, 'student/all_tutor_students.html', context)
