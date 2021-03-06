import sys
import logging

sys.path.append("../api")

from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from api.permissions import SuperUserMixin
from api.models import Project
from app import settings

logger = logging.getLogger(__name__)


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = "annotation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        context["bundle_name"] = project.get_bundle_name()
        return context


class ProjectsView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "projects.html"


class DatasetView(SuperUserMixin, LoginRequiredMixin, ListView):
    template_name = "dataset.html"
    paginate_by = 5
    extra_context = {"bundle_name": "dataset"}

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        return project.documents.all()


class LabelView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin.html"
    extra_context = {"bundle_name": "label"}


class StatsView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin.html"
    extra_context = {"bundle_name": "stats"}


class GuidelineView(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin.html"
    extra_context = {"bundle_name": "guideline"}


class DataUpload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        context["bundle_name"] = project.get_bundle_name_upload()
        return context


class DataDownload(SuperUserMixin, LoginRequiredMixin, TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        context["bundle_name"] = project.get_bundle_name_download()
        return context


class LoginView(BaseLoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    extra_context = {
        "github_login": bool(settings.SOCIAL_AUTH_GITHUB_KEY),
        "allow_signup": bool(settings.ALLOW_SIGNUP),
    }

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context
