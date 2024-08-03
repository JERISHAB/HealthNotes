from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse



# View to display all blog posts that are not drafts
def blog_post_list(request):
    category = request.GET.get('category')  # Get the selected category from query parameters
    if category:
        posts = BlogPost.objects.filter(category=category, is_draft=False).order_by('-created_at')
    else:
        posts = BlogPost.objects.filter(is_draft=False).order_by('-created_at')

    categories = BlogPost.CATEGORIES  # Get categories from the BlogPost model
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/blog_post_list.html', context)




# View to display details of a single blog post
def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/blog_post_detail.html', {'post': post})



# View to create a new blog post (requires login)
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        print("form is valid")
        if form.is_valid():
            print("form is valid")
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Link to the logged-in user
            blog_post.save()
            return redirect('blog:blog_post_list')
        else:
            # Handle form errors
            print(form.errors)
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})



# View to edit an existing blog post (requires login)
@login_required
def edit_blog_post(request, pk=None):
    if pk:
        # Editing an existing post
        post = get_object_or_404(BlogPost, pk=pk)
        form_action_url = reverse('blog:edit_blog_post', kwargs={'pk': pk})
    else:
        # Creating a new post
        post = None
        form_action_url = reverse('blog:create_blog_post')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('user:dashboard')  # Or the appropriate redirection
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blog/edit_blog_post.html', {
        'form': form,
        'post': post,
        'form_action_url': form_action_url
    })


@login_required
def delete_blog_post_confirm(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('user:dashboard')  # Redirect to dashboard after deletion
    
    return render(request, 'blog/delete_blog_post_confirm.html', {'post': post})



@login_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('user:dashboard')  # Redirect to the appropriate page
    else:
        return redirect('blog:delete_blog_post_confirm', pk=pk)