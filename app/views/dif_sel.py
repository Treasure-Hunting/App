from random import shuffle

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from models import Difficulty, QuizData, Player


class DifSel(TemplateView):
    template_name = 'app/dif-sel.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('player_pk', -1) != -1:
            return redirect('app:progress-error')

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['difficulties'] = Difficulty.objects.all()
        return context

    def post(self, request, **kwargs):
        difficulty_pk = request.POST.get('difficulty', -1)
        difficulty = get_object_or_404(Difficulty, pk=difficulty_pk)

        quizzes = list(difficulty.quizzes.all())
        shuffle(quizzes)
        # プレイヤー作成
        player = Player.objects.create(difficulty=difficulty, progress=1)

        for i in range(len(quizzes)):
            player.quizzes.add(
                QuizData.objects.create(quiz=quizzes[i], order=i+1)
            )

        request.session['player_pk'] = player.pk

        return redirect('app:hints', hint_index=1)
