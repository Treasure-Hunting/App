from django.shortcuts import redirect
from django.views.generic import TemplateView

from .common import get_player


class Hints(TemplateView):
    template_name = 'app/hints.html'

    def get(self, request, *args, **kwargs):
        # セッションからplayerの情報を取得
        player = get_player(request)

        if player.progress != kwargs['hint_index']:
            return redirect('app:progress-error')

        quiz_data = player.quizzes.get(order=kwargs['hint_index'])
        kwargs['hint'] = quiz_data.quiz.hint
        kwargs['difficulty'] = player.difficulty

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return redirect(
            'app:answer',
            hint_index=str(kwargs['hint_index'])
        )
