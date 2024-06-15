from django.urls import path
from teams.views import TeamBase
urlpatterns = [
  path('',TeamBase.list_all_teams,name="list_all_teams"),
  path('describe/',TeamBase.describe_team,name="description"),
  path('create/',TeamBase.create_team,name="create"),
  path('add/',TeamBase.add_users,name="add users"),
  path('remove/',TeamBase.remove_users,name="remove_users"),
  path('teamusers/',TeamBase.list_team_users,name="list_team_users"),
]