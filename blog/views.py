from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm,CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test


def home(request):
    return render(request,'blog/home.html')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request,pk):
    post= get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
@user_passes_test(lambda u: u.has_perm('blog.can_delete_Post'))
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            print(request.user)
            post.auther = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.has_perm('blog.can_delete_Post'))
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.has_perm('blog.can_delete_Post'))
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    for post in posts:
        print(post.title)
    return render(request,'blog/post_draft_list.html',{'posts' : posts})


@login_required
@user_passes_test(lambda u: u.has_perm('blog.can_delete_Post'))
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
@user_passes_test(lambda u: u.has_perm('blog.can_delete_Post'))
def post_delete(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

# Create your views here.
