from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth import authenticate, login, logout   # <-- missing imports added
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}.")

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("plan_todo_app:lists")

        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "plan_todo_app/login.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
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
            messages.success(request, "Account created successfully.")

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
             return redirect(next_url)

            return redirect("plan_todo_app:lists")
        messages.error(request, "Could not create account. Please fix the form errors.")
    else:
        form = UserCreationForm()

    return render(request, "plan_todo_app/register.html", {"form": form, "next": next_url})
