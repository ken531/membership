from django.shortcuts import render, redirect, HttpResponse
from .models import org
from apps.users.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime

def edit(request, org_id):
    if not 'uid' in request.session:
        messages.error(request, 'Please log in', extra_tags='log_in')
        return redirect ('/')
    Org = org.objects.get(id=org_id)
    context = {
        'organization': Org.organization,
        'description': Org.description,
        'org_id': Org.id,
        'user': User.objects.get(id=request.session['uid'])
    }
    return render(request, 'organization/edit.html', context)

def new(request):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags='log_in')
        return redirect ('/')
    user = User.objects.get(id=request.session['uid'])
    context = {
        'user': user.first_name,
    }
    return render(request, 'organization/new.html', context)

def org_info(request, org_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags='log_in')
        return redirect('/')
    Org = org.objects.get(id=org_id)
    user = User.objects.get(id=request.session['uid'])
    context = {
        "org": Org,
        'user': User.objects.get(id=request.session['uid']),
        'joining': Org.users.all().exclude(id=user.id)
    }
    return render(request, 'organization/org_info.html', context)

def create_org(request):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags='log_in')
        return redirect('/')

    errors = org.objects.validate_organization_creation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect ('/organization/new')

    userid=request.session['uid']
    org_id = org.objects.process_organization_creation(request.POST, userid)
    print(org_id)
    this_org = org.objects.get(id=org_id)
    this_org.users.add(User.objects.get(id=userid))
    return redirect ('/dashboard')

def remove(request, org_id):
    if not 'uid' in request.session:
        messages.error(request, 'Please log in', extra_tags='log_in')
        return redirect ('/')
    org.objects.get(id=org_id).delete()
    return redirect ('/dashboard')

def update_org(request, org_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags='log_in')
        return redirect('/')
    errors = org.objects.validate_organization_creation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'oganization/edit/{org_id}')
    org.objects.update_org(request.POST, org_id)
    return redirect ('/dashboard')

def cancel_joined(request, joined_id):
    if not 'uid' in request.session:
        messages.error(request, "Please log in", extra_tags='log_in')
        return redirect('/')
    user = User.objects.get(id=request.session['uid'])
    org.objects.get(id=joined_id).users.remove(user)
    return redirect('/dashboard')

def join_org(request, join_id):
    if not 'uid' in request.session:
        messages.error(request, 'Please log in', extra_tags='log_in')
        return redirect ('/')
    user = User.objects.get(id=request.session['uid'])
    org.objects.get(id=join_id).users.add(user)
    return redirect('/dashboard')