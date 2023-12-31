from django.urls import path
from .views import home,sign_in, signout,list_instructors, add_course, assign_lecture,add_batch

urlpatterns = [
    path("home/", home,name="home"),
    path("sign-in/", sign_in,name="sign_in"),
    path("sign-out/", signout,name="sign_out"),
    path('instructors/', list_instructors, name='instructors'),
    path('add_course/', add_course, name='add_course'),
    path('add_batch/',add_batch , name='add_batch'),
    path('assign_lecture/', assign_lecture, name='assign_lecture'),
]
