// Autor: @jqcaper
// Configuraciones Generales
var nombre_tabla = "#tabla_contratos"; // id
var nombre_boton_eliminar = ".delete"; // Clase
var nombre_formulario_modal = "#frmEliminar"; //id
var nombre_ventana_modal = "#myModal"; // id
// Fin de configuraciones


    $(document).on('ready',function(){
        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#modal_idPresupuesto').val(Pid);
            $('#modal_name').text(name);
        });


        $(nombre_formulario_modal).ajaxForm(options);
    });
