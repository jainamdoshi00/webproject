from django.shortcuts import render
from rest_framework.views import APIView                                #create class and inherit APIVIEW class to use its functionality.
from rest_framework.response import Response
from .models import Users
from teams.models import Team
from rest_framework.decorators import api_view


# Create your views here.

class UserBase(APIView):
    @api_view(['GET'])                                                   #telling Django REST Framework that this function is a view function capable of handling GET requests.
    def list_all_users(request):
        all_user = Users.objects.all().values('name','display_name','creation_time')
        return Response(all_user)
    
    @api_view(['GET'])
    def describe_user(request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response("User Id is required")
        user = Users.objects.filter(id=user_id).values('name','description_of_user','creation_time')
        if not user:
            return Response("User not found")
        return Response(user)
    
    @api_view(['POST'])
    def create_user(request):
        username = request.data["username"]
        name = request.data["name"]
        display_name = request.data["display_name"]
        description_of_user = request.data["description_of_user"]
        if not name or not display_name or not username:
            return Response("Name, Display Name and Username are required")
        if Users.objects.filter(username=username).exists():
            return Response("Username already exists")
        if len(name) > 64:
            return Response("Name cannot be more than 64 characters")
        if len(display_name) > 64:
            return Response("Display name cannot be more than 64 characters")
        if Users.objects.filter(name=name).exists():
            return Response("Username already exists")
        new_user = Users.objects.create(username=username,name=name, display_name=display_name,description_of_user=description_of_user)              #creating user
        return Response({"id": new_user.id})
    
    @api_view(['PUT'])
    def update_user(request):
        user_id = request.data.get("id")
        user_data = request.data.get('user', {})
        if not user_id:
            return Response("User ID is required")
        user = Users.objects.filter(id=user_id)
        if not user:
            return Response("User not found")
        if 'name' in user_data and len(user_data['name']) > 64:
            return Response("Name cannot be more than 64 characters")
        if 'display_name' in user_data and len(user_data['display_name']) > 128:
            return Response("Display name cannot be more than 128 characters")
        user.name = user_data.get('name', user.name)
        user.display_name = user_data.get('display_name', user.display_name)
        user.save()
        return Response("User updated successfully")
    
    @api_view(['GET'])
    def get_user_teams(request):
        user_id = request.data.get('id')
        if not user_id:
            return Response('User ID is required')
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response('User with id {} does not exist' .format(user_id))
        user_teams = Team.objects.filter(admin=user) | Team.objects.filter(members=user)
        team_list = []
        for team in user_teams:
            team_info = {
                'name': team.teamname,
                'description': team.description,
                'creation_time': team.creation_time
            }
            team_list.append(team_info)
        return Response(team_list)
    