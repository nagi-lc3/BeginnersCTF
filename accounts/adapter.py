from ctf.models import Problem, UserProblem
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """モデル保存前にUserProblemにカラム追加"""
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        user.save()

        # ユーザ作成時点で中間テーブルにレコード追加
        add_user_problem = []
        # idカラムを全て取り出して配列で回す
        id_list = Problem.objects.values_list('id', flat=True)
        for i in id_list:
            user_problem = UserProblem(custom_user_id=user.id, problem_id=i)
            add_user_problem.append(user_problem)
        UserProblem.objects.bulk_create(add_user_problem)
