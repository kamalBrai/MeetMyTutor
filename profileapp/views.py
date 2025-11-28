from django.shortcuts import render,redirect
from django.views import View
from categories.models import districts
from .models import Profile_Tutor,Profile_Student
from django.contrib import messages
from django.core.exceptions import ValidationError
import json
from mytutorapp.models import Feedback
from django.db.models import Avg
# Create your views here.


class tutor_profile_view(View):
    def get(self,request):
        tutor_profile = Profile_Tutor.objects.get(user=request.user)
        avg_rating = Feedback.objects.filter(tutor_user=tutor_profile).aggregate(Avg('rating'))['rating__avg']
        if avg_rating is None:
                avg_rating = 0  # Hand
        context = {
            'avg_rating': round(avg_rating, 1),
        }
        return render(request,'profile/tutor_profile1.html',context)
    
def edit_tutor_profile(request):
        if not request.user.is_authenticated:
            return redirect('log_in')
        district = districts.objects.all()
        try:
            data = Profile_Tutor.objects.get(user=request.user)
        except Profile_Tutor.DoesNotExist:
            data = None
        if request.method == 'POST' or request.FILES :
            try:
                if data is None:
                    data = Profile_Tutor(user=request.user)
                data.age = request.POST.get('age')
                data.qualification = request.POST.get('qualification')
                data.session_price = request.POST.get('session_price')
                data.district = request.POST.get('district')
                data.address = request.POST.get('address')
                data.gender = request.POST.get('gender')
                data.longitude = request.POST.get('longitude') or None
                data.latitude = request.POST.get('latitude') or None
                if data.longitude is None: 
                    data.location_access = False
                else:
                    data.location_access = True
                data.cv = request.FILES.get('cv')or data.cv
                if not data.cv:
                    messages.error(request, 'CV is required.')
                    return redirect('edit_tutor_profile')
                data.desc = request.POST.get('description')
                if request.POST.get('remove_profile_img') == 'on':
                     if data.profile_img:
                        data.profile_img.delete(save=False)  # delete file from storage
                data.profile_img = request.FILES.get('profile_img') or data.profile_img 
                education_levels = []
                i = 0
                while True:
                    level_key = f"educationLevels[{i}][level]"
                    subject_key = f"educationLevels[{i}][subjects][]"

                    level = request.POST.get(level_key)
                    subjects = request.POST.getlist(subject_key)

                    if not level:
                        break

                    education_levels.append({
                        "level": level,
                        "subjects": subjects
                    })
                    i += 1

                data.education_data = education_levels
                data.full_clean()
                data.form_completed = True
                data.save()
                messages.success(request,'updated successfully!')
                return redirect('tutor_profile')
            except ValidationError as ve:
                error_count = 0
                for field, errors in ve.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
                        error_count += 1
                        if error_count == 3:
                            break
                    if error_count == 3:
                        break

            except Exception as e:
                messages.error(request, str(e))
                return redirect('edit_tutor_profile')
          # Prepare preloaded education data as JSON to pass to template
        education_data_json = json.dumps(data.education_data) if data and data.education_data else '[]'
        context = {
            'district' : district,
            'education_data_json': education_data_json,
        } 
        
        return render(request,'profile/edit_tutor_profile.html',context)

def student_profile_view(request):
    return render(request,'profile/student_profile.html')

def edit_student_profile(request):
    district = districts.objects.all()
    if not request.user.is_authenticated:
            return redirect('log_in')
    try:
        data = Profile_Student.objects.get(user=request.user)
    except Profile_Student.DoesNotExist:
            data = None
    if request.method == 'POST' or request.FILES :
        try:
            if data is None:
                data = Profile_Student(user=request.user)
            data.age = request.POST.get('age') or data.age
            data.gender = request.POST.get('gender') or data.gender
            data.grade = request.POST.get('grade') or data.grade
            data.district = request.POST.get('district') or data.district
            data.address = request.POST.get('address') or data.address
            data.phone = request.POST.get('phone') or data.phone
            data.desc = request.POST.get('desc') or data.desc
            if request.POST.get('remove_profile_img') == 'on':
                if data.profile_img:
                    data.profile_img.delete(save=False)  # delete file from storage
            data.profile_img = request.FILES.get('profile_img') or data.profile_img 
            data.full_clean()
            data.form_completed = True
            data.save() 
            messages.success(request,'updated successfully!')    
            return redirect('student_profile')   
        except Exception as e:
            if hasattr(e, 'message_dict'):
                # Get errors with field names
                error_items = list(e.message_dict.items())  # returns list of (field, [errors])

                count = 0
                for field, errors in error_items:
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                        count += 1
                        if count == 3:
                            break
                    if count == 3:
                        break
            else:
                messages.error(request, str(e))

            return redirect('edit_student_profile')
    
    context = {
        'district' : district,
    }
    return render(request,'profile/edit_student_profile.html',context)