from django.urls import path
from . import views




urlpatterns = [
    path("signup/",views.SignUp.as_view()),
    path("login/",views.LoginView.as_view()),
    path("students/register/",views.Student_Details.as_view()),
    path("students/unverified/",views.Unverified_Students.as_view()),
    path("verify/student/<int:pk>/",views.Unverified_Students.as_view()),
    path("students/update/<int:pk>/",views.Student_Details.as_view()),
    
    
]
