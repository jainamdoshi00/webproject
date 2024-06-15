from django.urls import path
from users.views import UserBase

urlpatterns = [
    path('',UserBase.list_all_users,name="get_all_users"),
    path('describe/',UserBase.describe_user,name="description"),
    path('create/',UserBase.create_user,name="creating_user"),
    path('update/',UserBase.update_user,name="updating_user_details"),
    path('getuserteams/',UserBase.get_user_teams,name="get_user_teams")
]