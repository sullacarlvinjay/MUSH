from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_to_static(url):
    """Convert media URL to static URL in production."""
    if not url:
        return url
    
    if settings.DEBUG:
        return url
    else:
        # Convert /media/ to /static/ in production
        return url.replace('/media/', '/static/')
