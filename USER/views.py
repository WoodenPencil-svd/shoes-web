from django.contrib import messages
from django.http import Http404
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def profile_view(request,username = None):
    profile = request.user.profile 
    return render(request,'USER/profile.html',{'profile': profile})

def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form =ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
         
    return render(request,'USER/profile_edit.html',{'form':form})


def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request,'Account delete')
        return redirect('home')
    return render(request,'USER/profile_delete.html')

