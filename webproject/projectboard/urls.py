from django.urls import path
from projectboard.views import ProjectBoard

urlpatterns = [
  path('create/',ProjectBoard.create_board,name="create"),
  path('close/',ProjectBoard.close_board,name="close"),
  path('add/',ProjectBoard.add_task,name="add_task"),
  path('update/',ProjectBoard.update_task_status,name="update"),
  path('list/',ProjectBoard.list_boards,name="list_boards"),
  path('export/',ProjectBoard.export_board,name="export"),
]