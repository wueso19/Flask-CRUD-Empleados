var updateModal = document.getElementById('update')
updateModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var recipient = button.getAttribute('data-bs-whatever')
    var empleado = recipient.replace(/[{('')}]/g, '').split(', ')
    console.log(empleado);
    var modalNombre = updateModal.querySelector('#txtNombre')
    var modalCorreo = updateModal.querySelector('#txtCorreo')
    var modalFoto = updateModal.querySelector('#updateFoto')
    modalNombre.value = empleado[1]
    modalCorreo.value = empleado[2]
    modalFoto.src = `/uploads/${empleado[3].trim()}`
    modalFoto.alt = `${empleado[3].trim()}`

    var btnGuardar = updateModal.querySelector('#updateForm')
    btnGuardar.setAttribute("action",`/update/${empleado[0].trim()}`)
})