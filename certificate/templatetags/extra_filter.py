from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def linebreak_to_row(value):
    msg = ''
    items = linebreaksbr(value)
    # print('items',items.split("<br>"))
    dictionary = [subString.split(":",1) for subString in items.split("<br>")]
    for item in dictionary:
        if len(item) < 2:
            item.insert("")
        msg += format_html(
            '<tr><td><b>{}</b></td><td>:</td><td style="text-align:left"><span class="">{}</span></td></tr>',
            mark_safe(item[0]), mark_safe(item[1]))
    return mark_safe(msg)

    # for x, y in dictionary.items():
    #     msg += format_html(
    #         '<tr><td><b>{}</b></td><td>:</td><td style="text-align:left"><span class="">{}</span></td></tr>', mark_safe(x), mark_safe(y))
    # return mark_safe(msg)


@register.filter
def linebreak_to_web_row(value):
    msg = ''
    items = linebreaksbr(value)
    dictionary = [subString.split(":",1) for subString in items.split("<br>")]

    for item in dictionary:
        if len(item) < 2:
            item.insert("")
        msg += format_html(
            '<tr><td class="green">{}</td><td style="text-align:left">{}</td></tr>', mark_safe(item[0]), mark_safe(item[1]))
    return mark_safe(msg)


@register.filter
def minus(value):
    # print(value.value)
    # value = int(value)
    return value


@register.filter
def in_list(value):
    return value in [2, 4, 6, 8, 10]
