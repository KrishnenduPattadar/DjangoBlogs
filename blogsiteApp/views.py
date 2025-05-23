from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, BlogPostForm
from .models import BlogPost
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            messages.success(request, 'Registration successful! You can now log in.') ######
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'blogsiteApp/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            return render(request, 'blogsiteApp/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'blogsiteApp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blogsiteApp/dashboard.html', {'blogs': blogs})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Post published successfully!')
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blogsiteApp/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, user=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'blogsiteApp/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('dashboard')
    return render(request, 'blogsiteApp/delete_post.html', {'blog': blog})
