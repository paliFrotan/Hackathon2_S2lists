from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import TodoCreateForm, TodoUpdateForm
from .models import Todo


@login_required
def index(request):
    filter_value = request.GET.get("filter", "all")
    sort_value = request.GET.get("sort", "added_desc")

    qs = Todo.objects.filter(owner=request.user)

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
        edit_todo = get_object_or_404(Todo, pk=edit_id)
        edit_form = TodoUpdateForm(instance=edit_todo)

    return render(
        request,
        "plan_todo_app/index.html",
        {
            "todos": qs,
            "create_form": create_form,
            "filter_value": filter_value,
            "sort_value": sort_value,
            "edit_todo": edit_todo,
            "edit_form": edit_form,
        },
    )


@require_POST
@login_required
def add_todo(request):
    form = TodoCreateForm(request.POST)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.owner = request.user
        todo.save()
    return redirect("plan_todo_app:index")


@require_POST
@login_required
def toggle_done(request, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id, owner=request.user)
    todo.is_done = not todo.is_done
    todo.save(update_fields=["is_done"])
    return redirect("plan_todo_app:index")


@require_POST
@login_required
def update_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id, owner=request.user)
    form = TodoUpdateForm(request.POST, instance=todo)
    if form.is_valid():
        form.save()
    return redirect("plan_todo_app:index")

def lists(request):
    # your logic here
    return render(request, 'plan_todo_app/lists.html')


@require_POST
@login_required
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id, owner=request.user)
    todo.delete()
    return redirect("plan_todo_app:index")