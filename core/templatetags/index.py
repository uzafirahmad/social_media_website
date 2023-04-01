from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

def get_text(Queryset):
    return Queryset.post_text