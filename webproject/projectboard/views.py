from django.shortcuts import render
from rest_framework.views import APIView                                #create class and inherit APIVIEW class to use its functionality.
from rest_framework.response import Response
from .models import Team,Boardmodel,TaskModel
from rest_framework.decorators import api_view
from django.utils import timezone
import os

# Create your views here.
class ProjectBoard(APIView):
    @api_view(['POST'])
    def create_board(request):
        board_name = request.data.get("name")
        description = request.data.get("description")
        team_id = request.data.get("team_id")
        creation_time = request.data.get("creation_time")
        
        if not (board_name and description and team_id):
            return Response("Board name, description, and team ID are required")
        
        if len(board_name) > 64:
            return Response("Board name cannot be more than 64 characters")
        
        if len(description) > 128:
            return Response("Description cannot be more than 128 characters")
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response("Team does not exist")
        if Boardmodel.objects.filter(boardname=board_name, team=team).exists():
            return Response("Board name {} already exists for the team" .format(board_name))
        new_board = Boardmodel.objects.create(
            boardname=board_name,
            description=description,
            team=team,
            creationtime=creation_time
        )   
        return Response({"id": new_board.id})
    
    @api_view(['POST'])
    def close_board(request):
        board_id = request.data.get("id")
        if not board_id:
            return Response("Board ID is required")
        try:
            board = Boardmodel.objects.get(id=board_id)
        except Boardmodel.DoesNotExist:
            return Response("Board not found")
        
        # Check if the board status allows closure
        if board.status == 'closed':
            return Response("Board is already closed")
        
        # Check if all tasks are marked as COMPLETE
        incomplete_tasks = TaskModel.objects.filter(user_id=board.team, status__in=['open', 'inprogress'])
        if incomplete_tasks.exists():
            return Response("Cannot close board: Some tasks are not complete")
        
        # Update board status to CLOSED and record end time
        board.status = 'closed'
        board.creationtime = timezone.now()  
        board.save()
        
        return Response({"message": f"Board {board_id} closed successfully"})

    @api_view(['POST'])
    def add_task(request):
        title = request.data.get("title")
        description = request.data.get("description")
        user_id = request.data.get("user_id")
        creation_time = request.data.get("creation_time")
        
        if not (title and description and user_id):
            return Response("Task title, description, and user ID are required")
        
        if len(title) > 64:
            return Response("Task title cannot be more than 64 characters")
        
        if len(description) > 128:
            return Response("Description cannot be more than 128 characters")
        
        # Check if the board exists and is open
        try:
            board = Boardmodel.objects.get(team=user_id, status='open')
        except Boardmodel.DoesNotExist:
            return Response("Cannot add task: Board does not exist or is not open")
        
        # Check if the task title is unique for the board
        if TaskModel.objects.filter(title=title, user_id=user_id).exists():
            return Response({"error": f"Task title '{title}' already exists for the board"})
        
        # Create the TaskModel instance
        new_task = TaskModel.objects.create(
            title=title,
            description=description,
            user_id=user_id,
            creationtime=creation_time
        )
        return Response({"id": new_task.id})
    
    @api_view(['PUT'])
    def update_task_status(request):
        task_id = request.data.get("id")
        status = request.data.get("status")
        
        if not (task_id and status):
            return Response("Task ID and status are required")
        
        # Validate status
        valid_statuses = ['open', 'inprogress', 'complete']
        if status.lower() not in valid_statuses:
            return Response("Invalid status. Must be one of: OPEN, IN_PROGRESS, COMPLETE")
        
        # Retrieve the TaskModel instance
        try:
            task = TaskModel.objects.get(id=task_id)
        except TaskModel.DoesNotExist:
            return Response("Task not found")
        
        # Update task status
        task.status = status.lower()
        task.save()

    @api_view(['POST'])
    def list_boards(request):
        team_id = request.data.get("id")
        if not team_id:
            return Response("Team ID is required")
        
        # Retrieve all open boards for the team
        boards = Boardmodel.objects.filter(team=team_id, status='open')
        
        # Format the response as a list of dictionaries
        boards_list = []
        for board in boards:
            board_info = {
                "id": board.id,
                "name": board.boardname
            }
            boards_list.append(board_info)
        
        return Response(boards_list)    
    
    @api_view(['POST'])
    def export_board(request):
        board_id = request.data.get("id")
        
        if not board_id:
            return Response("Board ID is required")
        
        # Retrieve the board and its tasks
        try:
            board = Boardmodel.objects.get(id=board_id)
            tasks = TaskModel.objects.filter(user_id=board.team)
        except Boardmodel.DoesNotExist:
            return Response("Board not found")
        
        # Prepare the content to export
        content = f"Board Name: {board.boardname}\n"
        content += f"Description: {board.description}\n\n"
        content += "Tasks:\n"
        
        for task in tasks:
            content += f"- {task.title}\n"
            content += f"  Description: {task.description}\n"
            content += f"  Status: {task.status.capitalize()}\n\n"
        
        # Create a txt file in the out folder
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
        os.makedirs(out_dir, exist_ok=True)
        out_file = f"board_{board_id}_export.txt"
        out_path = os.path.join(out_dir, out_file)
        
        with open(out_path, 'w') as f:
            f.write(content)
        
        return Response({"out_file": out_file})