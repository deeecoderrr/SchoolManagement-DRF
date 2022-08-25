from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from .views import (
    HomeView,
    MyLoginView,
    StudentListView,
    RegisterView,
    AccountActivationView,
    TeacherListView,
    StudentDetailView,
    StudentDeleteView,
    StudentCreateView,
    StudentEditView,
    TeacherDetailView,
    TeacherDeleteView,
    TeacherCreateView,
    TeacherEditView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path(
        "account-activation/<uidb64>/<token>",
        AccountActivationView.as_view(),
        name="account_activation",
    ),
    path("logout/", logout_then_login, name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="school/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="school/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="school/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="school/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path("student/", StudentListView.as_view(), name="student"),
    path("new-student/", StudentCreateView.as_view(), name="student-create"),
    path("student/<id>/", StudentDetailView.as_view(), name="student-detail"),
    path("student/<id>/delete/", StudentDeleteView.as_view(), name="student-delete"),
    path("student/<id>/edit/", StudentEditView.as_view(), name="student-edit"),
    path("teacher/", TeacherListView.as_view(), name="teacher"),
    path("new-teacher/", TeacherCreateView.as_view(), name="teacher-create"),
    path("teacher/<id>/", TeacherDetailView.as_view(), name="teacher-detail"),
    path("teacher/<id>/delete/", TeacherDeleteView.as_view(), name="teacher-delete"),
    path("teacher/<id>/edit/", TeacherEditView.as_view(), name="teacher-edit"),
]
