from django.shortcuts import redirect
from django.views.generic import TemplateView

from app.utility import ConversionTableResolver
from .common import get_player


class GoGoal(TemplateView):
    template_name = "app/go-goal.html"

    def get(self, request, *args, **kwargs):
        player = get_player(request)

        if player.progress != 5:
            return redirect('app:progress-error')

        difficulty = player.difficulty
        kwargs['difficulty'] = difficulty

        if difficulty.pk == 1:
            kwargs['goal'] = player.difficulty.goal.name
        else:
            kwargs['quizzes'] = player.difficulty.quizzes.all()
            kwargs['change'] = ('10' if (difficulty.pk == 2) else '16') + '進数'
            table = ConversionTableResolver.createTable(difficulty.pk)
            kwargs['corresponds'] = table.data

        return super().get(request, *args, **kwargs)
