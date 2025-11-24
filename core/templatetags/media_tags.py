from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def media_url(image_field):
    """Generate static URL for media files in production."""
    if not image_field or not image_field.name:
        return ''
    
    if settings.DEBUG:
        return image_field.url
    else:
        # In production, media files are served as static files
        return f"/static/{image_field.name}"
