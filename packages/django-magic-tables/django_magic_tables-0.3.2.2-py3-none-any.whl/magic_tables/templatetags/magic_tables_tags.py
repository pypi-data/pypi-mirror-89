from django import template
from django.forms import model_to_dict
from django.template import Context, VariableDoesNotExist

register = template.Library()


class TableNode(template.Node):
    """
    Create Node object with table filled with object list.
    """

    def __init__(self, object_list, css_classes):
        self.object_list = template.Variable(object_list)
        self.css_classes = css_classes

    def render(self, context):
        try:
            object_list = self.object_list.resolve(context)
        except VariableDoesNotExist:
            return ''

        # check if QuerySet contains dicts or Model objects
        if not isinstance(object_list[0], dict):
            # turn Model object into dict
            dict_object_list = [model_to_dict(obj) for obj in object_list]
        else:
            dict_object_list = object_list

        # turn field name into associated verbose name
        fields = [object_list.model._meta.get_field(key).verbose_name for key in dict_object_list[0].keys()]

        table = context.template.engine.get_template("magic_tables/table.html")
        return table.render(Context({'dict_object_list': dict_object_list,
                                     'fields': fields,
                                     'css_classes': self.css_classes}, autoescape=context.autoescape))


@register.tag(name="table")
def do_table(parser, token):
    """
    You need to pass in at least the object_list and can also pass in the optional 'css_classes' object.
    These classes will be added to the table HTML tag.
    """

    token = token.split_contents()
    tag_name = token.pop(0)

    try:
        object_list = token.pop(0)
    except IndexError:
        raise template.TemplateSyntaxError(
            "%r tag requires at least one argument" % tag_name
        )

    css_classes = None
    try:
        css_classes = token.pop(0)
    except IndexError:
        pass

    if css_classes is not None:
        if not (css_classes[0] == css_classes[-1] and css_classes[0] in ('"', "'")):
            raise template.TemplateSyntaxError(
                "%r tag's argument should be in quotes" % tag_name
            )
        else:
            css_classes = css_classes[1:-1]

    return TableNode(object_list, css_classes)
