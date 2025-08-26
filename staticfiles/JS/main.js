// Mostrar alertas
function showAlert(message, type = "info", timeout = 3000) {
    const alertContainer = document.getElementById("alert-container");
    const wrapper = document.createElement("div");
    wrapper.innerHTML = `
        <div class="alert alert-${type} fade show shadow text-center text-nowrap" role="alert">
            ${message}
        </div>
    `;
    const alertElement = wrapper.firstElementChild;
    alertContainer.appendChild(alertElement);

    if (timeout) {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
            bsAlert.close();
        }, timeout);
    }
}

// Deshabilitar botón y mostrar spinner
function disableButtonWithSpinner(button, loadingText = "Procesando...") {
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        ${loadingText}
    `;
}

// Restaurar botón a su estado original
function enableButton(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// Actualizar reloj (fecha y hora)
function actualizarReloj(fechaId, horaId) {
    const now = new Date();

    const formatDate = {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };

    const formatTime = {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true
    };

    if (fechaId) {
        const fechaEl = document.getElementById(fechaId);
        if (fechaEl) fechaEl.textContent = now.toLocaleDateString('es-CO', formatDate);
    }
    if (horaId) {
        const horaEl = document.getElementById(horaId);
        if (horaEl) horaEl.textContent = now.toLocaleTimeString('es-CO', formatTime);
    }
}

// Inicializar reloj (Igual a la del sistema)
function iniciarReloj(fechaId, horaId) {
    function tick() {
        actualizarReloj(fechaId, horaId);
        const now = new Date();
        const delay = 1000 - now.getMilliseconds();
        setTimeout(tick, delay);
    }
    tick();
}

function cardInfo(tipo, contenido, icono) {
    let cardClass = "";

    switch (tipo) {
        case "success":
            cardClass = "bg-success-subtle border border-success-subtle text-success-emphasis";
            icono = icono || '<i class="bi bi-check-circle-fill fs-1"></i>';
            break;
        case "warning":
            cardClass = "bg-warning-subtle border border-warning-subtle text-warning-emphasis";
            icono = icono || '<i class="bi bi-exclamation-triangle-fill fs-1"></i>';
            break;
        case "error":
            cardClass = "bg-danger-subtle border border-danger-subtle text-danger-emphasis";
            icono = icono || '<i class="bi bi-x-circle-fill fs-1"></i>';
            break;
        default:
            cardClass = "bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis";
            icono = icono || '<i class="bi bi-info-circle-fill fs-1"></i>';
            break;
    }

    return `
        <div class="card ${cardClass} shadow-sm h-75 w-75">
            <div class="card-body d-flex justify-content-between align-items-center">
                <div class="flex-grow-1 text-center">
                    ${contenido}
                </div>
                <div class="ms-4">
                    ${icono}
                </div>
            </div>
        </div>
    `;
}
