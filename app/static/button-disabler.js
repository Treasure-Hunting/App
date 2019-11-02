$("form").submit(function (e) {
    const $form = $(e.currentTarget);
    const $btn = $form.find('input[type="submit"]');

    $btn.prop('disabled', true);
    $btn.val('読み込み中…');
});
