from django.shortcuts import render, redirect, get_object_or_404
from profileapp.models import Profile_Tutor, Profile_Student
from requestapp.models import Requesting_tutor
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import FeedbackForm
from django.db.models import Exists, OuterRef
from .models import Feedback

# --- My Tutors views (existing) ---
def my_tutors_view(request):
    student = Profile_Student.objects.get(user=request.user)
    list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted') if student else []
    context = {'list_req' : list_req, 'active_tab': 'all_tutors'} 
    return render(request,'mytutors/my_tutors.html',context)

def mytutors_ongoing(request):
    student = Profile_Student.objects.get(user=request.user)
    list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted',is_complete=False) if student else []
    context = {'list_req' : list_req, 'active_tab': 'incomplete'} 
    return render(request,'mytutors/ongoing_my_tutors.html',context)

def mytutors_complete(request):
    student = Profile_Student.objects.get(user=request.user)
    list_req = Requesting_tutor.objects.filter(student_user_id=student,status='accepted',is_complete=True) if student else []
    list_req = list_req.annotate(
        feedback_given=Exists(
            Feedback.objects.filter(
                req_tutor=OuterRef('pk'),
                student_user=student
            )
        )
    )
    context = {'list_req' : list_req, 'active_tab': 'completed'} 
    return render(request,'mytutors/complete_my_tutors.html',context)

@login_required(login_url='log_in')
def feedback_view(request, id):
    req_tutor = get_object_or_404(Requesting_tutor, id=id)
    tutor_profile = req_tutor.tutor_user
    student_profile = Profile_Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.tutor_user = tutor_profile
            feedback.student_user = student_profile
            feedback.req_tutor = req_tutor
            feedback.user = request.user
            feedback.is_feedback = True
            feedback.save()
            return redirect('feedback_thankyou')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_tutor.html', {'form': form})

def feedback_thankyou(request):
    return render(request, 'feedback/feedback_thankyou.html')

def student_feedback_view(request,id):
    tutors = Requesting_tutor.objects.get(id=id)
    student = Profile_Student.objects.get(user=request.user)
    show = Feedback.objects.filter(tutor_user = tutors.tutor_user, student_user = student,req_tutor = tutors).first()
    if request.method == 'POST':
        show.delete()
        return redirect('my_tutors_complete')
    return render(request,'feedback/view_feedback_student.html',{'show': show})

def tutor_feedback_view(request,id):
    student = Requesting_tutor.objects.get(id=id)
    tutors = Profile_Tutor.objects.get(user=request.user)
    show = Feedback.objects.filter(student_user = student.student_user, tutor_user = tutors,req_tutor = student).first()
    return render(request,'feedback/view_feedback_tutor.html',{'show': show})

# --- New Nearest Tutor Map View ---
import osmnx as ox
import networkx as nx

def nearest_tutors_map(request):
    """Return nearest tutors with real road distances using OSM"""
    try:
        student_lat = float(request.GET.get('lat'))
        student_lng = float(request.GET.get('lng'))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid coordinates"}, status=400)

    # Load road network around student (5 km radius)
    G = ox.graph_from_point((student_lat, student_lng), dist=5000, network_type='drive')

    # Map student to nearest node
    student_node = ox.distance.nearest_nodes(G, student_lng, student_lat)

    # Fetch tutors with coordinates
    tutors = Profile_Tutor.objects.exclude(latitude__isnull=True, longitude__isnull=True)

    tutors_data = []
    for tutor in tutors:
        tutor_node = ox.distance.nearest_nodes(G, tutor.longitude, tutor.latitude)
        try:
            path = nx.shortest_path(G, source=student_node, target=tutor_node, weight='length')
            distance = nx.shortest_path_length(G, source=student_node, target=tutor_node, weight='length')
            path_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]

            tutors_data.append({
                "id": tutor.id,
                "name": f"{tutor.user.first_name} {tutor.user.last_name}",
                "lat": tutor.latitude,
                "lng": tutor.longitude,
                "distance_m": distance,
                "path_coords": path_coords,
                "profile_img": tutor.profile_img.url if tutor.profile_img else "/static/images/default.jpg"
            })
        except nx.NetworkXNoPath:
            continue

    return JsonResponse({
        "student": {"lat": student_lat, "lng": student_lng},
        "tutors": tutors_data
    })
