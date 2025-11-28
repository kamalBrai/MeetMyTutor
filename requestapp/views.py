from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile_Tutor, Profile_Student, Requesting_tutor
from categories.models import subjects_list

@login_required(login_url='log_in')
def tutor_session_request(request, id):
    # Get tutor and student objects
    tutor = get_object_or_404(Profile_Tutor, id=id)
    student = Profile_Student.objects.get(user=request.user)

    # Prepare subjects grouped by education level directly from tutor JSON
    subjects_by_level = []
    for level in tutor.education_data:
        level_name = level.get('level', '')  # e.g., "secondary_9_10"
        formatted_level_name = level_name.replace("_", " ").capitalize()
        subjects_by_level.append({
            'level': formatted_level_name,
            'subjects': level.get('subjects', [])
        })

    selected_subjects = []  # For pre-checking (if editing)

    if request.method == 'POST':
        try:
            # Get selected subjects from form (list of strings)
            selected_subjects = request.POST.getlist('subjects')
            selected_subjects = [s.strip() for s in selected_subjects if s.strip()]

            # Collect other form data
            mode = request.POST.get('mode')
            time_from = request.POST.get('time_from')
            time_to = request.POST.get('time_to')
            start_date = request.POST.get('date_start')
            end_date = request.POST.get('date_end')
            priceperhour = request.POST.get('perhour')
            desc = request.POST.get('desc')

            # Create and save Requesting_tutor object
            request_data = Requesting_tutor(
                proposed_rate=priceperhour,
                session_start_date=start_date,
                session_end_date=end_date,
                session_time_from=time_from,
                session_time_to=time_to,
                student_user=student,
                tutor_user=tutor,
                desc=desc,
                mode=mode,
                subjects=selected_subjects  # <-- store subjects as JSON
            )
            request_data.full_clean()
            request_data.save()

            messages.success(request, "Request sent successfully!")
            return redirect('tutor_session_request', id=id)

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('tutor_session_request', id=id)

    context = {
        'tutor': tutor,
        'subjects_by_level': subjects_by_level,
        'selected_subjects': selected_subjects
    }
    return render(request, 'request_session/request_tutor.html', context)

@login_required(login_url='log_in')
def tutor_request(request):
    tutor = Profile_Tutor.objects.get(user=request.user)
    list_req_tutor = Requesting_tutor.objects.filter(tutor_user=tutor) if tutor else []

    # Prepare list with subjects for display
    req_with_subjects = []
    for req in list_req_tutor:
        # JSONField stores a list of subjects
        selected_subjects = req.subjects if req.subjects else []
        req_with_subjects.append({
            'request': req,
            'subjects': selected_subjects
        })

    context = {'req_list': req_with_subjects}
    return render(request, 'request_session/request_view_tutor.html', context)

@login_required(login_url='log_in')
def student_request(request):
    # Get current student
    student = Profile_Student.objects.get(user=request.user)
    
    # Fetch all requests made by this student
    list_req = Requesting_tutor.objects.filter(student_user=student) if student else []
    
    context = {'list_req': list_req}
    return render(request, 'request_session/request_view.html', context)

@login_required(login_url='log_in')
def counter_offer(request, id):
    data2 = get_object_or_404(Requesting_tutor, id=id)
    data = data2.student_user
    if request.method == 'POST':
        data2.counter_start_date = request.POST.get('counter_start_date')
        data2.counter_end_date = request.POST.get('counter_end_date')
        data2.counter_time_from = request.POST.get('counter_time_from')
        data2.counter_time_to = request.POST.get('counter_time_to')
        data2.counter_proposed_rate = request.POST.get('counter_proposed_rate')
        data2.desc = request.POST.get('desc')
        data2.status = 'counter offered'
        data2.save()
        messages.success(request, 'Counter offer sent successfully!')
        return redirect('request_list_tutor')
 
    context = {'data': data, 'data2': data2}
    return render(request, 'request_session/counter_offer.html', context)


@login_required(login_url='log_in')
def accept_request(request, id):
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2 = get_object_or_404(Requesting_tutor, id=id)
        data2.status = 'accepted' if value == 'accepted' else 'rejected'
        data2.save()
        messages.success(request, 'Request processed successfully!')
        return redirect('request_list_tutor')


@login_required(login_url='log_in')
def edit_accept_request(request, id):
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2 = get_object_or_404(Requesting_tutor, id=id)
        data2.status = 'accepted' if value == 'accepted' else 'rejected'
        data2.is_edit = True
        data2.save()
        messages.success(request, 'Request processed successfully!')
        return redirect('request_list_tutor')


@login_required(login_url='log_in')
def edit_request(request, id):
    data2 = get_object_or_404(Requesting_tutor, id=id)
    data = data2.student_user
    if request.method == 'POST':
        data2.counter_start_date = request.POST.get('counter_start_date')
        data2.counter_end_date = request.POST.get('counter_end_date')
        data2.counter_time_from = request.POST.get('counter_time_from')
        data2.counter_time_to = request.POST.get('counter_time_to')
        data2.counter_proposed_rate = request.POST.get('counter_proposed_rate')
        data2.desc = request.POST.get('desc')
        data2.status = 'counter offered'
        data2.is_edit = True
        data2.save()
        messages.success(request, 'Counter offer sent successfully!')
        return redirect('request_list_tutor')

    context = {'data': data, 'data2': data2}
    return render(request, 'request_session/edit_request.html', context)


@login_required(login_url='log_in')
def counter_offer_view(request, id):
    data2 = get_object_or_404(Requesting_tutor, id=id)
    data = data2.student_user
    if request.method == 'POST':
        value = request.POST.get('submit_btn')
        data2.status = 'accepted' if value == 'accepted' else 'rejected'
        data2.save()
        messages.success(request, 'Offer processed successfully!')
        return redirect('request_list')

    context = {'data': data, 'data2': data2}
    return render(request, 'request_session/counter_offer_view.html', context)
