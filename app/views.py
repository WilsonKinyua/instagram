from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


# profile page
@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'profile.html')


# save image  with image name,image caption and upload image to cloudinary
@login_required(login_url='/accounts/login/')
def save_image(request):
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']
        image_public_id = image_file['public_id']
        image = Image(image_name=image_name, image_caption=image_caption, image=image_url,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()
        # redirect with success message
        return render(request, 'profile.html', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html')
