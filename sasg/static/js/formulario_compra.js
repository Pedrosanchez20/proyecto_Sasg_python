document.addEventListener('DOMContentLoaded', function() {
    // Obtiene la referencia al campo de productos
    var productosCheckbox = document.querySelectorAll('[name="productos"]');

    // Función para mostrar u ocultar el campo de cantidad
    function actualizarCampoCantidad() {
        var cantidadInput = document.getElementById('cantidad_producto'); // Reemplaza 'id_cantidad' con el ID real del campo de cantidad

        // Si hay algún producto seleccionado, muestra el campo de cantidad; de lo contrario, ocúltalo
        cantidadInput.style.display = productosCheckbox.checked ? 'block' : 'none';
    }

    // Agrega un evento de cambio a cada checkbox de productos
    productosCheckbox.forEach(function(checkbox) {
        checkbox.addEventListener('change', actualizarCampoCantidad);
    });

    // Llama a la función para asegurarte de que el campo de cantidad esté correctamente configurado al cargar la página
    actualizarCampoCantidad();
});