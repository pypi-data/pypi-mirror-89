import json

from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SortableTablePlugin


@plugin_pool.register_plugin
class SortableTableCMSPlugin(CMSPluginBase):
    """
    Plugin for including a selection of entries
    """
    module = _('Table')
    name = _('Sortable Table')
    model = SortableTablePlugin
    render_template = 'sortabletable/render_table.html'
    text_enabled = True

    raw_id_fields = ('creator',)

    def render(self, context, instance, placeholder):
        """
        Update the context with plugin's data
        """
        context = super().render(
            context, instance, placeholder)
        context['table_id'] = instance.pk
        context['object'] = instance
        context['settings'] = json.dumps(instance.settings)
        context.update(instance.get_table_context())
        return context
