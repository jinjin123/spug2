# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.urls import path

from .views import *

urlpatterns = [
    path('', FileView.as_view()),
    path('object/', ObjectView.as_view()),
    path('excel/<str:type>', Exceldown.as_view()),
    path('dbmexcel/<str:type>', DbmExceldown.as_view()),

]
