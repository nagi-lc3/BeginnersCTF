from django.contrib.auth import get_user_model

from .models import Problem, UserProblem, Information, Inquiry
from django.contrib import admin


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_filter = ('genre', 'level', 'score', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        """モデル保存前にUserProblemにカラム追加"""
        super().save_model(request, obj, form, change)

        # 問題作成時点で中間テーブルにレコード追加
        add_user_problem = []
        # idカラムを全て取り出して配列で回す
        id_list = get_user_model().objects.values_list('id', flat=True)
        for i in id_list:
            user_problem = UserProblem(custom_user_id=i, problem_id=obj.id)
            add_user_problem.append(user_problem)
        UserProblem.objects.bulk_create(add_user_problem)


class UserProblemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'custom_user_id', 'problem_id', 'problem_correct_answer', 'corrected_at')
    list_display_links = ('id', 'custom_user_id', 'problem_id')
    search_fields = (
        'id', 'custom_user_username', 'problem__name', 'custom_user__id', 'problem__id', 'problem_correct_answer',
        'corrected_at')
    list_filter = ('custom_user__username', 'problem__name', 'problem_correct_answer', 'corrected_at')


class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'custom_user_id', 'subject', 'category', 'email', 'contents', 'created_at')
    list_display_links = ('id', 'custom_user_id', 'subject')
    search_fields = ('id', 'custom_user_id', 'subject', 'category', 'email', 'contents', 'created_at')
    list_filter = ('category', 'created_at')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(UserProblem, UserProblemAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Inquiry, InquiryAdmin)
