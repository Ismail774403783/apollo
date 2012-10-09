from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, UpdateView
from .forms import ContactForm, generate_submission_form
from .models import *

COMPLETION_STATUS = (
    (0, 'Complete'),
    (1, 'Partial'),
    (2, 'Empty'),
)


class TemplatePreview(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs['template_name']
        return super(TemplateView, self).dispatch(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)


class SubmissionListView(ListView):
    context_object_name = 'submissions'
    template_name = 'core/submission_list.html'
    paginate_by = settings.PAGE_SIZE
    page_title = ''

    def get_queryset(self):
        self.page_title = self.form.name
        return Submission.objects.filter(form=self.form).exclude(observer=None)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['page_title'] = self.page_title
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.form = get_object_or_404(Form, pk=kwargs['form'])
        return super(SubmissionListView, self).dispatch(*args, **kwargs)


class SubmissionEditView(UpdateView):
    template_name = 'core/submission_edit.html'

    def get_object(self, queryset=None):
        return self.submission.master()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.submission = get_object_or_404(Submission, pk=kwargs['pk'])
        self.form_class = generate_submission_form(self.submission.form)
        return super(SubmissionEditView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionEditView, self).get_context_data(**kwargs)
        context['submission'] = self.submission
        return context

    def get_success_url(self):
        return reverse('submissions_list', args=[self.submission.form.pk])


class ContactListView(ListView):
    context_object_name = 'contacts'
    template_name = 'core/contact_list.html'
    model = Observer
    paginate_by = settings.PAGE_SIZE

    def get_context_data(self, **kwargs):
        return super(ContactListView, self).get_context_data(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactListView, self).dispatch(*args, **kwargs)


class ContactEditView(FormView):
    template_name = 'core/contact_edit.html'
    form_class = ContactForm
    success_url = '/contacts/'

    def form_valid(self, form):
        pass
    pass
