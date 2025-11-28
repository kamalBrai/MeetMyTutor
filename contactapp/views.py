from django.shortcuts import render,redirect
from django.views import View
from .models import Contactmodel
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
# Create your views here.
class Contact_Page(View):
    def post(self,request):
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            data = Contactmodel(name=name,email=email,message=message)
            data.full_clean()
            data.save()
            
            # ActivityLog.objects.create(
            #     user= request.user if request.user.is_authenticated else None,
            #     action = f"Contact form added"
            #     )
            
             ##gmail starts
            subject = "Thank you Getting in Touch!"
            message = render_to_string('contact/gmail.html',{'name': name ,'date':datetime.now()})
            from_email = 'saraswotikhadka2k2@gmail.com'
            recipient_list = [email]
            emailmsg = EmailMessage(subject,message,from_email,recipient_list)
            emailmsg.send(fail_silently=False)
            ##gmail ends
            
            messages.success(request,'Sent Sucessfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request,f'{str(e)}')
            return redirect('contact')
        
    def get(self,request):
         return render(request,'contact/contact.html')