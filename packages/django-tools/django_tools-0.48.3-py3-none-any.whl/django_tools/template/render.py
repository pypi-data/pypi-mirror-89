"""
    template render
    ~~~~~~~~~~~~~~

    Some tools around template rendering

    :copyleft: 2009-2017 by the django-tools team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from django.template import Context, Template
from django.template.loader import get_template


def render_template_file(path, context):
    """
    Render given template file and return the rendered string
    """
    t = get_template(path)
    return t.render(context)


def render_string_template(template, context):
    """
    render the given template string with the context and return it as a string
    """
    t = Template(template)
    c = Context(context)
    return t.render(c)
