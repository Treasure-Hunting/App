from django.shortcuts import redirect
from django.views.generic import TemplateView

from .common import get_player, move_page_by_progress


class Reset(TemplateView):
    template_name = 'app/reset.html'

    def get(self, request, *args, **kwargs):
        if (request.session.get('player_pk', -1) == -1 or
                get_player(request).progress == 7):
            return redirect('app:progress-error')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        answer = request.POST.get('answer', 'n')
        player = get_player(request)

        if answer == 'y':
            player.delete()
            del request.session['player_pk']
            return redirect('app:dif-sel')
        else:
            return move_page_by_progress(request)
