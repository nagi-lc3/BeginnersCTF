// 問題解答済みなら背景を変える
$(function(){
    $('.check-solved').each(function(){
        if($(this).text().indexOf('解答済み☑') > -1){
            $(this).parents('.card-body').parents('.card').removeClass('bg-info');
            $(this).parents('.card-body').parents('.card').addClass('bg-dark');
        }
    });
});