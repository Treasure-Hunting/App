from django.views.generic import TemplateView

from .common import get_player


class Last(TemplateView):
    template_name = 'app/last.html'

    def get(self, request, **kwargs):
        player = get_player(request)

        kwargs['difficulty'] = player.difficulty
        kwargs['progress'] = player.progress

        return super().get(request, **kwargs)

    def post(self, request, **kwargs):
        player = get_player(request)
        player.progress = 7
        player.save()

        kwargs['progress'] = player.progress

        return super().get(request, **kwargs)
