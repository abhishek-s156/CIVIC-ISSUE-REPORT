"""
urls.py (inside issue_app)
----------------------------
This file connects a URL (web address) to a view (page logic).
Example: when someone visits "/report/", Django will run the
report_issue_page function from views.py
"""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('report/', views.report_issue_page, name='report_issue_page'),
    path('issue/<int:issue_id>/', views.issue_detail_page, name='issue_detail_page'),
    path('issue/<int:issue_id>/upvote/', views.upvote_issue_page, name='upvote_issue_page'),
    path('issue/<int:issue_id>/update-status/', views.update_status_page, name='update_status_page'),
    path('my-issues/', views.my_issues_page, name='my_issues_page'),

    # simple login / logout / signup pages
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', auth_views.LoginView.as_view(template_name='issue_app/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_page'),
]
