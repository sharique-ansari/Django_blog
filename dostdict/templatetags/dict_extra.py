from django import template

register = template.Library()


@register.filter
def index(word, i):
    try:
        word=str(word)
        return word[int(i)]
    except IndexError:
        return