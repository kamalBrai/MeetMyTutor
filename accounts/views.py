from django.shortcuts import render,redirect
from django.views import View
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, get_user_model,logout
from profileapp.models import *

# Create your views here.
class Register(View):
    def get(self,request):
        return render(request,'registration/register.html')
    
    def post(self,request):
        try:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password1 = request.POST.get('confirmpassword')
            usertype = request.POST.get('usertype')
            if password == password1:
                    validate_password(password)
                    if password == username:
                        messages.error(request,'password and uname shouldn\'t be same')
                        return render(request, 'registration/register.html')
                    if CustomUser.objects.filter(email=email).exists():
                        messages.error(request,'email already exists!')
                        return render(request, 'registration/register.html')
                    if CustomUser.objects.filter(username=username).exists():
                        messages.error(request,'username already exists!')
                        return render(request, 'registration/register.html')
                    user = CustomUser(
                        first_name = firstname,
                        last_name = lastname,
                        username = username,
                        email = email,
                        usertype = usertype
                    )
                    user.set_password(password)
                    user.full_clean() 
                    user.save()
                    messages.success(request,'Successfully Registered!')
                    return redirect('log_in')
            else:
                messages.error(request,'password and confirm password didn\'t match!')
                return render(request, 'registration/register.html')
        
        except Exception as e:
            for m in e:
              messages.error(request,f'{str(m)}')
            return render(request, 'registration/register.html')

class Log_in(View):
    def post(self,request):
       CustomUser = get_user_model()

class Log_in(View):
    def post(self, request):
        CustomUser = get_user_model()
        try:
            username_or_email = request.POST.get('username')
            password = request.POST.get('password')

            if not username_or_email or not password:
                messages.error(request, 'Please enter both username/email and password.')
                return render(request, 'login/login.html')

            user_obj = None
            if '@' in username_or_email:
                try:
                    user_obj = CustomUser.objects.get(email=username_or_email)
                except CustomUser.DoesNotExist:
                    pass 
            
            if not user_obj:
                try:
                    user_obj = CustomUser.objects.get(username=username_or_email)
                except CustomUser.DoesNotExist:
                    pass 

            if not user_obj:
                messages.error(request, 'Invalid credentials.')
                return render(request, 'login/login.html')

            authenticated_user = authenticate(request, username=user_obj.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                next_url = request.POST.get('next') 
                if authenticated_user.is_superuser or authenticated_user.is_staff:
                    return redirect('/admin/')
                
                elif authenticated_user.usertype == 'tutor':
                    try:
                        profile = Profile_Tutor.objects.get(user=request.user)
                        if not profile.form_completed:
                            return redirect('edit_tutor_profile')  
                    except Profile_Tutor.DoesNotExist:
                        return redirect('edit_tutor_profile')  
                    return redirect('home') 
                
                elif authenticated_user.usertype == 'student':
                      # Handle 'next' only for student
                    if next_url and next_url != 'None':
                        return redirect(next_url)
                    try:
                        profile = Profile_Student.objects.get(user=request.user)
                        if not profile.form_completed:
                            return redirect('edit_student_profile')  
                    except Profile_Student.DoesNotExist:
                        return redirect('edit_student_profile')  
                    return redirect('home')  

                else:
                    messages.info(request, 'Login successful. Redirecting to default dashboard.')
                    return redirect('some_default_dashboard') 
            else:
                messages.error(request, 'Invalid credentials.')
                return render(request, 'login/login.html')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return render(request, 'login/login.html')

    def get(self,request): 
        next_url = request.GET.get('next')    
        return render(request,'login/login.html',{'next': next_url})

def log_out(request):
    # ActivityLog.objects.create(user=request.user,action =f'logged out')
    logout(request)
    return redirect('home')