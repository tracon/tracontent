from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe
from django.shortcuts import get_object_or_404

from .models import StyleSheet


@require_safe
def resources_style_sheet_view(request, style_sheet_name):
    style_sheet = get_object_or_404(StyleSheet, name=style_sheet_name, active=True)
    return HttpResponse(style_sheet.content, content_type='text/css')