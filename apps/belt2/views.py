from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def register(request):
    result = User.objects.regValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result['user_id']
    return redirect('/wall')

def login(request):
    result = User.objects.loginValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result['user_id']
    return redirect('/wall')


def wall(request):
    all_jobs = Job.objects.all()
    if 'user_id' not in request.session:
        return redirect('/')
    current_user= User.objects.get(id = request.session['user_id'])
    context = {
        'current_user' : current_user,
        'all_jobs' : all_jobs, 
    }
    return render(request, 'wall.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

# -------------------start jobs stuff ----------------------------

def addjob(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'addjob.html')

def createjob(request):
    for x in request.POST:
        print(x, " is ", request.POST[x])
    result = Job.objects.jobaddValidator(request.POST)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/addjob')
    return redirect('/wall')

def edit(request, id ):
    if 'user_id' not in request.session:
        return redirect('/')
    this_job = Job.objects.get(id=id)
    current_user= User.objects.get(id = request.session['user_id'])
    if current_user.id != this_job.owner.id:
        return redirect('/wall') 
    context = {
        'this_job' : this_job,         
    }    
    return render(request, 'edit.html',context)

def editjob(request, id ):
    if 'user_id' not in request.session:
        return redirect('/')
    result = Job.objects.editValidator(request.POST, id)
    if len(result['errors']) > 0:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/edit/'+str(id))
    return redirect('/wall')

def show(request , id ):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user= User.objects.get(id = request.session['user_id'])
    this_job = Job.objects.get(id=id)
    context = {
        'this_job': this_job,
        'current_user': current_user,
    }
    return render(request, 'view.html',context )

def takejob(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_job = Job.objects.get(id=id)
    if this_job.worker != None:
        messages.error(request, "You cannot do that")
        return redirect('/wall')
    current_user= User.objects.get(id = request.session['user_id'])
    this_job.worker = current_user 
    this_job.save()
    return redirect('/wall')


def destroy(request, id):
    this_job = Job.objects.get(id=id)
    this_job.delete()
    return redirect('/wall')

