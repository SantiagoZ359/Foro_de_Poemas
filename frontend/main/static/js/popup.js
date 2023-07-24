// Simular clic en el botón de apertura del popup al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.getElementById("openPopupBtn").click();
    }, 2000); // Retraso de 2000 milisegundos (2 segundos)
});

document.getElementsByClassName("close")[0].addEventListener("click", function() {
    document.getElementById("loginPopup").style.display = "none";
});


document.addEventListener("DOMContentLoaded", function () {
setTimeout(function () {
    document.getElementById("openPopupBtn").click();
}, 5000); // Retraso de 5000 milisegundos (5 segundos)
});

document.getElementById("openPopupBtn").addEventListener("click", function () {
document.getElementById("loginPopup").style.display = "block";
document.body.style.overflow = "hidden"; // Ocultar el desplazamiento del cuerpo de la página
});

document.getElementsByClassName("close")[0].addEventListener("click", function () {
document.getElementById("loginPopup").style.display = "none";
document.body.style.overflow = "auto"; // Restaurar el desplazamiento del cuerpo de la página
});

