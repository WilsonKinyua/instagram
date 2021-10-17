from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api
# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    # get all the images from the database and order them by the date they were created
    images = Image.objects.all().order_by('-image_date')
    return render(request, 'index.html', {'images': images})


# profile page
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    # get images for the current logged in user
    images = Image.objects.filter(user_id=current_user.id)
    # get the profile of the current logged in user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"images": images, "profile": profile})
    # return render(request, 'profile.html')


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
        return redirect('/profile', {'success': 'Image Uploaded Successfully'})
        # return render(request, 'profile.html', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Image Upload Failed'})


# update profile with first name,last name,username,email and upload profile image to cloudinary
@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_url
            profile.bio = bio
            profile.save()
        else:
            profile = Profile(user_id=current_user.id,
                              profile_photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Profile Updated Successfully'})

        # return render(request, 'profile.html', {'success': 'Profile Updated Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Profile Update Failed'})


# like image
@login_required(login_url='/accounts/login/')
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()
    # check if the user has already liked the image
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        # unlike the image
        likes.delete()
        # reduce the number of likes by 1 for the image
        image = Image.objects.get(id=id)
        # check if the image like_count is equal to 0
        if image.like_count == 0:
            image.like_count = 0
            image.save()
        else:
            image.like_count -= 1
            image.save()
        return redirect('/')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        # increase the number of likes by 1 for the image
        image = Image.objects.get(id=id)
        image.like_count = image.like_count + 1
        image.save()
        return redirect('/')


# single image page with comments
@login_required(login_url='/accounts/login/')
def single_image(request, id):
    image = Image.objects.get(id=id)
    # get related images to the image that is being viewed by the user and order them by the date they were created
    related_images = Image.objects.filter(
        user_id=image.user_id).order_by('-image_date')
    title = image.image_name
    # check if image exists
    if Image.objects.filter(id=id).exists():
        # get all the comments for the image
        comments = Comments.objects.filter(image_id=id)
        return render(request, 'picture.html', {'image': image, 'comments': comments, 'images': related_images, 'title': title})
    else:
        return redirect('/')


# save comment
@login_required(login_url='/accounts/login/')
def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Image.objects.get(id=image_id)
        user = request.user
        comment = Comments(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        # increase the number of comments by 1 for the image
        image.comment_count = image.comment_count + 1
        image.save()
        return redirect('/picture/' + str(image_id))
    else:
        return redirect('/')


# user profile page with images
@login_required(login_url='/accounts/login/')
def user_profile(request, id):
    # check if user exists
    if User.objects.filter(id=id).exists():
        # get the user
        user = User.objects.get(id=id)
        # get all the images for the user
        images = Image.objects.filter(user_id=id)
        # get the profile of the user
        profile = Profile.objects.filter(user_id=id).first()
        return render(request, 'user-profile.html', {'images': images, 'profile': profile, 'user': user})
    else:
        return redirect('/')


# search for images
@login_required(login_url='/accounts/login/')
def search_images(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        images = Image.search_by_image_name(search_term)
        message = f'{search_term}'
        title = message

        return render(request, 'search.html', {'success': message, 'images': images})
    else:
        message = 'You havent searched for any term'
        return render(request, 'search.html', {'danger': message})