from django.shortcuts import redirect
from django.views import View

from .common import move_page_by_progress


class ProgressError(View):

    def get(self, request, **kwargs):
        if request.session.get('player_pk', -1) == -1:
            return redirect('app:dif-sel')

        return move_page_by_progress(request)
