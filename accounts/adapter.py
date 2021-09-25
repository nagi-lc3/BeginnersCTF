from ctf.models import Problem, UserProblem
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model


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

        # custom_userモデルのランキングを更新
        update_custom_user = []
        # 点数と点数更新日時でソートしてカラムを全て取り出して配列で回す
        id_list = get_user_model().objects.values_list('id', flat=True).order_by('-score',
                                                                                 'score_updated_at')
        # rank = インデックス, user_id = アイテム
        for rank, user_id in enumerate(id_list):
            custom_user = get_user_model()(id=user_id, ranking=rank + 1)
            update_custom_user.append(custom_user)
        get_user_model().objects.bulk_update(update_custom_user, fields=['ranking'])
