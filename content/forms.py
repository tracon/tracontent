import re

from django import forms
from django.core.validators import RegexValidator

from .models import BlogComment


kissa_validator = RegexValidator(
    regex=r"^kissa$",
    flags=re.IGNORECASE,
    message="Vihje: kissa",
)


class BlogCommentForm(forms.ModelForm):
    kissa = forms.CharField(
        label="Mikä eläin sanoo miau?",
        help_text="Tällä tarkistamme, että et ole robotti.",
        validators=[
            kissa_validator,
        ],
    )

    class Meta:
        model = BlogComment
        fields = ("author_name", "author_email", "comment", "kissa")
