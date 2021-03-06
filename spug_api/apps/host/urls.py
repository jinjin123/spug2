# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from .views import *

urlpatterns = [
    path('resource/<str:tag>/', HostView.as_view()),
    path('dbresource/<str:tag>/', MultiDbView.as_view()),
    path('import/', post_import),
    path('dbmimport/', multidb_import),
    path('parse/', post_parse),
    path('updatepwd/', ModifyPwd.as_view()),
    path('netcheck/',NetCheck.as_view()),
]
