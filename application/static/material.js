$('.material-field').on('change', function() {
    $(this).attr("class", "material-field");
});

$('.material-field').on('focusin', function () {
    $(this).find('.material-label').attr('class', 'material-label-focus');
    $(this).find('.material-input').attr('class', 'material-input-focus');
});

$('.material-field').on('focusout', function () {
    $(this).find('.material-label-focus').attr('class', 'material-label');
    $(this).find('.material-input-focus').attr('class', 'material-input');
});

$('.material-file').on('change', function () {
    var filename = $(this).val();
    var filename = filename.split("\\");
    var filename = filename[filename.length - 1];
    $('label.material-file').html(filename);
    $('label.material-file').addClass('material-file-selected');
});