from django import template

register = template.Library()

cens = ['Редиска', 'Дурак', 'Плохой']


@register.filter(name='censor')
def censor(value):
    for word in cens:
        value = value.replace(word, word[0] + '*' * len(word))

    return value

