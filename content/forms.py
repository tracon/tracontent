# encoding: utf-8

import re

from django import forms
from django.core.validators import RegexValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Hidden

from .models import BlogComment
from .utils import horizontal_form_helper, indented_without_label


kissa_validator = RegexValidator(
    regex=r'^kissa$',
    flags=re.IGNORECASE,
    message=u'Vihje: kissa',
)


class BlogCommentForm(forms.ModelForm):
    kissa = forms.CharField(
        label='Mikä eläin sanoo miau?',
        help_text=u'Tällä tarkistamme, että et ole robotti.',
        validators=[kissa_validator,],
    )

    def __init__(self, *args, **kwargs):
        super(BlogCommentForm, self).__init__(*args, **kwargs)

        # self.helper = horizontal_form_helper()
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            'author_name',
            'author_email',
            'comment',
            'kissa',
            Submit('submit', u'Lähetä', css_class='btn-success')
        )

    class Meta:
        model = BlogComment
        fields = ('author_name', 'author_email', 'comment', 'kissa')
