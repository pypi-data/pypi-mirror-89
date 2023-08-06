from crispy_forms.utils import render_crispy_form
from django_jinja import library
from jinja2 import contextfunction
from webpack_loader.templatetags.webpack_loader import render_bundle

library.global_function(render_bundle)


@contextfunction
@library.global_function
def crispy(context, form, helper=None):
    return render_crispy_form(form, helper=helper, context=context)
