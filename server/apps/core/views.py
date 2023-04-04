from django.views import generic


class IndexTemplate(generic.TemplateView):
    template_name = "core/index.html"
