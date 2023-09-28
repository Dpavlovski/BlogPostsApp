from django.shortcuts import render, redirect
from .forms import *
# Create your views here.


def get_posts(request):
    qs = Blog.objects.all()
    context = {"blogs": qs}
    return render(request, "posts.html", context)


def add_post(request):
    if request.method == "POST":
        form_data = BlogForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            blog = form_data.save(commit=False)
            blog.author = UserProfile.objects.get(user=request.user)
            blog.save()
            return redirect("get_posts")
    return render(request, "BlogForm.html", {"form": BlogForm})


def get_user_profile(request):
    context = {"user": UserProfile.objects.get(user=request.user),
               "posts": Blog.objects.filter(author__user=request.user).all()}
    return render(request, "UserProfile.html", context)


def get_blocked_users(request):
    if request.method == "POST":
        form_data = BlockUserForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            block_user = form_data.save(commit=False)
            block_user.blocker = UserProfile.objects.get(user=request.user)
            block_user.save()
            return redirect("get_blocked_users")

    blocked_users = BlockUser.objects.filter(blocker__user=request.user)
    other_users = UserProfile.objects.exclude(user__in=blocked_users.values_list("blocked__user", flat=True))

    context = {
        "blocked_users": blocked_users,
        "other_users": other_users,
        "form": BlockUserForm(),
    }
    return render(request, "BlockedUsers.html", context)
