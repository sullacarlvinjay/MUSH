from django import template

register = template.Library()

@register.simple_tag
def media_url(image_field):
    """Return the URL of an uploaded file from whichever storage holds it."""
    if not image_field or not image_field.name:
        return ''
    return image_field.url
