$(document).ready(function(){
    $("#botaoPesquisa").click(function(){
        $(".temperaturas").fadeOut(1);
        $(".geografia").fadeOut(1);
        $(".temperaturas").fadeIn(4000);
        $(".geografia").fadeIn(4000);
    });
});