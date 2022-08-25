// funcion que devulve el csrf token de django
function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getToken('csrftoken');

// GESTION DE USUARIOS
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

function editar_usuario_modal(url){
  $("#EditarUsuarioModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}
function cambiar_estado_usuario(url, id){
  const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Estás seguro?',
      text: "Cambiará el estado del usuario",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Si, cambiar!',
      cancelButtonText: 'No, cancelar!',
      confirmButtonClass: "buttonSweetalert",
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
          $.ajax({
              url: url,
              type: 'POST',
              data: {"csrfmiddlewaretoken": csrftoken,"pk": id},
              success: function(data){
                  swalWithBootstrapButtons.fire(
                      'Modificado!',
                      'El estado del usuario ha sido modificado.',
                      'success'
                    ).then(function(){
                      location.reload();
                    })
                   
              }
            });
           
      } else if (
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Canecelado',
          'No se han aplicado cambios al usuario :)',
          'error'
        ).then(function(){
          location.reload();
        })
      }
    })


}

// GESTION DE ESTUDIANTES
function crear_estudiante_modal(url){
$("#CraerEstudianteModal").load(url, function (){ 
  $(this).appendTo("body").modal('show');
});
}

function ver_estudiante_modal(url){
$("#VerEstudianteModal").load(url, function (){ 
  $(this).appendTo("body").modal('show');
});
}

function editar_estudiante_modal(url){
$("#EditarEstudianteModal").load(url, function (){ 
  $(this).appendTo("body").modal('show');
});
}

function cambiar_estado_estudiante(url, id){
const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: 'btn btn-success',
      cancelButton: 'btn btn-danger'
    },
    buttonsStyling: false
  })
  
  swalWithBootstrapButtons.fire({
    title: '¿Estás seguro?',
    text: "Cambiará el estado del estudiante",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Si, cambiar!',
    cancelButtonText: 'No, cancelar!',
    confirmButtonClass: "buttonSweetalert",
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
        $.ajax({
            url: url,
            type: 'POST',
            data: {"csrfmiddlewaretoken": csrftoken,"pk": id},
            success: function(data){
                swalWithBootstrapButtons.fire(
                    'Modificado!',
                    'El estado del estudiante ha sido modificado.',
                    'success'
                  ).then(function(){
                    location.reload();
                  })
                 
            }
          });
         
    } else if (
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire(
        'Canecelado',
        'No se han aplicado cambios al estudiante :)',
        'error'
      ).then(function(){
        location.reload();
      })
    }
  })


}
// GESTION DE CARROS

function crear_carros_modal(url){
  $("#CrearCarroModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}

function editar_carro_modal(url){
  $("#EditarCarroModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}

function cambiar_estado_carro(url, placa){
  const swalWithBootstrapButtons = Swal.mixin({
      customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger'
      },
      buttonsStyling: false
    })
    
    swalWithBootstrapButtons.fire({
      title: '¿Estás seguro?',
      text: "Cambiará el estado del carro",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Si, cambiar!',
      cancelButtonText: 'No, cancelar!',
      confirmButtonClass: "buttonSweetalert",
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
          $.ajax({
              url: url,
              type: 'POST',
              data: {"csrfmiddlewaretoken": csrftoken,"placa": placa},
              success: function(data){
                  swalWithBootstrapButtons.fire(
                      'Modificado!',
                      'El estado del carro ha sido modificado.',
                      'success'
                    ).then(function(){
                      location.reload();
                    })
                   
              }
            });
           
      } else if (
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire(
          'Canecelado',
          'No se han aplicado cambios al carro :)',
          'error'
        ).then(function(){
          location.reload();
        })
      }
    })
  
  
  }

  // GESTION DE RUTAS

function BuscarRuta(placa){
  $("#"+placa).submit()
}

function AgregarEstudianteRuta(url){
  $("#AgregarEstudianteRutaModal").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}