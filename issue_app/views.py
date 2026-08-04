"""
views.py
---------
This file has the "logic" for every page of our website.
Each function here is called a "view". A view takes a
request (what the user asked for) and gives back a response
(usually an HTML page).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .models import Issue
from .forms import IssueForm, CommentForm, SignUpForm
from .smart_helper import find_similar_issues


def home_page(request):
    """
    Home page - shows all reported issues.
    Also allows simple filtering by category and status using
    ?category=... and ?status=... in the URL.
    """
    all_issues = Issue.objects.all()

    selected_category = request.GET.get('category')
    selected_status = request.GET.get('status')

    if selected_category:
        all_issues = all_issues.filter(category=selected_category)

    if selected_status:
        all_issues = all_issues.filter(status=selected_status)

    context = {
        'all_issues': all_issues,
        'selected_category': selected_category,
        'selected_status': selected_status,
    }
    return render(request, 'issue_app/home.html', context)


@login_required
def report_issue_page(request):
    """
    Page where a logged-in user can report a new civic issue.
    Before saving, we use our simple AI helper to check if a
    similar issue was already reported, and show a warning.
    """
    similar_issues = []

    if request.method == 'POST':
        issue_form = IssueForm(request.POST, request.FILES)

        if issue_form.is_valid():
            # check for similar/duplicate issues first (simple AI step)
            typed_title = issue_form.cleaned_data['title']
            typed_description = issue_form.cleaned_data['description']

            existing_issues = list(Issue.objects.all())
            similar_issues = find_similar_issues(typed_title, typed_description, existing_issues)

            # if user already confirmed "yes, still submit", save it
            if request.POST.get('confirm_submit') == 'yes' or not similar_issues:
                new_issue = issue_form.save(commit=False)
                new_issue.reported_by = request.user
                new_issue.save()
                messages.success(request, "Your issue has been reported. Thank you!")
                return redirect('issue_detail_page', issue_id=new_issue.id)
            # else: fall through and show the similar issues warning below
    else:
        issue_form = IssueForm()

    context = {
        'issue_form': issue_form,
        'similar_issues': similar_issues,
    }
    return render(request, 'issue_app/report_issue.html', context)


def issue_detail_page(request, issue_id):
    """Page that shows full details of one issue, its comments,
    and lets the user upvote it or add a comment."""
    one_issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.issue = one_issue
            new_comment.commented_by = request.user
            new_comment.save()
            messages.success(request, "Comment added.")
            return redirect('issue_detail_page', issue_id=one_issue.id)
    else:
        comment_form = CommentForm()

    already_upvoted = False
    if request.user.is_authenticated:
        already_upvoted = one_issue.upvoted_by.filter(id=request.user.id).exists()

    context = {
        'one_issue': one_issue,
        'comment_form': comment_form,
        'already_upvoted': already_upvoted,
        'all_comments': one_issue.comments.all(),
    }
    return render(request, 'issue_app/issue_detail.html', context)


@login_required
def upvote_issue_page(request, issue_id):
    """Add or remove an upvote (like) from the current user on an issue."""
    one_issue = get_object_or_404(Issue, id=issue_id)

    if one_issue.upvoted_by.filter(id=request.user.id).exists():
        one_issue.upvoted_by.remove(request.user)   # already upvoted -> remove it
    else:
        one_issue.upvoted_by.add(request.user)       # not upvoted yet -> add it

    return redirect('issue_detail_page', issue_id=one_issue.id)


@login_required
def my_issues_page(request):
    """Page that shows only the issues reported by the logged-in user."""
    my_issues = Issue.objects.filter(reported_by=request.user)
    return render(request, 'issue_app/my_issues.html', {'my_issues': my_issues})


@login_required
def update_status_page(request, issue_id):
    """
    Page for staff/admin users to change the status of an issue
    (pending -> in progress -> resolved).
    """
    if not request.user.is_staff:
        messages.error(request, "Only staff members can update the status.")
        return redirect('issue_detail_page', issue_id=issue_id)

    one_issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed_status_list = dict(Issue._meta.get_field('status').choices)
        if new_status in allowed_status_list:
            one_issue.status = new_status
            one_issue.save()
            messages.success(request, "Status updated.")

    return redirect('issue_detail_page', issue_id=issue_id)


def signup_page(request):
    """Page where a new user can create their account."""
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            login(request, new_user)
            messages.success(request, "Account created. Welcome!")
            return redirect('home_page')
    else:
        signup_form = SignUpForm()

    return render(request, 'issue_app/signup.html', {'signup_form': signup_form})
