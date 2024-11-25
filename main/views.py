from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.contrib import messages
import os
from PIL import Image


def list_complaint(request):
    queryset = Complaint.objects.all()
    context={'complaint':queryset}
    return render(request,'list.html',context)    

# def register_complaint(request):
#     if request.method=="POST":
#         data=request.POST
#         name=data.get("complaint_name")
#         complaint_description=data.get("complaint_description")
#         complaint_image=request.FILES.get("complaint_image")
#         Complaint.objects.create(name=name,
#                                desc=complaint_description,
#                                image=complaint_image)
#         messages.info(request, 'Complaint registered successfully.')
#         return redirect('/')

#     return render(request, 'register.html')


from django.core.mail import send_mail,EmailMessage
from django.conf import settings

def send_email_to_client():
    subject = "This mail is from Django Server"
    message = "Testing Email"
    from_email = settings.EMAIL_HOST_USER
    recepient_list = ["sonaryash1406@gmail.com"]
    send_mail(subject,message,from_email,recepient_list)


def send_email_with_attachment(subject,messsage,recepient_list,file_path):
    mail =EmailMessage(subject=subject,body=messsage, from_email= settings.EMAIL_HOST_USER,
                       to=recepient_list)
    
    mail.attach_file(file_path)
    mail.send()
    
def send_email(request):
    q = Complaint.objects.all().last()
    subject = "New Complaint reported"
    message = f"""
Dear Authority,
A new complaint has been submitted. Here are the details:
Description: {q.desc}
Please find the attached image for reference.

Regards,
CityAssist
"""
                
    recepient_list = ["sonaryash1406@gmail.com","shubhamrsingh08@gmail.com"]
    file_path = f"{settings.BASE_DIR}/public/static/img.jpg"
    send_email_with_attachment(subject=subject,messsage=message,recepient_list=recepient_list,file_path=file_path)
    return redirect('/')



# def register_complaint(request):
#     if request.method == "POST":
#         # Fetch data from the form
#         data = request.POST
#         name = data.get("complaint_name")
#         complaint_description = data.get("complaint_description")
#         complaint_image = request.FILES.get("complaint_image")

#         # Save the complaint in the database
#         complaint = Complaint.objects.create(
#             name=name,
#             desc=complaint_description,
#             image=complaint_image
#         )
        
#         # Prepare email details
#         subject = "New Complaint Reported"
#         message = f"""
#         Dear Authority,

#         A new complaint has been submitted. Here are the details:
#         Description: {complaint.desc}

#         Please find the attached image for reference.

#         Regards,
#         CityAssist
#         """
#         recipient_list = ["sonaryash1406@gmail.com", "shubhamrsingh08@gmail.com"]

#         # Build the file path for the uploaded image
#         file_path = complaint.image.path

#         # Send email with the attachment
#         email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#         email.attach_file(file_path)  # Attach the uploaded file
#         email.send()

#         # Add a success message
#         messages.success(request, "Complaint registered and email sent successfully.")
        
#         return redirect("/")
#     return render(request, "register.html")

def register_complaint(request):
    if request.method == "POST":
        data = request.POST
        name = data.get("complaint_name")
        complaint_description = data.get("complaint_description")
        complaint_image = request.FILES.get("complaint_image")

        complaint = Complaint.objects.create(
            name=name,
            desc=complaint_description,
            image=complaint_image
        )
        
        subject = "New Complaint Reported"
        message = f"""
        Dear Authority,

        A new complaint has been submitted. Here are the details:
        Description: {complaint.desc}

        Please find the attached image for reference.

        Regards,
        CityAssist
        """
        recipient_list = ["sonaryash1406@gmail.com", "shubhamrsingh08@gmail.com"]

        file_path = complaint.image.path

        save_latest_image_as(file_path)

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        email.attach_file(file_path)  # Attach the uploaded file
        email.send()

        messages.success(request, "Complaint registered and email sent successfully.")
        
        return redirect("/")
    return render(request, "register.html")


def save_latest_image_as(original_file_path):
    """
    Utility function to fetch the latest image and save it as 'img.jpg'
    """
    destination_path = os.path.join(settings.MEDIA_ROOT, "img.jpg")
    
    with Image.open(original_file_path) as img:
        img.save(destination_path)