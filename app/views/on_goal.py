from django.shortcuts import redirect
from django.views.generic import TemplateView

from .common import get_player


class OnGoal(TemplateView):
    template_name = 'app/on-goal.html'

    def get(self, request, **kwargs):
        player = get_player(request)

        if player.progress != 5:
            return redirect('app:progress-error')

        if kwargs['pk'] == player.difficulty.pk:
            player.progress = 6
            return redirect('app:last')

        kwargs['difficulty'] = player.difficulty

        return super().get(request, **kwargs)
