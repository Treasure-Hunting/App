$(window).on('beforeunload', function (e) {
    if (!window.isMoving) {
        return 'ブラウザの戻る機能を使うと正常に動作しなくなる可能性があります。';
    }
});

$('form').submit(function (e) {
    window.isMoving = true;
});
