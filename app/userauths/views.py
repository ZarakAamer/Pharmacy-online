from core.views import get_direction, get_language
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from userauths.forms import ProfileForm, UserRegisterForm
from userauths.models import User


def register_view(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        if User.objects.filter(username=username).exists():

            messages.warning(
                request,
                f"Hey {username}, account with username {username} already exist.",
            )
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
            }
            return render(request, "userauths/sign-up.html", context)
        elif User.objects.filter(
                email=email).exists():
            messages.warning(
                request,
                f"Hey {username}, account with email {email} already exist.",
            )
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
            }
        elif User.objects.filter(phone=phone).exists():
            messages.warning(
                request,
                f"Hey {username}, account with phone number {phone} already exist.",
            )
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
            }
        else:
            user = User(first_name=first_name, last_name=last_name,
                        username=username, phone=phone, email=email)
            user.set_password(password1)
            user.save()
            new_user = authenticate(
                username=phone,
                password=password1,
            )
            login(request, new_user)
            return redirect("index")
    else:
        context = {
            "current_lang": get_language(),
            "dir": get_direction(),
        }
        return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("index")

    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user = User.objects.get(phone=phone)
            user = authenticate(request, phone=phone, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("index")
            else:
                messages.warning(
                    request, "User Does Not Exist, create an account."
                )

        except:
            messages.warning(request, f"User with {phone} does not exist")

    return render(
        request,
        "userauths/sign-in.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def logout_view(request):

    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")


def profile_update(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("dashboard")

    form = ProfileForm(instance=user)
    context = {
        "dir": get_direction(),
        "current_lang": get_language(),
        "form": form,
        "profile": user,
    }

    return render(request, "userauths/profile-edit.html", context)
