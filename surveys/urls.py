from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    signup, user_logout, create_survey, survey_list, survey_responses, take_survey, download_responses_excel, download_responses_pdf, submit_feedback, delete_account,
    dashboard, survey_templates, use_template, branding_settings,download_responses_csv, download_responses_csv_single, update_survey_status,thank_you, settings_view, notifications_page,
    survey_analytics, survey_management, survey_review, dashboard_analytics_data,view_all_responses, edit_template_survey, edit_existing_survey, delete_survey, fill_survey
)

urlpatterns = [
    path("login/", LoginView.as_view(template_name="surveys/login.html"), name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", user_logout, name="logout"),
    path("create/", create_survey, name="create_survey"),
    path("surveys/", survey_list, name="survey_list"),
    path("survey/<slug:survey_slug>/", take_survey, name="take_survey"),
    path("survey/<slug:survey_slug>/responses/", survey_responses, name="survey_responses"),
    path("survey-review/<int:survey_id>/", survey_review, name="survey_review"),
    path("edit-template/<str:template_key>/", edit_template_survey, name="edit_template_survey"),
    path("edit-survey/<int:survey_id>/", edit_existing_survey, name="edit_existing_survey"),
    path('survey/<int:survey_id>/thankyou/', thank_you, name='thank_you'),

    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/analytics/", survey_analytics, name="survey_analytics"),
    path("dashboard/manage/", survey_management, name="survey_management"),
    path("dashboard/analytics-data/", dashboard_analytics_data, name="dashboard_analytics_data"),
    path("delete-survey/<int:survey_id>/", delete_survey, name="delete_survey"),
    path("templates/", survey_templates, name="survey_templates"),
    path("use-template/<str:template_key>/", use_template, name="use_template"),
    # path("settings/branding/", branding_settings, name="branding_settings"),
    path("responses/", view_all_responses, name="view_all_responses"),
    path("responses/download/", download_responses_csv, name="download_responses_csv"),

    path("responses/download/csv/<int:survey_id>/", download_responses_csv_single, name="download_responses_csv_single"),
    path("responses/download/excel/<int:survey_id>/", download_responses_excel, name="download_responses_excel"),
    path("responses/download/pdf/<int:survey_id>/", download_responses_pdf, name="download_responses_pdf"),
    path("update-survey-status/<int:survey_id>/", update_survey_status, name="update_survey_status"),

    path("survey/<slug:slug>/", fill_survey, name="fill_survey"),
    path("submit-feedback/", submit_feedback, name="submit_feedback"),
    path("settings/", settings_view, name="settings_page"),
    path("update-settings/", settings_view, name="update_settings"),
    path("delete-account/", delete_account, name="delete_account"),
    
    path("notifications/", notifications_page, name="notifications_page"),
]