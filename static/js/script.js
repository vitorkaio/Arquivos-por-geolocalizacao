$('document').ready(function () {
      $("#botaoPesquisa").click(function(){
        $(".temperaturas").fadeOut(1);
        $(".geografia").fadeOut(1);
        $(".temperaturas").fadeIn(4000);
        $(".geografia").fadeIn(4000);
    });
  $('ul.tabs').tabs();
  $(".button-collapse").sideNav();

  function getPosition(){
  // Verifica se o browser do usuario tem suporte a Geolocation
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (posicao) {

          var p = posicao.coords.latitude + ',' + posicao.coords.longitude;
          //document.getElementById('local').setAttribute('name', p.toString())
          // Requisição HTTP
          var req = new XMLHttpRequest();
          req.open('GET', "/coordenadas/" + p, false);
          req.send('ddd');
          var out = req.responseText;

      });
  }
}
getPosition();

});




