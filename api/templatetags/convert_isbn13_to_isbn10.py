#参考記事 https://note.com/k1ro/n/nd0fae64fff33



from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter(name='stars')
def convert_to_isbn13_to_isbn10():
  pass




def checkdigit(code):
    s = str(code)[:12]
    a = 0
    b = 0

    for i in range(0, len(s), 2):
        a += int(s[i])
    #print a

    for i in range(1, len(s), 2):
        b += int(s[i])
    #print b

    d = (a + (b * 3)) % 10
    d = 10 - d 
    if d == 10:
        d = 0
    return d