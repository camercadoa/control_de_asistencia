// Mapear status de backend a clases de Bootstrap
function mapStatusToBootstrap(status) {
    switch (status) {
        case "success": return "success";
        case "error": return "danger";
        case "warning": return "warning";
        case "info": return "info";
        default: return "secondary";
    }
}

// Procesar respuesta estandarizada del backend
function handleBackendResponse(data, { onSuccess = null, onWarning = null, onError = null, showAlertMsg = true } = {}) {
    const { status, message, data: payload } = data;
    const type = mapStatusToBootstrap(status);

    if (showAlertMsg) {
        showAlert(message, type);
    }

    if (status === "success" && onSuccess) {
        onSuccess(payload, message);
    } else if (status === "warning" && onWarning) {
        onWarning(payload, message);
    } else if (status === "error" && onError) {
        onError(payload, message);
    }
}

// Mostrar alertas
function showAlert(message, type = "info", timeout = 3000) {
    const alertContainer = document.getElementById("alert-container");
    const wrapper = document.createElement("div");
    wrapper.innerHTML = `
        <div class="alert alert-${type} fade show shadow text-center text-nowrap small" role="alert">
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

// Crear tarjeta de información con respuesta del servidor
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
        case "info":
            cardClass = "bg-info-subtle border border-info-subtle text-info-emphasis";
            icono = icono || '<i class="bi bi-info-circle-fill fs-1"></i>';
            break;
        default:
            cardClass = "bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis";
            icono = icono || '<i class="bi bi-dot fs-1"></i>';
            break;
    }

    const cardId = `card-${Date.now()}`;

    // Creamos el HTML
    const html = `
        <div id="${cardId}" class="card ${cardClass} shadow-lg rounded-4 fade show h-75 w-100 m-5">
            <div class="card-body d-flex justify-content-between align-items-center px-4 py-3">
                <div class="flex-grow-1 text-center">
                    ${contenido}
                </div>
                <div class="ms-4">
                    ${icono}
                </div>
            </div>
        </div>
    `;

    setTimeout(() => {
        const el = document.getElementById(cardId);
        if (el) {
            el.classList.remove("show");
            el.addEventListener("transitionend", () => {
                el.remove();
            }, { once: true });
        }
    }, 6000); // 6 segundos en pantalla

    return html;
}

// Marcar inputs como inválidos
function markInvalid(inputs, message = null) {
    if (!Array.isArray(inputs)) inputs = [inputs];
    inputs.forEach(input => {
        if (!input) return;
        input.classList.add("is-invalid");

        // Si existe feedback, actualizar texto
        if (message) {
            let feedback = input.parentElement.querySelector(".invalid-feedback");
            if (!feedback) {
                feedback = document.createElement("div");
                feedback.classList.add("invalid-feedback");
                input.parentElement.appendChild(feedback);
            }
            feedback.textContent = message;
        }
    });
}

// Limpiar estado inválido
function clearInvalid(inputs) {
    if (!Array.isArray(inputs)) inputs = [inputs];
    inputs.forEach(input => input?.classList.remove("is-invalid"));
}

// Limpiar invalid al escribir
function attachClearOnInput(inputs) {
    if (!Array.isArray(inputs)) inputs = [inputs];
    inputs.forEach(input => {
        if (!input) return;
        input.addEventListener("input", () => input.classList.remove("is-invalid"));
    });
}

// Mostrar spinner en un contenedor
function showSpinner(container, colspan = 1, message = "Cargando...") {
    container.innerHTML = `
        <tr>
            <td colspan="${colspan}" class="text-center py-4">
                <div class="d-flex flex-column align-items-center">
                    <div class="spinner-border text-secondary-emphasis mb-2" role="status"></div>
                    <span class="text-muted small">${message}</span>
                </div>
            </td>
        </tr>
    `;
}

// Ocultar spinner
function hideSpinner(container) {
    container.innerHTML = "";
}

// Inicializar DataTable con configuración por defecto
function initDataTable(selector, options = {}) {
    const defaultConfig = {
        processing: true,
        serverSide: false,
        responsive: true,
        pageLength: 15,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/es-ES.json"
        },
        // Layout: botones a la izquierda del buscador
        dom: '<"d-flex justify-content-between align-items-center mb-2"lfB>rt<"d-flex justify-content-between align-items-center mt-2"ip>',
        buttons: [
            {
                text: '<i class="bi bi-arrow-clockwise"></i> Recargar',
                className: 'btn btn-sm bg-primary-subtle border border-primary-subtle text-primary-emphasis',
                action: function (e, dt, node, config) {
                    dt.ajax.reload(null, false); // recarga sin resetear página
                }
            },
            {
                extend: 'excelHtml5',
                text: '<i class="bi bi-file-earmark-excel"></i> Excel',
                className: 'btn btn-sm bg-success-subtle border border-success-subtle text-success-emphasis',
                titleAttr: 'Exportar a Excel'
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="bi bi-file-earmark-pdf"></i> PDF',
                className: 'btn btn-sm bg-danger-subtle border border-danger-subtle text-danger-emphasis',
                titleAttr: 'Exportar a PDF',
                orientation: 'landscape',
                pageSize: 'A4'
            }
        ],
        columns: [] // Definir columnas por defecto (si no se pasan en options)
    };

    // Fusionar defaults con opciones personalizadas
    const config = $.extend(true, {}, defaultConfig, options);

    return $(selector).DataTable(config);
}


// Resetea un formulario dentro de un modal y limpia errores de validación
function resetModalForm(modalId, formId, inputIds = []) {
    const modal = document.getElementById(modalId);
    const form = document.getElementById(formId);

    if (!modal || !form) return;

    modal.addEventListener("hidden.bs.modal", () => {
        form.reset();

        // limpiar estados inválidos
        const inputs = inputIds.map(id => document.getElementById(id)).filter(Boolean);
        if (inputs.length) {
            clearInvalid(inputs);
        }
    });
}
