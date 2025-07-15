from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid


class Branding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="branding/logos/", blank=True, null=True)
    color = models.CharField(max_length=7, default="#7C3AED")  # HEX color
    font = models.CharField(max_length=50, default="Inter")

    def __str__(self):
        return f"{self.user.username}'s Branding"
    

class Survey(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    template_key = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    is_saved_template = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_id = uuid.uuid4().hex[:8]
            self.slug = slugify(self.title) + "-" + unique_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=50, default="text")         # ✅ Add this
    allow_multiple = models.BooleanField(default=False)            # ✅ Add this
    required = models.BooleanField(default=False)
    options = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.survey.title} - {self.answer}"

class SurveyTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.JSONField(default=list, blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField(default=5)
    questions = models.JSONField()  # List of predefined questions

    def __str__(self):
        return self.name
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"🔔 {self.message} ({self.user.username})"
