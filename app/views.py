from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import Http404
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from .models import Player, Difficulty, Goal, Quiz, QuizData
from random import shuffle
from .utility import ConversionTableResolver


class GoGoal(TemplateView):
    template_name = "app/go-goal.html"

    def get(self, request, *args, **kwargs):
        player = get_player(request)

        if (player.progress != 5):
            return redirect('app:progress-error')

        difficulty_pk = player.difficulty.pk
        kwargs['difficulty_pk'] = difficulty_pk
        if(difficulty_pk == 1):
            kwargs['goal'] = player.difficulty.goal.name
        else:
            kwargs['quizzes'] = player.difficulty.quizzes.all()
            kwargs['change'] = ('10' if (difficulty_pk == 2) else '16') + '進数'
            table = ConversionTableResolver.createTable(difficulty_pk)
            kwargs['corresponds'] = table.data
        return super().get(request, *args, **kwargs)


class Hints(TemplateView):
    template_name = 'app/hints.html'

    def get(self, request, *args, **kwargs):
        # セッションからplayerの情報を取得
        player = get_player(request)
        if (player.progress != kwargs['hint_index']):
            return redirect('app:progress-error')
        # 簡略化
        # hint = {1: player.quiz1.hint, 2: player.quiz2.hint,
        #        3: player.quiz3.hint, 4: player.quiz4.hint}
        # 現在のページに対応したヒントを送信
        # kwargs['hint'] = hint[kwargs['hint_index']]
        quiz_data = player.quizzes.get(order=kwargs['hint_index'])
        kwargs['hint'] = quiz_data.quiz.hint
        kwargs['difficulty_pk'] = player.difficulty
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # キーワードを受け取ったなら
        # if self.request.POST.get('number', None):
        #     セッションからplayerの情報を取得
        #     player = get_player(request)
        #      簡略化
        #      keyword = {1: player.quiz1.keyword, 2: player.quiz2.keyword,
        #                3: player.quiz3.keyword, 4: player.quiz4.keyword}
        #     受け取ったキーワードが現在のページの答えと等しいなら
        #     quiz_data = player.quizzes.get(order=kwargs['hint_index'])
        #     keyword = quiz_data.quiz.keyword
        #     if keyword == self.request.POST.get('number', None):
        #         正解と送信
        #         kwargs['result'] = '正解'
        #         現在が４ページ目なら
        #        if kwargs['hint_index'] == 4:
        #            player.progress = 5
        #            player.save()
        #            ゴール誘導ページへ
        #            return redirect('app:go-goal')
        #        else:
        #            player.progress = kwargs['hint_index'] + 1
        #            player.save()
        #            # 次のページへ
        #            return redirect('app:hints',
        #                            hint_index=str(kwargs['hint_index'] + 1))
        #    else:
        #        # 不正解と送信
        #        kwargs['result'] = '不正解'
        return redirect('app:answer',
                        hint_index=str(kwargs['hint_index']))
        # return self.get(request, *args, **kwargs)


class Answer(TemplateView):
    template_name = "app/answer.html"

    def get(self, request, *args, **kwargs):
        # セッションからplayerの情報を取得
        player = get_player(request)
        if (player.progress != kwargs['hint_index']):
            return redirect('app:progress-error')
        kwargs['difficulty_pk'] = player.difficulty
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


class Opening(TemplateView):
    template_name = 'app/opening.html'

    def post(self, request, **kwargs):
        if(request.session.get('player_pk', -1) != -1):
            return redirect('app:reset')
        else:
            return redirect('app:dif-sel')


class DifSel(TemplateView):
    template_name = 'app/dif-sel.html'

    def get(self, request, *args, **kwargs):
        if (request.session.get('player_pk', -1) != -1):
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


class OnGoal(TemplateView):
    template_name = 'app/on-goal.html'

    def get(self, request, **kwargs):
        player = get_player(request)

        if (player.progress != 5):
            return redirect('app:progress-error')

        if kwargs['pk'] == player.difficulty.pk:
            player.progress = 6
            return redirect('app:last')
        return super().get(request, **kwargs)


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


class ProgressError(View):

    def get(self, request, **kwargs):
        if (request.session.get('player_pk', -1) == -1):
            return redirect('app:dif-sel')
        return move_page_by_progress(request)


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
        if (answer == 'y'):
            player.delete()
            del request.session['player_pk']
            return redirect('app:dif-sel')
        else:
            return move_page_by_progress(request)


def get_player(request):
    return get_object_or_404(Player,
                             pk=request.session.get('player_pk', -1))


def move_page_by_progress(request):
    player = get_player(request)
    progress = player.progress
    if (progress <= 4):
        return redirect('app:hints', hint_index=progress)
    elif (progress == 5):
        return redirect('app:go-goal')
    elif (progress == 6 or progress == 7):
        return redirect('app:last')
    return Http404()
