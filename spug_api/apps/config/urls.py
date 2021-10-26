# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from .views import *

urlpatterns = [
    path('', ConfigView.as_view()),
    path('parse/json/', parse_json),
    path('parse/text/', parse_text),
    path('diff/', post_diff),
    path('environment/', EnvironmentView.as_view()),
    path('project/', ProjectView.as_view()),
    path('cluster/', Cluster.as_view()),
    path('workzone/', Work_Zone.as_view()),
    path('cuser/', ConnctUserConfig.as_view()),
    path('zone/', ZoneConfig.as_view()),
    path('rest/', ResourceTConfig.as_view()),
    path('hostall/', HostallConfig.as_view()),
    path('devpostion/', DevicePoConfig.as_view()),
    path('servicebag/', ServicebagConfig.as_view()),
    path('portlist/', PortlistConfig.as_view()),
    path('service/', ServiceView.as_view()),
    path('history/', HistoryView.as_view()),
    path('rsnamespace/', RancherNsView.as_view()),
    path('rsconf/',RancherConfConfView.as_view()),
    path('rsconfagg/', RancherAggMap.as_view()),
    path('rsconfig/', RancherConfManagerView.as_view()),
]
