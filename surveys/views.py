from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .models import Survey, Question, Response
from .forms import SignupForm, SurveyForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Survey, Response  # Plus Idea if available
from datetime import datetime, timezone


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required(login_url='login')
def settings_view(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get("name")
        email = request.POST.get("email")
        tagline = request.POST.get("tagline")
        brand_color = request.POST.get("brand_color")
        default_status = request.POST.get("default_status")
        email_alerts = request.POST.get("email_alerts")

        # Update basic user info (name and email)
        user.email = email
        user.first_name = name  # You might split first/last later
        user.save()

        # You can optionally store these preferences in a Settings model
        messages.success(request, "Your settings have been updated 💾")
        return redirect("settings_page")

    return render(request, "surveys/settings.html")

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        username = request.user.username
        request.user.delete()
        messages.success(request, f"Your Askly account '{username}' has been deleted 💔")
        return redirect("home")
    Notification.objects.create(
    user=request.user,
    message=f"🗑️ Survey '{survey.title}' was deleted."
    )


    # GET request shows confirmation page
    return render(request, "surveys/delete_account_confirm.html")

from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import redirect

@csrf_protect
def submit_feedback(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save, email, or log — here we just print
        print(f"📬 Feedback from {name} ({email}): {message}")

        messages.success(request, "Thank you for your feedback 💜")
        return redirect("home")

    return redirect("home")


@login_required(login_url='/login')  # Redirect guests before loading the page
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, "surveys/survey_list.html", {"surveys": surveys})
class CustomLoginView(LoginView):
    template_name = "surveys/login.html"


# 🔹 User Authentication Views
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "surveys/signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")



# 🔹 Survey Management Views
from django.contrib import messages
@login_required(login_url='login')
def create_survey(request):
    ...

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Survey, Question

@login_required
def create_survey(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if not title:
            messages.error(request, "Survey title is required.")
            return redirect("create_survey")

        survey = Survey.objects.create(
            title=title,
            description=description,
            owner=request.user
        )

        texts = request.POST.getlist("question_texts")
        types = request.POST.getlist("question_types")
        required_flags = request.POST.getlist("required_flags")
        allow_multiple_flags = request.POST.getlist("allow_multiple")

        for i in range(len(texts)):
            text = texts[i].strip()
            qtype = types[i] if i < len(types) else "text"
            required = str(i) in required_flags
            allow_multi = str(i) in allow_multiple_flags

            if text:
                Question.objects.create(
                    survey=survey,
                    text=text,
                    type=qtype,
                    required=required,
                    allow_multiple=allow_multi
                )

        

        messages.success(request, f"Survey '{survey.title}' created successfully!")
        Notification.objects.create(
        user=request.user,
        message=f"✅ Survey '{survey.title}' created successfully!"
        )
        return redirect("survey_review", survey_id=survey.id)

    return render(request, "surveys/create_survey.html")


def survey_review(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return render(request, "surveys/survey_review.html", {"survey": survey})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Survey

@login_required(login_url='login')
def survey_list(request):
    user = request.user
    status_filter = request.GET.get("status", "all")

    # Base queryset: surveys created by this user
    surveys = Survey.objects.filter(owner=user)

    # If filtering by status
    if status_filter != "all":
        surveys = surveys.filter(status=status_filter)

    context = {
        "surveys": surveys,
        "status_filter": status_filter,
    }

    return render(request, "surveys/survey_list.html", context)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
@login_required(login_url='login')
def update_survey_status(request, survey_id):
    if request.method == "POST":
        try:
            survey = Survey.objects.get(id=survey_id, owner=request.user)
            data = json.loads(request.body)
            new_status = data.get("status")

            if new_status in ["active", "draft", "archived"]:
                survey.status = new_status
                survey.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Invalid status."})
        except Survey.DoesNotExist:
            return JsonResponse({"success": False, "error": "Survey not found."})
    return JsonResponse({"success": False, "error": "Invalid request method."})

def take_survey(request, survey_slug):
    print(f"DEBUG: Received slug -> {survey_slug}")  # 🔍 Debugging log
    survey = get_object_or_404(Survey, slug=survey_slug)

    if request.method == "POST":
        answers = request.POST.getlist("answers")
        questions = survey.questions.all()

        for i, question in enumerate(questions):
            Response.objects.create(
                survey=survey,
                question=question,
                answer=answers[i]
            )

        return redirect("survey_list")

    return render(request, "surveys/survey.html", {"survey": survey})


# 🔹 Survey Responses View
def survey_responses(request, survey_slug):
    survey = get_object_or_404(Survey, slug=survey_slug)
    responses = Response.objects.filter(survey=survey)
    Notification.objects.create(
    user=survey.owner,
    message=f"📝 New response submitted for '{survey.title}'"
    )

    return render(request, "surveys/survey_responses.html", {"survey": survey, "responses": responses})


# 🔹 Main Pages
from .models import Notification

from .models import Notification

def home(request):
    notifications = []
    unread_count = 0

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:5]
        unread_count = Notification.objects.filter(user=request.user, read=False).count()

    return render(request, "surveys/home.html", {
        "notifications": notifications,
        "unread_count": unread_count,
    })

def thank_you(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return render(request, "surveys/thank_you.html", {"survey": survey})


from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def notifications_page(request):
    Notification.objects.filter(user=request.user, read=False).update(read=True)
    user_notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "surveys/notifications_page.html", {"notifications": user_notifications})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Survey, Response

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Survey, Response

@login_required(login_url='login')
def view_all_responses(request):
    surveys = Survey.objects.filter(owner=request.user)
    all_responses = Response.objects.filter(survey__in=surveys).select_related("question", "survey")

    return render(request, "surveys/all_responses.html", {
        "responses": all_responses
    })

from django.http import HttpResponse
import csv
from .models import Survey, Response

@login_required(login_url='login')
def download_responses_csv_single(request, survey_id):
    survey = Survey.objects.get(id=survey_id, owner=request.user)
    responses = Response.objects.filter(survey=survey).select_related("question")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{survey.title}-responses.csv"'

    writer = csv.writer(response)
    writer.writerow(["Question", "Answer", "Submitted At"])

    for r in responses:
        writer.writerow([r.question.text, r.answer, r.submitted_at.strftime("%d-%b-%Y %H:%M")])

    return response
import openpyxl
from openpyxl.styles import Font
from io import BytesIO

@login_required(login_url='login')
def download_responses_excel(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, owner=request.user)
    responses = Response.objects.filter(survey=survey).select_related("question")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"{survey.title} Responses"

    sheet.append(["Question", "Answer", "Submitted At"])
    for cell in sheet[1]: cell.font = Font(bold=True)

    for r in responses:
        sheet.append([r.question.text, r.answer, r.submitted_at.strftime("%d-%b-%Y %H:%M")])

    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)

    response = HttpResponse(stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{survey.slug}-responses.xlsx"'
    return response
import openpyxl
from openpyxl.styles import Font
from io import BytesIO

@login_required(login_url='login')
def download_responses_excel(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, owner=request.user)
    responses = Response.objects.filter(survey=survey).select_related("question")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"{survey.title} Responses"

    sheet.append(["Question", "Answer", "Submitted At"])
    for cell in sheet[1]: cell.font = Font(bold=True)

    for r in responses:
        sheet.append([r.question.text, r.answer, r.submitted_at.strftime("%d-%b-%Y %H:%M")])

    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)

    response = HttpResponse(stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{survey.slug}-responses.xlsx"'
    return response

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

@login_required(login_url='login')
def download_responses_pdf(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, owner=request.user)
    responses = Response.objects.filter(survey=survey).select_related("question")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph(f"Survey: {survey.title}", styles["Title"]), Spacer(1, 12)]

    for r in responses:
        elements.append(Paragraph(f"<b>{r.question.text}</b>: {r.answer}", styles["BodyText"]))
        elements.append(Paragraph(f"<i>Submitted at:</i> {r.submitted_at.strftime('%d-%b-%Y %H:%M')}", styles["BodyText"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{survey.slug}-responses.pdf"'
    return response
    

import csv
from django.http import HttpResponse

@login_required(login_url='login')
def download_responses_csv(request):
    surveys = Survey.objects.filter(owner=request.user)
    responses = Response.objects.filter(survey__in=surveys).select_related("survey", "question")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="responses.csv"'

    writer = csv.writer(response)
    writer.writerow(["Survey Title", "Question", "Answer", "Submitted At"])

    for r in responses:
        writer.writerow([r.survey.title, r.question.text, r.answer, r.submitted_at])

    return response



@login_required(login_url='login')
def dashboard(request):
    user = request.user

    # Fetch surveys created by this user, annotate with response count
    surveys = Survey.objects.filter(owner=user).annotate(response_count=Count("response"))

    # Total responses across all surveys
    total_responses = sum(survey.response_count for survey in surveys)

    # Count distinct templates used (if template_key exists)
    templates_used = surveys.exclude(template_key=None).values_list("template_key", flat=True).distinct().count()

    # Optional: Count ideas submitted
    try:
        from .models import Idea
        idea_count = Idea.objects.filter(owner=user).count()
    except ImportError:
        idea_count = 0

    # Recent activities (creation or update)
    activities = [
        f"You created or updated '{survey.title}' on {survey.created_at.strftime('%d %b %Y')}"
        for survey in surveys.order_by("-created_at")[:5]
    ]

    # Add readable timestamps to each survey
    now = datetime.now(timezone.utc)
    for survey in surveys:
        if survey.updated_at:
            delta = now - survey.updated_at
            seconds = delta.total_seconds()

            if seconds < 60:
                survey.human_updated = "Just now"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                survey.human_updated = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                survey.human_updated = f"{hours} hour{'s' if hours != 1 else ''} ago"
            else:
                survey.human_updated = survey.updated_at.strftime("%d %b %Y")
        else:
            survey.human_updated = "—"

    # Group most recent responses per survey (limit 10 per survey)
    responses_by_survey = {
        survey.id: Response.objects.filter(survey=survey).order_by("-submitted_at")[:10]
        for survey in surveys
    }

    # Pass everything to your template
    context = {
        "user": user,
        "surveys": surveys,
        "total_responses": total_responses,
        "templates_used": templates_used,
        "idea_count": idea_count,
        "activities": activities,
        "responses_by_survey": responses_by_survey,
    }

    return render(request, "surveys/dashboard.html", context)


@login_required(login_url='login')
def use_template(request, template_key):
    template_map = {
        "customer_feedback": {
            "title": "Customer Feedback",
            "description": "Collect product, service, or experience feedback.",
            "questions": [
                "How satisfied are you with our service?",
                "What did you like the most?",
                "What can we improve?",
                "Would you recommend us?"
            ]
        },
        "employee_satisfaction": {
            "title": "Employee Satisfaction",
            "description": "Gauge team morale and satisfaction.",
            "questions": [
                "How supported do you feel at work?",
                "Do you feel valued?",
                "Any suggestions for improvement?"
            ]
        },
        "student_survey": {
            "title": "Student Survey",
            "description": "Understand student opinions on classes and environment.",
            "questions": [
                "How engaging are your classes?",
                "Do you feel supported academically?",
                "Any suggestions for improvement?"
            ]
        },
        "health_check": {
            "title": "Health Check",
            "description": "Quick health check survey for staff or visitors.",
            "questions": [
                "Have you experienced any symptoms today?",
                "Have you been in contact with anyone unwell?",
                "Would you like a follow-up check?"
            ]
        },
        "partner_feedback": {
            "title": "Partner Feedback",
            "description": "Evaluate partnership and collaboration experiences.",
            "questions": [
                "How satisfied are you with this partnership?",
                "What worked well?",
                "What would you change?"
            ]
        },
        "idea_submission": {
            "title": "Idea Submission",
            "description": "Gather innovative ideas from your team or community.",
            "questions": [
                "What's your idea?",
                "What problem does it solve?",
                "How can it be implemented?"
            ]
        },
    }

    template = template_map.get(template_key)
    if not template:
        return redirect("survey_templates")

    # Create survey instance
    survey = Survey.objects.create(title=template["title"], owner=request.user)

    # Add questions
    for q_text in template["questions"]:
        Question.objects.create(survey=survey, text=q_text)

    Notification.objects.create(
    user=request.user,
    message=f"📄 Template '{template_key}' was used to create a new survey!"
    )

    # Redirect to review
    return redirect("survey_review", survey_id=survey.id)


def preview_template(request, template_key):
    # same dictionary as above
    ...
    return render(request, "surveys/template_preview.html", {"template": template})




def survey_templates(request):
    templates = [
        {
            "name": "Customer Feedback",
            "description": "Collect product, service, or experience feedback.",
            "icon": "fas fa-smile",
            "key": "customer_feedback",
            "tags": ["Customer", "Service", "Experience"],
            "rating": 5,
            "questions": [
                "How satisfied are you with our service?",
                "What did you like the most?",
                "What can we improve?",
                "Would you recommend us?"
            ]
        },
        {
            "name": "Employee Satisfaction",
            "description": "Gauge your team's morale and satisfaction at work.",
            "icon": "fas fa-users",
            "key": "employee_satisfaction",
            "tags": ["HR", "Workplace", "Team"],
            "rating": 4,
            "questions": [
                "How supported do you feel at work?",
                "Do you feel valued?",
                "Any suggestions for improvement?"
            ]
        },
        {
            "name": "Student Survey",
            "description": "Understand student opinions on classes and environment.",
            "icon": "fas fa-graduation-cap",
            "key": "student_survey",
            "tags": ["School", "Education", "Students"],
            "rating": 4,
            "questions": [
                "How engaging are your classes?",
                "Do you feel supported academically?",
                "Any suggestions for improvement?"
            ]
        },
        {
            "name": "Health Check",
            "description": "Quick health check survey for staff or visitors.",
            "icon": "fas fa-heartbeat",
            "key": "health_check",
            "tags": ["Health", "Symptoms", "Safety"],
            "rating": 4,
            "questions": [
                "Have you experienced any symptoms today?",
                "Have you been in contact with anyone unwell?",
                "Would you like a follow-up check?"
            ]
        },
        {
            "name": "Partner Feedback",
            "description": "Evaluate partnerships and business collaboration experiences.",
            "icon": "fas fa-handshake",
            "key": "partner_feedback",
            "tags": ["Partnership", "Business", "Review"],
            "rating": 3,
            "questions": [
                "How satisfied are you with this partnership?",
                "What worked well?",
                "What would you change?"
            ]
        },
        {
            "name": "Idea Submission",
            "description": "Gather innovative ideas from your team or community.",
            "icon": "fas fa-lightbulb",
            "key": "idea_submission",
            "tags": ["Innovation", "Ideas", "Feedback"],
            "rating": 5,
            "questions": [
                "What's your idea?",
                "What problem does it solve?",
                "How can it be implemented?"
            ]
        },
        {
            "name": "Event Feedback",
            "description": "Collect participant impressions and suggestions from events.",
            "icon": "fas fa-calendar-check",
            "key": "event_feedback",
            "tags": ["Events", "Participants", "Suggestions"],
            "rating": 4,
            "questions": [
                "How would you rate the event overall?",
                "What did you enjoy most?",
                "Any suggestions for future events?"
            ]
        },
        {
            "name": "Onboarding Experience",
            "description": "Evaluate the ease and effectiveness of your onboarding process.",
            "icon": "fas fa-rocket",
            "key": "onboarding_experience",
            "tags": ["HR", "New Hires", "Process"],
            "rating": 3,
            "questions": [
                "How clear were the onboarding steps?",
                "Did you feel supported?",
                "How can the experience be improved?"
            ]
        }
    ]

    return render(request, "surveys/survey_templates.html", {"templates": templates})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Survey, Question
@login_required
def edit_template_survey(request, template_key):
    # --- 1. Built‑in template “database” -------------------------------
    template_map = {
        "customer_feedback": {
            "title": "Customer Feedback",
            "description": "Collect product, service, or experience feedback.",
            "questions": [
                {"text": "How satisfied are you with our service?", "type": "text", "allow_multiple": False},
                {"text": "What did you like the most?", "type": "text", "allow_multiple": False},
                {"text": "What can we improve?", "type": "text", "allow_multiple": False},
                {"text": "Would you recommend us?", "type": "multiple_choice", "allow_multiple": False,
                 "options": ["Yes", "No", "Maybe"]},
            ],
        },
        "employee_satisfaction": {
            "title": "Employee Satisfaction",
            "description": "Gauge team morale and satisfaction.",
            "questions": [
                {"text": "How supported do you feel at work?", "type": "rating", "allow_multiple": False},
                {"text": "Do you feel valued?", "type": "multiple_choice", "allow_multiple": False,
                 "options": ["Yes", "No", "Sometimes"]},
                {"text": "Any suggestions for improvement?", "type": "text", "allow_multiple": False},
            ],
        },
        "student_survey": {
            "title": "Student Survey",
            "description": "Understand student opinions on classes and environment.",
            "questions": [
                {"text": "How engaging are your classes?", "type": "rating", "allow_multiple": False},
                {"text": "Do you feel supported academically?", "type": "multiple_choice", "allow_multiple": False,
                 "options": ["Always", "Sometimes", "Rarely"]},
                {"text": "Any suggestions for improvement?", "type": "text", "allow_multiple": False},
            ],
        },
        "health_check": {
            "title": "Health Check",
            "description": "Quick health check survey for staff or visitors.",
            "questions": [
                {"text": "Have you experienced any symptoms today?", "type": "checkbox", "allow_multiple": True,
                 "options": ["Cough", "Fever", "Fatigue"]},
                {"text": "Have you been in contact with anyone unwell?", "type": "multiple_choice",
                 "allow_multiple": False, "options": ["Yes", "No"]},
                {"text": "Would you like a follow‑up check?", "type": "multiple_choice", "allow_multiple": False,
                 "options": ["Yes", "No"]},
            ],
        },
        "partner_feedback": {
            "title": "Partner Feedback",
            "description": "Evaluate partnership and collaboration experiences.",
            "questions": [
                {"text": "How satisfied are you with this partnership?", "type": "rating", "allow_multiple": False},
                {"text": "What worked well?", "type": "text", "allow_multiple": False},
                {"text": "What would you change?", "type": "text", "allow_multiple": False},
            ],
        },
        "idea_submission": {
            "title": "Idea Submission",
            "description": "Gather innovative ideas from your team or community.",
            "questions": [
                {"text": "What's your idea?", "type": "text", "allow_multiple": False},
                {"text": "What problem does it solve?", "type": "text", "allow_multiple": False},
                {"text": "How can it be implemented?", "type": "text", "allow_multiple": False},
            ],
        },
        "event_feedback": {
            "title": "Event Feedback",
            "description": "Collect impressions and suggestions from event participants.",
            "questions": [
                {"text": "How would you rate the event overall?", "type": "rating", "allow_multiple": False},
                {"text": "What did you enjoy most?", "type": "text", "allow_multiple": False},
                {"text": "Any suggestions for future events?", "type": "text", "allow_multiple": False},
            ],
        },
        "onboarding_experience": {
            "title": "Onboarding Experience",
            "description": "Evaluate how smooth and effective onboarding was.",
            "questions": [
                {"text": "How clear were the onboarding steps?", "type": "rating", "allow_multiple": False},
                {"text": "Did you feel supported during onboarding?", "type": "multiple_choice",
                 "allow_multiple": False, "options": ["Yes", "No", "Somewhat"]},
                {"text": "Suggestions to improve onboarding?", "type": "text", "allow_multiple": False},
            ],
        },
    }

    # --- 2. Current template -------------------------------------------------
    selected_template = template_map.get(template_key)
    if not selected_template:
        return redirect("survey_templates")

    # --- 3. Build “other templates” list (exclude current) -------------------
    other_templates = [
        {"key": k, **v}
        for k, v in template_map.items()
        if k != template_key
    ][:6]  # grab up to 6

    # --- 4. Handle POST -> create survey -------------------------------------
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        question_texts = request.POST.getlist("question_texts")
        question_types = request.POST.getlist("question_types")
        allow_multiple_flags = request.POST.getlist("allow_multiple")
        required_flags = request.POST.getlist("required_flags")
        question_options_raw = request.POST.getlist("question_options")

        survey = Survey.objects.create(
            title=title,
            owner=request.user,
            template_key=template_key,
        )

        for i in range(len(question_texts)):
            text = question_texts[i].strip()
            q_type = question_types[i] if i < len(question_types) else "text"
            allow_multi = str(i) in allow_multiple_flags
            required = str(i) in required_flags
            options_raw = question_options_raw[i] if i < len(question_options_raw) else ""
            options = [opt.strip() for opt in options_raw.split(",") if opt.strip()]

            if text:
                Question.objects.create(
                    survey=survey,
                    text=text,
                    type=q_type,
                    allow_multiple=allow_multi,
                    required=required,
                    options=options,
                )

        Notification.objects.create(
    user=request.user,
    message=f"✏️ Survey '{survey.title}' was updated."
        )

        return redirect("survey_review", survey_id=survey.id)

    # --- 5. Render ------------------------------------------------------------
    return render(
        request,
        "surveys/edit_template_survey.html",
        {
            "template_key": template_key,
            "template": selected_template,
            "other_templates": other_templates,  # ⬅️  pass to template
        },
    )




def survey_analytics(request):
    return render(request, "surveys/survey_analytics.html")

def dashboard_analytics_data(request):
    surveys = Survey.objects.filter(owner=request.user)
    responses = Response.objects.filter(survey__in=surveys)

    survey_titles = [s.title for s in surveys]
    counts = [responses.filter(survey=s).count() for s in surveys]

    return JsonResponse({
        "labels": survey_titles,
        "completionRates": counts
    })

def survey_management(request):
    return render(request, "surveys/survey_management.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Branding

@login_required
def branding_settings(request):
    branding, created = Branding.objects.get_or_create(user=request.user)

    if request.method == "POST":
        branding.color = request.POST.get("color", "#7C3AED")
        branding.font = request.POST.get("font", "Inter")

        if "logo" in request.FILES:
            branding.logo = request.FILES["logo"]

        branding.save()
       
        messages.success(request, "Branding preferences saved successfully!")
        return redirect("dashboard")
        

    return render(request, "surveys/branding_settings.html", { "branding": branding })


@login_required
def edit_existing_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, owner=request.user)

    if request.method == "POST":
        survey.title = request.POST.get("title", "").strip()
        survey.save()

        # Clear existing questions
        Question.objects.filter(survey=survey).delete()

        # Get lists from dynamic form fields
        texts = request.POST.getlist("question_texts")
        types = request.POST.getlist("question_types")
        allow_multiple_flags = request.POST.getlist("allow_multiple")
        required_flags = request.POST.getlist("required_flags")
        options_raw = request.POST.getlist("question_options")

        for i in range(len(texts)):
            text = texts[i].strip()
            qtype = types[i] if i < len(types) else "text"
            allow_multi = str(i) in allow_multiple_flags
            required = str(i) in required_flags
            options = [opt.strip() for opt in options_raw[i].split(",")] if i < len(options_raw) else []

            if text:
                Question.objects.create(
                    survey=survey,
                    text=text,
                    type=qtype,
                    allow_multiple=allow_multi,
                    required=required,
                    options=options
                )

        return redirect("survey_review", survey_id=survey.id)
    Notification.objects.create(
    user=request.user,
    message=f"🧩 Template '{template_key}' was edited."
    )

    return render(request, "surveys/edit_existing_survey.html", { "survey": survey })


@login_required
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, owner=request.user)
    survey.delete()

    Notification.objects.create(
    user=request.user,
    message=f"🗑️ Survey '{survey.title}' was deleted."
    )
    return redirect("dashboard")


from django.shortcuts import render, redirect, get_object_or_404
from .models import Survey, Question, Response, Branding

def fill_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug)

    # 🔗 Get the branding of the survey owner
    branding = Branding.objects.filter(user=survey.owner).first()

    if request.method == "POST":
        for question in survey.questions.all():
            key = f"question_{question.id}"
            answer = request.POST.getlist(key) if question.allow_multiple else request.POST.get(key, "").strip()

            if question.required and not answer:
                error_msg = f"Please answer the question: '{question.text}'"
                return render(request, "surveys/fill_survey.html", {
                    "survey": survey,
                    "error": error_msg,
                    "branding": branding
                })

            if answer:
                if isinstance(answer, list):
                    for a in answer:
                        Response.objects.create(survey=survey, question=question, answer=a)
                else:
                    Response.objects.create(survey=survey, question=question, answer=answer)

        return render(request, "surveys/thank_you.html", {
            "survey": survey,
            "branding": branding  # Optional: match thank-you page styling too
        })
    Notification.objects.create(
    user=survey.owner,
    message=f"📝 New response submitted for '{survey.title}'"
    )

    return render(request, "surveys/fill_survey.html", {
        "survey": survey,
        "branding": branding
    })
