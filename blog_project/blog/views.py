from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

def healthz(request):
    return HttpResponse("ok")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # после регистрации отправляем на логин
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('post_list')
    return render(request, 'post_form.html', {'post': None})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужие посты!")
    
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("post_detail", pk=post.pk)
    
    return render(request, "post_form.html", {"post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалять чужие посты!")
    
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    
    return render(request, "post_confirm_delete.html", {"post": post})