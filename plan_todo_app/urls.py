from django.urls import path, include
from . import views
from . import views_lists
from . import views_auth
from . import views_detail

app_name = "plan_todo_app"

urlpatterns = [
    path("", views_lists.lists_index, name="index"),
    path("lists/", views_lists.lists_index, name="lists"),
    path("lists/<int:list_id>/", views_detail.list_detail, name="list_detail"),
    path("lists/<int:list_id>/add/", views_detail.add_todo, name="add"),
    path("lists/<int:list_id>/update/<int:todo_id>/", views_detail.update_todo, name="update"),
    path("lists/<int:list_id>/delete/<int:todo_id>/", views_detail.delete_todo, name="delete"),
    path("lists/<int:list_id>/toggle/<int:todo_id>/", views_detail.toggle_done, name="toggle"),
    path("lists/<int:list_id>/", views_lists.list_detail, name="list_detail"),
    path("lists/<int:list_id>/update/", views_lists.update_list, name="update_list"),
    path("lists/<int:list_id>/delete/", views_lists.delete_list, name="delete_list"),
    path("lists/create/", views_lists.create_list, name="create_list"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
    path("register/", views_auth.register, name="register"),
    path("add/", views.add_todo, name="add"),
    path("toggle/<int:todo_id>/", views.toggle_done, name="toggle"),
    path("update/<int:todo_id>/", views.update_todo, name="update"),
    path("delete/<int:todo_id>/", views.delete_todo, name="delete_todo"),
]