from django.shortcuts import render
from users.models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from teams.models import Team

# Create your views here.
class TeamBase(APIView):
    @api_view(['GET'])
    def list_all_teams(request):
        list_teams = Team.objects.all().values('teamname','description','creation_time','admin')
        return Response(list_teams)
    
    @api_view(['GET'])
    def describe_team(request):
        team_id = request.query_params.get('id')
        if not team_id:
            return Response("Team Id is required")
        team = Team.objects.filter(id=team_id).values('teamname','description','creation_time','admin')
        if not team:
            return Response("Team_Description not found")
        return Response(team)
    
    @api_view(['POST'])
    def create_team(request):
        teamname= request.data["teamname"]
        description = request.data["description"]
        admin = request.data["id"]
        if not teamname or not description:
            return Response("TeamName and Description are required")
        if Team.objects.filter(teamname=teamname).exists():
            return Response("Teamname already exists")
        if len(teamname) > 64:
            return Response("TeamName cannot be more than 64 characters")
        if len(description) > 128:
            return Response("Description cannot be more than 128 characters")
        try:
            admin_user = Users.objects.get(id=admin)
            print(admin_user)
        except Users.DoesNotExist:
            return Response("Admin user does not exist")
        new_team = Team.objects.create(teamname=teamname,description=description,admin=admin_user)              
        return Response({"id": new_team.id})
    
    @api_view(['PUT'])
    def update_team(request):
        team_id = request.data.get("id")
        team_data = request.data.get('team', {})
        if not team_id:
            return Response("Team ID is required")
        team = Team.objects.filter(id=team_id)
        if not team:
            return Response("Team not found")
        if 'teamname' in team_data and len(team_data['teamname']) > 64:
            return Response("Team Name cannot be more than 64 characters")
        if 'description' in team_data and len(team_data['description']) > 128:
            return Response("Description cannot be more than 128 characters")
        if 'admin' in team_data:
            admin_id = team_data['admin']
        try:
            admin = Users.objects.get(id=admin_id)
            team.admin = admin
        except Users.DoesNotExist:
            return Response("Admin user does not exist")
        team.teamname = team_data.get('teamname', team.teamname)
        team.description = team_data.get('description', team.description)
        team.save()
        return Response("User updated successfully")
    
    @api_view(['POST'])
    def add_users(request):
        team_id = request.data.get("id")
        user_ids = request.data.get("users", [])
        if not team_id:
            return Response("Team ID is required")
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response("Team not found")
        if len(user_ids) > 50:
            return Response("Maximum 50 users can be added at once")
        users_to_add = []
        for user_id in user_ids:
            try:
                user = Users.objects.get(id=user_id)
                users_to_add.append(user)
            except Users.DoesNotExist:
                return Response("User with ID {} does not exist" .format(user_id))
        for user in users_to_add:
            team.members.add(user)
        return Response("Users added to team successfully") 

    @api_view(['POST'])
    def remove_users(request):
        team_id = request.data.get("id")
        user_ids = request.data.get("users", [])
        if not team_id:
            return Response("Team ID is required")
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response("Team not found")
        if len(user_ids) > 50:
            return Response("Maximum 50 users can be removed at once")
        users_to_remove = []
        for user_id in user_ids:
            try:
                user = Users.objects.get(id=user_id)
                users_to_remove.append(user)
            except Users.DoesNotExist:
                return Response("User with ID {} does not exist" .format(user_id))
        for user in users_to_remove:
            team.members.remove(user)
        return Response("Users removed from team successfully")
    
    @api_view(['POST'])
    def list_team_users(request):
        team_id = request.data.get("id")
        if not team_id:
            return Response("Team ID is required")
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response("Team not found")
        team_users = []
        for user in team.members.all():
            user_info = {
                "id": user.id,
                "name": user.name,
                "display_name": user.display_name
            }
            team_users.append(user_info)
        return Response(team_users)
       