from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# Simple tag to retrieve the total posts published on the blog
register = template.Library()


# Count posts
@register.simple_tag
def total_posts():
    return Post.published.count()


# Display latest posts
@register.inclusion_tag('blog/_components/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Display most commented posts
@register.simple_tag
def show_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return most_commented_posts


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
