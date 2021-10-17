from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('upload/add/', views.save_image, name='save.image'),
    path('profile/update/', views.update_profile, name='update.profile'),
    path('like/<int:id>/', views.like_image, name='like.image'),
    path('picture/<int:id>/', views.single_image, name='single.image'),
    path('comment/add', views.save_comment, name='comment.add'),
    path('user/<int:id>/', views.user_profile, name='user.profile'),
    path('search/', views.search_images, name='search.images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
