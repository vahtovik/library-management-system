from django import template

register = template.Library()


@register.filter
def add_class(field, css_classes):
    classes = css_classes.split()
    return field.as_widget(attrs={"class": " ".join(classes)})
