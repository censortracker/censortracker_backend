from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class IndexTemplate(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/index.html"
