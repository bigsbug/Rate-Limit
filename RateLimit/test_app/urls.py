from django.urls import path
from test_app.views import index

urlpatterns = [
    path("", index),
]
