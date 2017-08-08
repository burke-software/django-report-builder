from django.apps import AppConfig
from django.urls import reverse
from material.frontend.apps import ModuleMixin


class ReportConfig(ModuleMixin, AppConfig):
    name = 'report_builder'
    icon = '<i class="material-icons">settings_applications</i>'

    def index_url(self):
        return reverse('{}:report_builder'.format(self.label))
