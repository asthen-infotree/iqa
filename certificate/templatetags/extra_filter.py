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
    dictionary = dict(subString.split(":",1) for subString in items.split("<br>"))
    # for item in items.split("<br>"):
    #     print('item', type(item))
    #     print(dict(item[0],item[1]))
    # <tr>
    #                <td><b>Material</b></td><td>:</td><td style="text-align:left"><span class="">{{ product.material }}</span></td>
    #            </tr>

    for x, y in dictionary.items():
        msg += format_html(
            '<tr><td><b>{}</b></td><td>:</td><td style="text-align:left"><span class="">{}</span></td></tr>', x, y)
    return mark_safe(msg)


@register.filter
def linebreak_to_row_template3(value):
    msg = ''
    items = linebreaksbr(value)
    dictionary = dict(subString.split(":") for subString in items.split("<br>"))

    for x, y in dictionary.items():
        msg += format_html(
            '<tr><td style="max-width:30%;width:30%;display:inline-block;word-break:break-all;"><b>{}</b></td><td style="width:2%">:</td><td style="text-align:left"><span class="">{}</span></td></tr>', x, y)
    return mark_safe(msg)


@register.filter
def linebreak_to_web_row(value):
    msg = ''
    items = linebreaksbr(value)
    dictionary = dict(subString.split(":") for subString in items.split("<br>"))

    for x, y in dictionary.items():
        msg += format_html(
            '<tr><td class="green">{}</td><td style="text-align:left">{}</td></tr>', x, y)
    return mark_safe(msg)


@register.filter
def minus(value):
    # print(value.value)
    # value = int(value)
    return value


@register.filter
def in_list(value):
    return value in [2, 4, 6, 8, 10]
