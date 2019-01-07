from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentCreateForm

def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'mainview/posts.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'mainview/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mainview:home')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('mainview:home')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    def get_success_url(self):
        return reverse('mainview:home')

def PostDetailView(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-date_posted')
    print(comments)
    data = {
        'post': post,
        'author': post.author,
        'date_posted': post.date_posted,
        'content': post.content,
        'comments': comments,
    }
    return render(request, 'mainview/post_detail.html', data)

def CreateComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)

        if form.is_valid():
            print(request.user.pk)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            
            #messages.success(request, f'Your comment was created.')
            return redirect('mainview:post-detail', pk)
    else:
        form = CommentCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'mainview/comment_form.html', context)