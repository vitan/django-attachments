from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template import loader
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from attachments.models import Attachment
from attachments.forms import AttachmentForm
from attachments.AjaxResponseMixin import AjaxResponseMixin

def add_url_for_obj(obj):
    return reverse('add_attachment', kwargs={
                        'app_label': obj._meta.app_label,
                        'module_name': obj._meta.module_name,
                        'pk': obj.pk
                    })

@require_POST
@login_required
def add_attachment(request, app_label, module_name, pk,
                   template_name='attachments/list_fragment.html', extra_context={}):

    response = AjaxResponseMixin()
    model = get_model(app_label, module_name)
    if model is None:
        response.update_errors({'fail': ugettext('Model is None.')})
        return response.ajax_response()
    obj = get_object_or_404(model, pk=pk)
    form = AttachmentForm(request.POST, request.FILES)

    if form.is_valid():
        attachment_obj = form.save(request, obj)
        template = loader.get_template(template_name)
        request_context = RequestContext(request, {'attachment': attachment_obj })
        data = template.render(request_context)
        context = { 'success': data }
        return response.ajax_response(**context)

    else:
        response.update_errors({'fail': ugettext('attachment failed.')})
        return response.ajax_response()

@login_required
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)

    response = AjaxResponseMixin()
    if request.user.has_perm('delete_foreign_attachments') \
       or request.user == g.creator:
        g.delete()
        context = {'success': ugettext('Your attachment was deleted.')}
        return response.ajax_response(**context)
    else:
        response.update_errors({
            'fail': ugettext('Your have no the permission.')
        })
        return response.ajax_response()
