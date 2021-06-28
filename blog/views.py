from django import http
from django.contrib.auth import authenticate
from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
# Create your views here.
from .forms import SignUpForm,LoginForm,PostForm
from .models import Post

#HOME
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})



#ABOUT

def about(request):
    return render(request,'blog/about.html')


#CONTACT
def contact(request):
    return render(request,'blog/contact.html')

#DASHBOARD
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        ip=request.session.get('ip',0)
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'gps':gps,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')

#LOGOUT
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#SIGNUP
def user_signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            form=SignUpForm()
            messages.success(request,'Congratulations You are an author now')
            group=Group.objects.get(name="author")
            user.groups.add(group)

            
    else:
        form=SignUpForm()
    return render(request,'blog/signup.html',{'form':form})


#LOGIN
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"logged in successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


#ADD NEW POST

def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                form=PostForm()
                messages.success(request,"Post added successfully!!")
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#UPDATE POST

def update_post(request,id):
    if request.user.is_authenticated:
        obj=Post.objects.get(pk=id)
        if request.method=="POST":
            
            form=PostForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                messages.success(request,"Post Uppdated successfully!!!")
                form=PostForm()
        else:
            form=PostForm(instance=obj)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#DELETE POST
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            obj=Post.objects.get(pk=id)
            obj.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')




