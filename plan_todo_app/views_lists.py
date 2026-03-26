from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from .models import List
from .models import Todo
# Inline update view for a list
@login_required
@require_http_methods(["POST"])
def update_list(request, list_id):
    list_obj = get_object_or_404(List, pk=list_id, owner=request.user)
    new_name = request.POST.get("name", "").strip()
    if new_name:
        list_obj.name = new_name
        list_obj.save()
    return redirect('plan_todo_app:lists')

# Delete view for a list
@login_required
@require_http_methods(["POST"])
def delete_list(request, list_id):
    list_obj = get_object_or_404(List, pk=list_id, owner=request.user)
    list_obj.delete()
    return redirect('plan_todo_app:lists')



@login_required
def lists_index(request):
    lists = List.objects.filter(owner=request.user).order_by("name")
    return render(request, "plan_todo_app/lists.html", {"lists": lists})


@login_required
@require_POST
def create_list(request):
    title = (request.POST.get("title") or request.POST.get("name") or "").strip()
    if not title:
        lists = List.objects.filter(owner=request.user).order_by("name")
        return render(
            request,
            "plan_todo_app/lists.html",
            {"lists": lists, "list_error": "List title is required."},
        )

    todo_list = List.objects.create(name=title, owner=request.user)
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

            # Prefer safe `next`, otherwise go to the new list
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("plan_todo_app:list_detail", list_id=todo_list.id)
    else:
        pass

    return render(request, "plan_todo_app/create_list.html", {"next": next_url})