function remove_flash() {
    const element = document.getElementById("flash-messages");
    element.remove();
}

function open_diag() {
    const dialogEl = document.getElementById('myDialog');
    dialogEl.showModal();
}

function close_diag() {
    const dialogEl = document.getElementById('myDialog');
    dialogEl.close();
}