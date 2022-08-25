from distutils.log import Log
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from .tokens import token_validator, token_decoder
from django.contrib import messages
from .forms import (
    UserRegisterForm,
    MyLoginAuthForm,
    NewStudentForm,
    EditStudentForm,
    NewTeacherForm,
    EditTeacherForm,
)
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .trigger_email import trigger_email
from .communicator import StudentCommunicator, TeacherCommunicator

import logging

logger = logging.getLogger("django")


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "school/home.html"


class MyLoginView(LoginView):
    authentication_form = MyLoginAuthForm
    template_name = "school/login.html"


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "school/register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            logger.error(f"Erros in user registration form: {form.errors}")
            return render(request, "school/register.html", {"form": form})
        else:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            hostname = get_current_site(request)
            email_id = form.cleaned_data.get("email")
            try:
                response = trigger_email(hostname, user, email_id)

                if response == 1:
                    messages.success(
                        request,
                        f"Your account has been created! Activation link is sent to your email address.",
                    )

                    return redirect("login")
                else:
                    messages.error(
                        request,
                        f"Problem while creating account, please try again in sometime.",
                    )
            except Exception as exe:
                logger.error(exe)
                messages.error(
                    request,
                    f"Problem while creating account, please try again in sometime.",
                )


class AccountActivationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = token_decoder(uidb64)
            user = User.objects.get(pk=uid)

        except Exception as exe:
            logger.exception(exe)
            user = None

        if token_validator(user, token):
            user.is_active = True
            user.save()
            return HttpResponse(
                "Thank you for your email confirmation. Now you can login your account."
            )
        else:
            return HttpResponse("Activation link is invalid!")


class StudentListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = StudentCommunicator().list_student()
        if isinstance(data, list):
            return render(request, "school/student_list.html", {"context": data})
        else:
            messages.error(
                request, "Something went wrong, please try again in sometime!"
            )
            return redirect("home")


class StudentDetailView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = StudentCommunicator().get_student(id)
        if status_code == 200:
            return render(request, "school/student_detail.html", {"context": data})
        elif status_code == 404:
            messages.error(request, "Student not found!")
        else:
            messages.error(request, data)
        return redirect("student")


class StudentDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = StudentCommunicator().delete_student(id)

        if status_code == 204:
            messages.success(request, data)
        else:
            messages.error(request, data)
        return redirect("student")


class StudentCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = NewStudentForm()
        return render(request, "school/student_new.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = NewStudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status_code, data = StudentCommunicator().create_student(data)
            if status_code == 201:
                messages.success(request, "Student record created sucessfully!")
                return redirect("student-detail", data.get("id"))
            elif status_code == 400:
                messages.error(request, data)
            else:
                messages.error(request, "Something went wrong, try again later!")
        else:
            logger.error(f"Error in student creation form: {form.errors}")
            messages.error(request, "Something went wrong, try again later!")
        return redirect("student")


class StudentEditView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = StudentCommunicator().get_student(id)
        if status_code == 200:
            edit_form = EditStudentForm(data)
            return render(request, "school/student_edit.html", {"edit_form": edit_form})
        elif status_code == 404:
            messages.error(request, "Student not found!")
        else:
            messages.error(request, data)
        return redirect("student")

    def post(self, request, id, *args, **kwargs):
        form = EditStudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["id"] = id
            status_code, data = StudentCommunicator().edit_student(id, data)
            if status_code == 200:
                messages.success(request, "Student record updated sucessfully!")
                return redirect("student-detail", data.get("id"))
            elif status_code == 400:
                messages.error(request, data)
                return redirect("student-edit", id)
            elif status_code == 404:
                messages.error(request, "Students detail not found!")
            else:
                messages.error(request, "Something went wrong, try again later!")
        else:
            logger.error(f"Error in student edit form: {form.errors}")
            messages.error(request, "Something went wrong, try again later!")
        return redirect("student")


class TeacherListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = TeacherCommunicator().list_teacher()
        if isinstance(data, list):
            return render(request, "school/teacher_list.html", {"context": data})
        else:
            messages.error(request, data)
            return redirect("home")


class TeacherDetailView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = TeacherCommunicator().get_teacher(id)
        if status_code == 200:
            return render(request, "school/teacher_detail.html", {"context": data})
        elif status_code == 404:
            messages.error(request, "Teacher not found!")
        else:
            messages.error(request, data)
        return redirect("teacher")


class TeacherDeleteView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = TeacherCommunicator().delete_teacher(id)

        if status_code == 204:
            messages.success(request, data)
        else:
            messages.error(request, data)
        return redirect("teacher")


class TeacherCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = NewTeacherForm()
        return render(request, "school/teacher_new.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = NewTeacherForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status_code, data = TeacherCommunicator().create_teacher(data)
            if status_code == 201:
                messages.success(request, "Teacher record created sucessfully!")
                return redirect("teacher-detail", data.get("id"))
            elif status_code == 400:
                messages.error(request, data)
            else:
                messages.error(request, "Something went wrong, try again later!")
        else:
            logger.error(f"Error in teacher creation form: {form.errors}")
            messages.error(request, "Something went wrong, try again later!")
        return redirect("teacher")


class TeacherEditView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        status_code, data = TeacherCommunicator().get_teacher(id)
        if status_code == 200:
            edit_form = EditTeacherForm(data)
            return render(request, "school/teacher_edit.html", {"edit_form": edit_form})
        elif status_code == 404:
            messages.error(request, "Teacher not found!")
        else:
            messages.error(request, data)
        return redirect("teacher")

    def post(self, request, id, *args, **kwargs):
        form = EditTeacherForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["id"] = id

            status_code, data = TeacherCommunicator().edit_teacher(id, data)
            if status_code == 200:
                messages.success(request, "Teacher record updated sucessfully!")
                return redirect("teacher-detail", data.get("id"))
            elif status_code == 400:
                messages.error(request, data)
                return redirect("teacher-edit", id)
            elif status_code == 404:
                messages.error(request, "Teachers detail not found!")
            else:
                messages.error(request, "Something went wrong, try again later!")
        else:
            logger.error(f"Error in teacher edit form: {form.errors}")
            messages.error(request, "Something went wrong, try again later!")
        return redirect("teacher")
