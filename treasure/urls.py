from django.urls import path, include
from .views import *

app_name = 'treasure'
urlpatterns = [
    path('go-goal/', GoGoal.as_view(), name='go-goal'),
    path('opening/', Opening.as_view(), name='opening'),
    path('dif-sel/', DifSel.as_view(), name='dif-sel'),
    path('<int:pk>/on-goal/', OnGoal.as_view(), name='on-goal'),
    path('last/', Last.as_view(), name='last'),
    path('<int:hint_index>/hints/', Hints.as_view(), name='hints'),
    path('<int:hint_index>/answer/', Answer.as_view(), name='answer'),
    path('progress-error/', ProgressError.as_view(), name='progress-error'),
    path('reset/', Reset.as_view(), name='reset'),
]
