from django.shortcuts import redirect
from django.views.generic import TemplateView

from .common import get_player


class Answer(TemplateView):
    template_name = "app/answer.html"

    def get(self, request, *args, **kwargs):
        # セッションからplayerの情報を取得
        player = get_player(request)

        if player.progress != kwargs['hint_index']:
            return redirect('app:progress-error')

        kwargs['difficulty'] = player.difficulty

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # キャンセル
        if self.request.POST.get('cancel', -1) == '1':
            return redirect('app:hints',
                            hint_index=str(kwargs['hint_index']))
        # キーワードを受け取ったなら
        elif self.request.POST.get('number', None):
            # セッションからplayerの情報を取得
            player = get_player(request)
            # 簡略化
            # keyword = {1: player.quiz1.keyword, 2: player.quiz2.keyword,
            #           3: player.quiz3.keyword, 4: player.quiz4.keyword}
            # 受け取ったキーワードが現在のページの答えと等しいなら
            quiz_data = player.quizzes.get(order=kwargs['hint_index'])
            keyword = quiz_data.quiz.keyword

            if keyword == self.request.POST.get('number', None):
                # 正解と送信
                # kwargs['result'] = '正解'
                # 現在が４ページ目なら
                if kwargs['hint_index'] == 4:
                    player.progress = 5
                    player.save()
                    # ゴール誘導ページへ
                    return redirect('app:go-goal')
                else:
                    player.progress = kwargs['hint_index'] + 1
                    player.save()
                    # 次のページへ
                    return redirect('app:hints',
                                    hint_index=str(kwargs['hint_index'] + 1))
            else:
                # 不正解と送信
                kwargs['result'] = '不正解'

        return self.get(request, *args, **kwargs)
