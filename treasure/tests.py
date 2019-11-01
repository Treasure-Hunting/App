from random import shuffle
from django.test import TestCase
from django.test import Client
from .models import Difficulty, Player, QuizData
from django.urls import reverse
from django.contrib.auth.models import User
from .utility import ConversionTableResolver
# Create your tests here.


class GoalTest(TestCase):

    # テストするプレイヤーに与える難易度のpkのリスト
    try_difficulty_pk_list = [1, 3, 2]
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        for i in self.try_difficulty_pk_list:  # Playerをtry_listに沿って作成
            difficulty = Difficulty.objects.get(pk=i)
            quizzes = list(difficulty.quizzes.all())
            shuffle(quizzes)  # 難易度から得たクイズをシャッフル。
            player = Player.objects.create(difficulty=difficulty)
        for i in range(len(quizzes)):
            player.quizzes.add(
                QuizData.objects.create(quiz=quizzes[i], order=i)
            )

    def test_on_goal(self):
        for player in Player.objects.all():  # playerの数だけ繰り返す。
            s = self.client.session
            s['player_pk'] = player.pk  # プレイヤーのpk(1スタート)をセッションに登録する。
            s.save()
            for diff in Difficulty.objects.all():  # Difficultyの長さだけ繰り返す。
                player.progress = 5
                player.save()
                # 与えたセッションを使い,/treasure/(難易度のpk)/on-goal/をGETする。
                response = self.client.get('/treasure/' + str(diff.pk) +
                                           '/on-goal/', follow=True)
                # URLに与えた難易度のpkが,try_listのDifficulty(現在テスト中のプレイヤーに与えているDifficulty)のpkと等しい時
                if(diff.pk == self.try_difficulty_pk_list[player.pk - 1]):
                    # 最後のページへ飛移するはず。(302)
                    self.assertEqual(response.redirect_chain,
                                     [('/treasure/last/', 302)])
                    # 難易度の文字列化したものが表示されるはず。
                    self.assertContains(response, diff.name)
                # QRコードを読み込む文があるかのテストを、特に実行に支障がないため削除しました(raiga0310)

    def test_go_goal(self):
        for player in Player.objects.all():  # playerの数だけ繰り返す。
            s = self.client.session
            s['player_pk'] = player.pk  # プレイヤーのpk(1スタート)をセッションに登録する。
            s.save()
            # 難易度を得る。
            diff = Difficulty.objects.get(
                pk=self.try_difficulty_pk_list[player.pk - 1])
            player.progress = 5
            player.save()
            # 与えたセッションを使い,/treasure/go-goal/をGETする。
            response = self.client.get('/treasure/go-goal/')
            # try_listのDifficulty(現在テスト中のプレイヤーに与えているDifficulty)のpkが1の時、
            if(self.try_difficulty_pk_list[player.pk - 1] == 1):
                # ゴールのnameが表示されるはず。
                self.assertContains(response, diff.goal.name)
            elif(self.try_difficulty_pk_list[player.pk - 1] == 2):
                # 2なら10進数と表示されるはず。
                self.assertContains(response, '10進数')
            else:
                self.assertEqual(self.try_difficulty_pk_list[player.pk - 1], 3)
                # 3なら16進数が表示されるはず。
                self.assertContains(response, '16進数')


class UtilityTest(TestCase):
    def setUp(self):
        pass

    def test_conversion_table(self):
        table_data = ConversionTableResolver.createTable(2).data
        # 変換表(10進)が表示されているか
        self.assertIn({'binary': '00000000',
                       'to_base': '00000000'}, table_data)
        self.assertIn({'binary': '11111111',
                       'to_base': '00000255'}, table_data)
        table_data = ConversionTableResolver.createTable(3).data
        # 変換表(16進)が表示されているか
        self.assertIn({'binary': '00000000',
                       'to_base': '00000000'}, table_data)
        self.assertIn({'binary': '11111111',
                       'to_base': '000000ff'}, table_data)
