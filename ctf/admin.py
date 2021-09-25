from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.formats import base_formats

from .models import Problem, UserProblem, Information, Inquiry
from django.contrib import admin


class ProblemResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    name = Field(attribute='name', column_name='name')
    file = Field(attribute='file', column_name='file')
    statement = Field(attribute='statement', column_name='statement')
    genre = Field(attribute='genre', column_name='genre')
    level = Field(attribute='level', column_name='level')
    score = Field(attribute='score', column_name='score')
    answer = Field(attribute='answer', column_name='answer')
    created_at = Field(attribute='created_at', column_name='created_at')
    updated_at = Field(attribute='updated_at', column_name='updated_at')

    class Meta:
        model = Problem
        fields = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')


class UserProblemResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    custom_user_id = Field(attribute='custom_user_id', column_name='custom_user_id')
    problem_id = Field(attribute='problem_id', column_name='problem_id')
    problem_correct_answer = Field(attribute='problem_correct_answer', column_name='problem_correct_answer')
    corrected_at = Field(attribute='corrected_at', column_name='corrected_at')

    class Meta:
        model = UserProblem
        fields = ('id', 'custom_user_id', 'problem_id', 'problem_correct_answer', 'corrected_at')


class InformationResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    title = Field(attribute='title', column_name='title')
    contents = Field(attribute='contents', column_name='contents')
    created_at = Field(attribute='created_at', column_name='created_at')
    updated_at = Field(attribute='updated_at', column_name='updated_at')

    class Meta:
        model = Information
        fields = ('id', 'title', 'contents', 'created_at', 'updated_at')


class InquiryResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id')
    name = Field(attribute='name', column_name='name')
    email = Field(attribute='email', column_name='email')
    subject = Field(attribute='subject', column_name='subject')
    contents = Field(attribute='contents', column_name='contents')

    class Meta:
        model = Inquiry
        fields = ('id', 'name', 'email', 'subject', 'contents', 'created_at')


class ProblemAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'file', 'statement', 'genre', 'level', 'score', 'answer', 'created_at', 'updated_at')
    list_filter = ('genre', 'level', 'score', 'created_at', 'updated_at')

    base_formats.CSV.CONTENT_TYPE = 'text/csv; charset=CP932'
    resource_class = ProblemResource

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
        # ignore_conflicts=Trueにより更新時は何もしない（IDは増える）
        UserProblem.objects.bulk_create(add_user_problem, ignore_conflicts=True)


class UserProblemAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'id', 'custom_user_id', 'problem_id', 'problem_correct_answer', 'corrected_at')
    list_display_links = ('id', 'custom_user_id', 'problem_id')
    search_fields = (
        'id', 'custom_user_username', 'problem__name', 'custom_user__id', 'problem__id', 'problem_correct_answer',
        'corrected_at')
    list_filter = ('custom_user__username', 'problem__name', 'problem_correct_answer', 'corrected_at')

    base_formats.CSV.CONTENT_TYPE = 'text/csv; charset=CP932'
    resource_class = UserProblemResource


class InformationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'contents', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    base_formats.CSV.CONTENT_TYPE = 'text/csv; charset=CP932'
    resource_class = InformationResource


class InquiryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'contents', 'created_at')
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'email', 'subject', 'contents', 'created_at')
    list_filter = ('name', 'email', 'created_at')

    base_formats.CSV.CONTENT_TYPE = 'text/csv; charset=CP932'
    resource_class = InquiryResource


admin.site.register(Problem, ProblemAdmin)
admin.site.register(UserProblem, UserProblemAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Inquiry, InquiryAdmin)
