from .models import Problem, UsersProblem, Information
from django.contrib import admin


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_filter = ('genre', 'level', 'score', 'created_at', 'updated_at')


class UserProblemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'custom_user', 'problem', 'custom_user_id', 'problem_id', 'problem_correct_answer', 'corrected_at')
    list_display_links = ('id', 'custom_user')
    search_fields = (
        'id', 'custom_user__username', 'problem__name', 'custom_user__id', 'problem__id', 'problem_correct_answer',
        'corrected_at')
    list_filter = ('custom_user__username', 'problem__name', 'problem_correct_answer', 'corrected_at')


class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(UsersProblem, UserProblemAdmin)
admin.site.register(Information, InformationAdmin)
