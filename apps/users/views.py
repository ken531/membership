from django.shortcuts import render, redirect, HttpResponse
from .models import User
from apps.organization.models import org
from django.contrib import messages

def index(request):
    return render(request, 'users/index.html')

def register_user(request):
    # validate user information
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")

    # register user
    request.session['uid'] = User.objects.register_user(request.POST)
    # request.session['hashed_uid'] = User.objects.hash_id(request.session['uid'])
    return redirect("/dashboard")

def login(request):
    # validate login info
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")

    # login
    request.session['uid'] = User.objects.get(email=request.POST['email']).id
    # request.session['hashed_uid'] = str(User.objects.hash_id(request.session['uid']))
    return redirect("/dashboard")

def user_page(request, uid):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    # check if it's correct user
    # hashed = request.session['hashed_uid']
    # if not User.objects.user_validator(uid, hashed):
    #     return redirect("/")
    user_info = User.objects.get_user_info(uid)
    context={
        "fname": user_info.first_name,
        "lname": user_info.last_name,
        "em": user_info.email,
        # "reviews": len(user_info.reviews.all()),
        # "reviewed_books": user_info.reviews.all(),
    }
    return render(request, "/login/user.html", context)

# region dashboard related
def dashboard(request):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags="log_in")
        return redirect("/")
    user = User.objects.get(id=request.session['uid'])
    context={
        "user": user,
        "user_org": user.created_organization.all(),
        "org_joined": org.objects.all().filter(users=user).exclude(creator=user),
        "org": org.objects.all().exclude(creator__id=request.session['uid']).exclude(users=user)
    }
    return render (request, 'users/dashboard.html', context)

# endregion

def logout(request):
    keys = []
    for key in request.session.keys():
        keys.append(key)
    for key in keys:
        del request.session[key]
    return redirect("/")
