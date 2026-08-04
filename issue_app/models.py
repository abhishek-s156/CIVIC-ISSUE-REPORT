"""
models.py
----------
This file has the "tables" of our project.
In Django, each class here becomes a table in the database.

We have 2 simple tables:
1. Issue    -> one civic problem reported by a citizen (like pothole, garbage, etc.)
2. Comment  -> a small message left by someone on an issue
"""

from django.db import models
from django.contrib.auth.models import User


# a fixed list of problem types citizen can pick while reporting
CATEGORY_CHOICES = [
    ('pothole', 'Pothole / Road Damage'),
    ('garbage', 'Garbage / Waste'),
    ('streetlight', 'Street Light Not Working'),
    ('water', 'Water Supply Problem'),
    ('drainage', 'Drainage / Sewage'),
    ('other', 'Other Problem'),
]

# a fixed list of status an issue can have
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]


class Issue(models.Model):
    """
    This table stores every civic issue reported by any user.
    Example: "Big pothole near XYZ school"
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=255, help_text="Area / Street / Landmark")
    photo = models.ImageField(upload_to='issue_photos/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_issues')
    created_at = models.DateTimeField(auto_now_add=True)

    # people who liked / supported this issue (to show it is important)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_issues', blank=True)

    def total_upvotes(self):
        """Return how many people have upvoted this issue."""
        return self.upvoted_by.count()

    def total_comments(self):
        """Return how many comments this issue has."""
        return self.comments.count()

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']   # newest issue shows first


class Comment(models.Model):
    """
    This table stores small text comments/updates that people
    write under an issue. Example: "This is fixed now, thank you!"
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commented_by.username} on {self.issue.title}"

    class Meta:
        ordering = ['created_at']
