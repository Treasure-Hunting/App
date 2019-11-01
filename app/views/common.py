from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from models import Player


def get_player(request):
    return get_object_or_404(
        Player,
        pk=request.session.get('player_pk', -1)
    )


def move_page_by_progress(request):
    player = get_player(request)
    progress = player.progress

    if progress <= 4:
        return redirect('app:hints', hint_index=progress)
    elif progress == 5:
        return redirect('app:go-goal')
    elif progress == 6 or progress == 7:
        return redirect('app:last')

    return Http404()
