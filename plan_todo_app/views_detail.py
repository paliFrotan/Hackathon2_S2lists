from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TodoCreateForm, TodoUpdateForm
from .models import List, Todo


def _owned_list_or_404(user, list_id: int) -> List:
    return get_object_or_404(List, pk=list_id, owner=user)


@login_required
def list_detail(request, list_id: int):
    todo_list = _owned_list_or_404(request.user, list_id)

    filter_value = request.GET.get("filter", "all")   # all | active | done
    sort_value = request.GET.get("sort", "added_desc")  # added_desc|added_asc|due_asc|due_desc

    qs = Todo.objects.filter(todo_list=todo_list)

    if filter_value == "active":
        qs = qs.filter(is_done=False)
    elif filter_value == "done":
        qs = qs.filter(is_done=True)

    if sort_value == "added_asc":
        qs = qs.order_by("created_at")
    elif sort_value == "added_desc":
        qs = qs.order_by("-created_at")
    elif sort_value == "due_asc":
        qs = qs.order_by("due_date", "-created_at")
    elif sort_value == "due_desc":
        qs = qs.order_by("-due_date", "-created_at")

    create_form = TodoCreateForm()

    edit_id = request.GET.get("edit")
    edit_todo = None
    edit_form = None
    if edit_id:
        edit_todo = get_object_or_404(Todo, pk=edit_id, todo_list=todo_list)
        edit_form = TodoUpdateForm(instance=edit_todo)

    return render(
        request,
        "plan_todo_app/list_detail.html",
        {
            "todo_list": todo_list,
            "todos": qs,
            "create_form": create_form,
            "filter_value": filter_value,
            "sort_value": sort_value,
            "edit_todo": edit_todo,
            "edit_form": edit_form,
        },
    )


@login_required
@require_POST
def add_todo(request, list_id: int):
    todo_list = _owned_list_or_404(request.user, list_id)
    form = TodoCreateForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.owner = request.user
        todo.todo_list = todo_list
        todo.save()
    return redirect("plan_todo_app:list_detail", list_id=todo_list.id)


@login_required
@require_POST
def toggle_done(request, list_id: int, todo_id: int):
    todo_list = _owned_list_or_404(request.user, list_id)
    todo = get_object_or_404(Todo, pk=todo_id, todo_list=todo_list)
    todo.is_done = not todo.is_done
    todo.save(update_fields=["is_done"])
    return redirect("plan_todo_app:list_detail", list_id=todo_list.id)


@login_required
@require_POST
def update_todo(request, list_id: int, todo_id: int):
    todo_list = _owned_list_or_404(request.user, list_id)
    todo = get_object_or_404(Todo, pk=todo_id, todo_list=todo_list)
    form = TodoUpdateForm(request.POST, instance=todo)
    if form.is_valid():
        form.save()
    return redirect("plan_todo_app:list_detail", list_id=todo_list.id)


@login_required
@require_POST
def delete_todo(request, list_id: int, todo_id: int):
    todo_list = _owned_list_or_404(request.user, list_id)
    todo = get_object_or_404(Todo, pk=todo_id, todo_list=todo_list)
    todo.delete()
    return redirect("plan_todo_app:list_detail", list_id=todo_list.id)