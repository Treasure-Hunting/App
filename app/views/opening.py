from django.shortcuts import redirect
from django.views.generic import TemplateView


class Opening(TemplateView):
    template_name = 'app/opening.html'

    def post(self, request, **kwargs):
        if request.session.get('player_pk', -1) != -1:
            return redirect('app:reset')
        else:
            return redirect('app:dif-sel')
