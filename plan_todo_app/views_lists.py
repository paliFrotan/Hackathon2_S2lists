from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from .models import List

from django.views.decorators.http import require_http_methods

from .models import Todo


@login_required
def lists_index(request):
    lists = List.objects.filter(owner=request.user).order_by("name")
    return render(request, "plan_todo_app/lists.html", {"lists": lists})


@login_required
@require_POST
def create_list(request):
    title = (request.POST.get("title") or request.POST.get("name") or "").strip()
    if not title:
        messages.error(request, "List title is required.")
        lists = List.objects.filter(owner=request.user).order_by("name")
        return render(
            request,
            "plan_todo_app/lists.html",
            {"lists": lists, "list_error": "List title is required."},
        )

    todo_list = List.objects.create(name=title, owner=request.user)
    messages.success(request, f"List '{todo_list.name}' created.")
    return redirect("plan_todo_app:list_detail", list_id=todo_list.id)

def list_detail(request, list_id):
    list_obj = get_object_or_404(List, pk=list_id)
    todos = Todo.objects.filter(todo_list=list_obj)
    return render(request, "plan_todo_app/list_detail.html", {
        "todo_list": list_obj,
        "todos": todos,
    })

@login_required
@require_http_methods(["GET", "POST"])
def create_list_page(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        title = (request.POST.get("title") or request.POST.get("name") or "").strip()
        if title:
            todo_list = List.objects.create(name=title, owner=request.user)
            messages.success(request, f"List '{todo_list.name}' created.")

            # Prefer safe `next`, otherwise go to the new list
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("plan_todo_app:list_detail", list_id=todo_list.id)
        messages.error(request, "List title is required.")
    else:
        pass

    return render(request, "plan_todo_app/create_list.html", {"next": next_url})