// function abrir_mapa(url){
//   $(".DivMapa").load(url, function (){ 
//     $(this).appendTo(this);
//   });
// }

// ____________________________________________________________ david ___________________

function crear_usuario_modal(url){
  $("#CraerUsuarioModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}

function ver_usuario_modal(url){
    $("#VerUsuarioModal").load(url, function (){ 
      $(this).appendTo("body").modal('show');
    });
  }