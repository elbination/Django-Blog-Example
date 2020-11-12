from django import template
from ..models import Post

# Simple tag to retrieve the total posts published on the blog

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


# Display latest posts
@register.inclusion_tag('blog/_components/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
