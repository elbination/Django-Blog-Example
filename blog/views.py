from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .forms import CommentForm
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# Create your views here.
def post_list(request):
    published_posts = Post.published.all()
    paginator = Paginator(published_posts, 2)  # 2 posts each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
    }
    return render(request, 'blog/post/list.html', context=context)


def post_detail(request, year, month, day, slug):
    # Retrieve the objects that matches given params
    # or an 404 exception if no object is found
    post = get_object_or_404(Post,
                             slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    # Using the related_name attribute of the relationship in the Comment model
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():  # If the form is valid
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post  # Specify the new comment belongs to this post
            # Save the comment to the database
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been added')
            return HttpResponseRedirect(reverse('blog:post_detail', args=[year, month, day, slug]
                                                ))
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'blog/post/detail.html', context=context)
