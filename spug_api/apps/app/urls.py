# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from .views import *

urlpatterns = [
    path('', AppView.as_view()),
    path('deploy/', DeployView.as_view()),
    path('deploy/svc/<str:tag>/', RancherSvcView.as_view()),
    path('deploy/svc/notice', RancherSvcNoticeView.as_view()),
    # path('deployns/', DeployRancherNsView.as_view()),
    # path('deployconf/', DeployRancherConfView.as_view()),
    path('deploy/<int:d_id>/versions/', get_versions),
]
