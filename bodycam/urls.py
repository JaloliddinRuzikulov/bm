from django.urls import path
from .views import AddView, LaventView, LaventPrintView, LaventCloseView, ReturnView, DataView, ManageView

urlpatterns = [
    path('add/', AddView.as_view(), name='add_bodycam'),
    path('manage/', ManageView.as_view(), name='manage_bodycam'),
    path('lavent/', LaventView.as_view(), name='lavent_bodycam'),
    path('lavent/<int:pk>/print/', LaventPrintView.as_view(), name='lavent_print_bodycam'),
    path('lavent/<int:pk>/close/', LaventCloseView.as_view(), name='lavent_close_bodycam'),
    path('return/', ReturnView.as_view(), name='return_bodycam'),
    path('data/', DataView.as_view(), name='data_bodycam'),
]
