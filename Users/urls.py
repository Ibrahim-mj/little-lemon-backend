from django.urls import path

from . import views

urlpatterns = [
    path(
        "register/",
        views.UserViewSet.as_view(
            actions={
                # 'get': 'list',
                "post": "create",
                # 'put': 'update',
                # 'delete': 'destroy'
            }
        ),
        name="register",
    ),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
]
