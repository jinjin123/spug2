# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from .views import *

urlpatterns = [
    path('request/', RequestView.as_view()),
    path('request/change/<int:id>', RequestChangeDetailView.as_view()),
    path('request/rancher/', RequestRancherDeployView.as_view()),
    path('request/upload/', do_upload),
    path('request/<int:envid>/<int:r_id>/', RequestDetailView.as_view()),
    path('request/rancher/publish', RancherPublishView.as_view()),
    path('request/master', RequestMaster.as_view()),
    path('request/oplogs', RequestOplog.as_view()),

]
