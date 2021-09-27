$(function(){
    // 不必要な文字列を削除
    $('form').children('.mb-3').children('a').remove();
    $('form').children('.mb-3').children('br').remove();

    $(".mb-3").contents().each(function() {
        if (this.nodeType == 3) {
            $(this).remove();
        }
    });

});