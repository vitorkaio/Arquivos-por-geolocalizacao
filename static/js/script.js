$(document).ready(function () {
  $('ul.tabs').tabs();
  $(".button-collapse").sideNav();
});

function getPosition() {

  // Verifica se o browser do usuario tem suporte a Geolocation
  if (navigator.geolocation) {

      navigator.geolocation.getCurrentPosition(function (posicao) {

          var p = posicao.coords.latitude + ',' + posicao.coords.longitude;
          //document.getElementById('local').setAttribute('name', p.toString())
          // Requisição HTTP
          var req = new XMLHttpRequest();
          req.open('GET', "http://10.3.1.52:5000/coordenadas/" + p, false);
          req.send('ddd');
          var out = req.responseText;

      });
  }
}
