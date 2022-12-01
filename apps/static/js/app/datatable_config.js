//script que permite generar una tabla de datos con la información traducida
$.fn.dataTableExt.ofnSearch['string'] = function ( data ) {
return ! data ?
    '' :
    typeof data === 'string' ?
        data
            .replace( /\n/g, ' ' )
            .replace( /á/g, 'a' )
            .replace( /é/g, 'e' )
            .replace( /í/g, 'i' )
            .replace( /ó/g, 'o' )
            .replace( /ú/g, 'u' )
            .replace( /ê/g, 'e' )
            .replace( /î/g, 'i' )
            .replace( /ô/g, 'o' )
            .replace( /è/g, 'e' )
            .replace( /ï/g, 'i' )
            .replace( /ü/g, 'u' )
            .replace( /ç/g, 'c' )
            .replace( /Á/g, 'A' )
            .replace( /É/g, 'E' )
            .replace( /Í/g, 'I' )
            .replace( /Ó/g, 'O' )
            .replace( /Ú/g, 'U' )
             :
        data;
};

if ($('.datatable').length !== 0) {

    var options = {
        dom: '<"dataTables_wrapper dt-bootstrap"<"row"<"col-xl-7 d-block d-sm-flex d-xl-block justify-content-center"<"d-block d-lg-inline-flex mr-0 mr-sm-3"l><"d-block d-lg-inline-flex"B>><"col-xl-5 d-flex d-xl-block justify-content-center"fr>>t<"row"<"col-sm-5"i><"col-sm-7"p>>>',
        buttons: [
            { extend: 'excel', className: 'btn-sm m-l-5' }
        ],
        language: {
            "processing": "Procesando...",
            "lengthMenu": "Mostrar _MENU_ registros",
            "zeroRecords": "No se encontraron resultados",
            "emptyTable": "Ningún dato disponible en esta tabla",
            "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "infoFiltered": "(filtrado de un total de _MAX_ registros)",
            "search": "Buscar:",
            "decimal": "",
            "infoPostFix": "",
            "thousands": ",",
            "loadingRecords": "Cargando...",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            },
            "aria": {
                "sortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sortDescending": ": Activar para ordenar la columna de manera descendente"
            },
            buttons: {
                copyTitle: 'Copiado a portapapeles',
                copySuccess: {
                    _: '%d lineas copiadas',
                    1: '1 linea copiada'
                }
            }
        },
        //responsive: true,
        //colReorder: true,
        //keys: true,
        //rowReorder: true,
        //select: true
    };

    $('.datatable').DataTable(options);
}