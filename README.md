# Team Project Planner Tool
This is tool for team project planner which consists of API's.

# Installation
1. Install VSCode
2. Inorder to install requirements.txt file run following command in root folder:
   pip3 freeze > requirements.txt

To run the application execute following commands in root folder
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver

# Description
This is Django project and goal is to implement API's for - 
1. Managing Users
2. Managing Teams
3. Managing team board and tasks within a board

# API Reference
For Users - 
http://localhost:8000/Users/ (Base URL).
You can navigate to users app within that urls.py to view endpoints for performing different tasks

For Teams - 
http://localhost:8000/Teams/ (Base URL).
You can navigate to teams app within that urls.py to view endpoints for performing different tasks

For TeamBoard and tasks within a board - 
http://localhost:8000/ProjectBoard/ (Base URL).
You can navigate to projectboard app within that urls.py to view endpoints for performing different tasks



