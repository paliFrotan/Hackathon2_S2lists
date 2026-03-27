from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth import authenticate, login, logout   # <-- missing imports added
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
    else:
        form = AuthenticationForm()
        return render(request, "plan_todo_app/login.html", {"form": form})

    if user:
            login(request, user)
            return redirect("plan_todo_app:lists")

        # Invalid login → re-render with error
    return render(request, "plan_todo_app/login.html", {
            "error": "Invalid username or password"
        })

    # IMPORTANT: handle GET request
    return render(request, "plan_todo_app/login.html")


def logout_view(request):
    logout(request)
    return redirect("plan_todo_app:login")


def register(request):
    if request.user.is_authenticated:
        return redirect("plan_todo_app:lists")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
             return redirect(next_url)

            return redirect("plan_todo_app:lists")
    else:
        form = UserCreationForm()

    return render(request, "plan_todo_app/register.html", {"form": form, "next": next_url})
