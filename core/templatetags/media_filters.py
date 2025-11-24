from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_to_static(url):
    """Convert media URL to static URL in production."""
    if not url:
        return url
    
    if settings.DEBUG:
        return url  # Keep /media/ in development
    else:
        # Convert /media/unknown_mushrooms/ to /static/unknown_mushrooms/
        return url.replace('/media/unknown_mushrooms/', '/static/unknown_mushrooms/')
