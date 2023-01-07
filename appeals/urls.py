from django.urls import path
from .views import AppealsDone, AppealsArchive, AppealsNotDone, AppealsDetail, AppealsChangeDone, AppealsMy, AppealsNew, \
    AppealsIgnore

urlpatterns = [
    path('<int:pk>/', AppealsDetail.as_view(), name='appeals_detail'),
    path('<int:pk>/done/', AppealsChangeDone.as_view(), name='appeals_change_done'),
    path('new/', AppealsNew.as_view(), name='appeals_new'),
    path('my/', AppealsMy.as_view(), name='appeals_list'),
    path('done/', AppealsDone.as_view(), name='appeals_done'),
    path('notdone/', AppealsNotDone.as_view(), name='appeals_notdone'),
    path('ignore/', AppealsIgnore.as_view(), name='appeals_ignore'),
    path('archive/', AppealsArchive.as_view(), name='appeals_archive'),
]
