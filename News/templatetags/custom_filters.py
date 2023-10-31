from django import template

register = template.Library()

@register.filter()
def censor(value):
    if type(value) is not str:
        raise ValueError

    bad_w = ['редиска','редиски','редиске','редиску','редиской']
    for word in value.split():
        if word.lower() in bad_w:
            value = value.replace(word, f"{word[0]}{'*'*(len(word)-2)}{word[-1]}")
    return value