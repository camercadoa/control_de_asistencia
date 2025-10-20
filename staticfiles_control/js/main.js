// ============================================================================
// TOOLTIPS BOOTSTRAP
// ============================================================================

/**
 * Inicializa todos los tooltips de Bootstrap dentro de un contenedor.
 * @param {Document|HTMLElement} [container=document] - Elemento donde buscar tooltips.
 */
function initTooltips(container = document) {
    const tooltipTriggerList = [].slice.call(container.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));
}


// ============================================================================
// MAPEO DE ESTADOS Y RESPUESTAS DEL BACKEND
// ============================================================================

/**
 * Convierte un estado del backend en una clase de Bootstrap.
 * @param {string} status - Estado recibido (success, error, warning, info).
 * @returns {string} - Clase de Bootstrap correspondiente.
 */
function mapStatusToBootstrap(status) {
    switch (status) {
        case "success": return "success";
        case "error": return "danger";
        case "warning": return "warning";
        case "info": return "info";
        default: return "secondary";
    }
}

/**
 * Procesa la respuesta del backend mostrando alertas y ejecutando callbacks.
 * @param {Object} data - Respuesta del backend.
 * @param {string} data.status - Estado de la respuesta.
 * @param {string} data.message - Mensaje del backend.
 * @param {any} data.data - Datos de la respuesta.
 * @param {Object} [options={}] - Configuración adicional.
 * @param {Function} [options.onSuccess] - Callback en caso de éxito.
 * @param {Function} [options.onWarning] - Callback en caso de advertencia.
 * @param {Function} [options.onError] - Callback en caso de error.
 * @param {Function} [options.onInfo] - Callback en caso de información.
 * @param {boolean} [options.showAlertMsg=true] - Mostrar o no el mensaje en alerta.
 */
function handleBackendResponse(data, { onSuccess = null, onWarning = null, onError = null, onInfo = null, showAlertMsg = true } = {}) {
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
    } else if (status === "info" && onInfo) {
        onInfo(payload, message);
    }
}


// ============================================================================
// ALERTAS Y NOTIFICACIONES
// ============================================================================

/**
 * Muestra una alerta Bootstrap dentro de #alert-container.
 * @param {string} message - Texto a mostrar.
 * @param {string} [type="info"] - Tipo de alerta (success, danger, warning, info).
 * @param {number|null} [timeout=3000] - Tiempo en ms antes de cerrarse automáticamente. Si es null, no se cierra.
 */
function showAlert(message, type = "info", timeout = 3000) {
    const alertContainer = document.getElementById("alert-container");
    const wrapper = document.createElement("div");
    wrapper.innerHTML = `
        <div class="alert alert-${type} fade show shadow text-center text-nowrap small mx-auto" role="alert">
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

/**
 * Crea una tarjeta de información que se elimina automáticamente después de 6 segundos.
 * @param {string} tipo - Tipo de tarjeta (success, warning, error, info).
 * @param {string} contenido - Texto o contenido a mostrar.
 * @param {string} [icono] - HTML de ícono opcional.
 * @returns {string} - HTML de la tarjeta.
 */
function cardInfo(tipo, contenido, icono) {
    let cardClass = "";
    let iconHTML = icono || "";

    switch (tipo) {
        case "success":
            cardClass = "border-success text-success";
            iconHTML = iconHTML || '<i class="bi bi-check-circle-fill fs-1"></i>';
            cardTitle = "Registro Exitoso";
            break;
        case "warning":
            cardClass = "border-warning text-warning";
            iconHTML = iconHTML || '<i class="bi bi-exclamation-triangle-fill fs-1"></i>';
            cardTitle = "Atención";
            break;
        case "error":
            cardClass = "border-danger text-danger";
            iconHTML = iconHTML || '<i class="bi bi-x-circle-fill fs-1"></i>';
            cardTitle = "Error";
            break;
        case "info":
            cardClass = "border-info text-info";
            iconHTML = iconHTML || '<i class="bi bi-info-circle-fill fs-1"></i>';
            cardTitle = "Información";
            break;
        default:
            cardClass = "border-secondary text-secondary";
            iconHTML = iconHTML || '<i class="bi bi-dot fs-1"></i>';
            cardTitle = "Default";
            break;
    }

    const cardId = `card-${Date.now()}`;
    const html = `
        <div id="${cardId}" class="card ${cardClass} shadow-sm rounded-4 fade show col-10 col-md-8 mx-auto my-0 my-md-3">
            <div class="card-body d-flex flex-column align-items-center text-center py-4 px-3">
                <div class="mb-3">
                    ${iconHTML}
                    <br>
                    <p class="fw-bold fs-4">${cardTitle}</p>
                </div>
                <div class="card-text">${contenido}</div>
            </div>
        </div>
    `;

    setTimeout(() => {
        const el = document.getElementById(cardId);
        if (el) {
            el.classList.remove("show");
            el.addEventListener("transitionend", () => el.remove(), { once: true });
        }
    }, 6000);

    return html;
}


// ============================================================================
// UTILIDADES DE RELOJ (FECHA Y HORA)
// ============================================================================

/**
 * Actualiza elementos HTML con la fecha y la hora actual.
 * @param {string} [fechaId] - ID del elemento donde mostrar la fecha.
 * @param {string} [horaId] - ID del elemento donde mostrar la hora.
 */
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

/**
 * Inicia un reloj en vivo actualizando fecha y hora en intervalos de 1s.
 * @param {string} [fechaId] - ID del elemento donde mostrar la fecha.
 * @param {string} [horaId] - ID del elemento donde mostrar la hora.
 */
function iniciarReloj(fechaId, horaId) {
    function tick() {
        actualizarReloj(fechaId, horaId);
        const now = new Date();
        const delay = 1000 - now.getMilliseconds();
        setTimeout(tick, delay);
    }
    tick();
}


// ============================================================================
// BOTONES (Loading Spinner y Restaurar)
// ============================================================================

/**
 * Deshabilita un botón y muestra un spinner de carga.
 * @param {HTMLButtonElement} button - Botón a modificar.
 * @param {string} [loadingText="Procesando..."] - Texto a mostrar junto al spinner.
 */
function disableButtonWithSpinner(button, loadingText = "Procesando...") {
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        ${loadingText}
    `;
}

/**
 * Restaura el botón a su estado original.
 * @param {HTMLButtonElement} button - Botón a restaurar.
 * @param {string} originalText - Texto original del botón.
 */
function enableButton(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}


// ============================================================================
// VALIDACIÓN DE FORMULARIOS
// ============================================================================

/**
 * Marca inputs como inválidos y muestra un mensaje de error.
 * @param {HTMLInputElement|HTMLInputElement[]} inputs - Uno o varios inputs.
 * @param {string|null} [message=null] - Mensaje de error a mostrar.
 */
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

/**
 * Elimina la clase de error de los inputs.
 * @param {HTMLInputElement|HTMLInputElement[]} inputs - Uno o varios inputs.
 */
function clearInvalid(inputs) {
    if (!Array.isArray(inputs)) inputs = [inputs];
    inputs.forEach(input => input?.classList.remove("is-invalid"));
}

/**
 * Escucha eventos de input para limpiar el estado inválido al escribir.
 * @param {HTMLInputElement|HTMLInputElement[]} inputs - Uno o varios inputs.
 */
function attachClearOnInput(inputs) {
    if (!Array.isArray(inputs)) inputs = [inputs];
    inputs.forEach(input => {
        if (!input) return;
        input.addEventListener("input", () => input.classList.remove("is-invalid"));
    });
}


// ============================================================================
// TABLAS (DataTables con configuración por defecto)
// ============================================================================

/**
 * Inicializa un DataTable con configuración estándar (exportación, responsive, tooltips).
 * @param {string} selector - Selector del elemento <table>.
 * @param {Object} [options={}] - Configuración personalizada.
 * @param {boolean} [includeLastColumnInExport=false] - Si es true, no se excluirá la última columna en exportaciones.
 * @returns {DataTable} - Instancia de DataTable.
 */
function initDataTable(selector, options = {}, includeLastColumnInExport = false) {
    const defaultConfig = {
        processing: true,
        serverSide: false,
        responsive: true,
        pageLength: 15,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/es-ES.json"
        },
        dom: '<"d-flex flex-column flex-md-row justify-content-between align-items-center mb-2"Bf>rt<"d-flex flex-column flex-md-row justify-content-between align-items-center mb-2"ip>',
        buttons: [
            {
                text: '<i class="bi bi-arrow-clockwise me-1 text-primary"></i><span class="text-dark">Recargar</span>',
                className: 'btn btn-sm bg-white border-0',
                action: function (e, dt, node, config) {
                    dt.ajax.reload(null, false);
                }
            },
            {
                extend: 'excelHtml5',
                text: '<i class="bi bi-file-earmark-excel-fill me-1 text-success"></i><span class="text-dark">Excel</span>',
                className: 'btn btn-sm bg-white border-0',
                titleAttr: 'Exportar a Excel',
                exportOptions: {
                    columns: includeLastColumnInExport
                        ? ':visible'
                        : ':visible:not(:last-child)'
                }
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="bi bi-file-earmark-pdf-fill me-1 text-danger"></i><span class="text-dark">PDF</span>',
                className: 'btn btn-sm bg-white border-0',
                titleAttr: 'Exportar a PDF',
                orientation: 'landscape',
                pageSize: 'A4',
                exportOptions: {
                    columns: includeLastColumnInExport
                        ? ':visible'
                        : ':visible:not(:last-child)'
                }
            },
            {
                extend: 'print',
                text: '<i class="bi bi-printer-fill me-1 text-secondary"></i><span class="text-dark">Imprimir</span>',
                className: 'btn btn-sm bg-white border-0',
                titleAttr: 'Imprimir',
                exportOptions: {
                    columns: includeLastColumnInExport
                        ? ':visible'
                        : ':visible:not(:last-child)'
                }
            }
        ],
        columns: []
    };

    const config = $.extend(true, {}, defaultConfig, options);
    const dt = $(selector).DataTable(config);

    // Envuelve la tabla con la clase 'table-responsive'
    $(selector).wrap('<div class="table-responsive"></div>');

    // ⚡ Inicializar tooltips cada vez que se dibujen filas
    dt.on("draw", function () {
        initTooltips(document);
    });

    return dt;
}


// ============================================================================
// MODALES Y FORMULARIOS
// ============================================================================

/**
 * Resetea un formulario dentro de un modal y limpia errores de validación.
 * @param {string} modalId - ID del modal.
 * @param {string} formId - ID del formulario.
 * @param {string[]} [inputIds=[]] - IDs de inputs a limpiar.
 */
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

// ============================================================================
// FORMATOS DE FECHAS Y HORAS (Django REST Framework)
// ============================================================================

/** * Formatea horas en formato 12 horas con a. m./p. m.
 * @param {string} timeStr - Hora en formato "HH:MM:SS".
 * @returns {string} - Hora formateada en "hh:mm a. m." o "hh:mm p. m.".
 */
function formatTime12Hour(timeStr) {
    const [hours, minutes] = timeStr.split(":");
    const period = hours >= 12 ? "p. m." : "a. m.";
    const formattedHours = hours % 12 || 12;
    return `${formattedHours < 10 ? '0' : ''}${formattedHours}:${minutes} ${period}`;
}

/**
 * Formatea fechas en formato "DD/MM/YYYY".
 * @param {string} dateStr - Fecha en formato "YYYY-MM-DD".
 * @returns {string} - Fecha formateada en "DD/MM/YYYY".
 */
function formatDateDDMMYYYY(dateStr) {
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`;
}


/** * Obtiene la fecha actual en formato "DD/MM/YYYY".
 * @returns {string} - Fecha de hoy en formato "DD/MM/YYYY".
 */
function fechaHoyFormato() {
    const hoy = new Date();
    const dd = String(hoy.getDate()).padStart(2, '0');
    const mm = String(hoy.getMonth() + 1).padStart(2, '0');
    const yyyy = hoy.getFullYear();
    return `${dd}/${mm}/${yyyy}`;
}

// ============================================================================
// SELECT MULTIPLE CON BÚSQUEDA
// ============================================================================

/**
 * Agrega un campo de búsqueda a un <select multiple>
 * @param {string} selectId - ID del <select>
 * @param {string} placeholder - Texto opcional para el campo de búsqueda
 */
function addSearchToMultipleSelect(selectId, placeholder = "Buscar...") {
    const select = document.getElementById(selectId);
    if (!select) return;

    // Evitar duplicar el buscador
    if (select.parentElement.querySelector(".select-search-input")) return;

    // Crear contenedor general
    const wrapper = document.createElement("div");
    wrapper.classList.add("mb-2");

    const inputGroup = document.createElement("div");
    inputGroup.classList.add("input-group", "input-group-sm", "mb-2");

    // Icono de búsqueda
    const spanIcon = document.createElement("span");
    spanIcon.classList.add("input-group-text");
    spanIcon.innerHTML = '<i class="bi bi-search"></i>';

    // Campo de texto
    const input = document.createElement("input");
    input.type = "text";
    input.classList.add("form-control", "select-search-input");
    input.placeholder = placeholder;

    // Botón de limpiar
    const clearBtn = document.createElement("button");
    clearBtn.classList.add("btn", "btn-outline-secondary");
    clearBtn.type = "button";
    clearBtn.innerHTML = '<i class="bi bi-x-lg"></i>';

    // Armar estructura del input-group
    inputGroup.appendChild(spanIcon);
    inputGroup.appendChild(input);
    inputGroup.appendChild(clearBtn);

    // Insertar el input-group antes del select
    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(inputGroup);
    wrapper.appendChild(select);

    // Guardar las opciones originales (para restaurar)
    const originalOptions = Array.from(select.options);

    // Filtrar opciones al escribir
    input.addEventListener("input", () => {
        const term = input.value.trim().toLowerCase();
        select.innerHTML = "";

        const filtered = originalOptions.filter(opt =>
            opt.textContent.toLowerCase().includes(term)
        );

        filtered.forEach(opt => select.appendChild(opt));
    });

    // Limpiar búsqueda
    clearBtn.addEventListener("click", () => {
        input.value = "";
        select.innerHTML = "";
        originalOptions.forEach(opt => select.appendChild(opt));
        input.focus();
    });
}

// ============================================================================
// SELECTS (Llenar opciones desde un array de objetos)
// ============================================================================

/**
 * Llena un <select> con opciones desde un array de objetos.
 * @param {string} selectId - ID del <select>.
 * @param {Object[]} data - Array de objetos con datos.
 * @param {string} placeholder - Texto del placeholder.
 * @param {string} labelKey - Nombre de la propiedad del objeto a mostrar como texto.
 * @param {Function} [formatter] - Función opcional que recibe (item) y retorna el texto a mostrar.
 */
function fillSelect(selectId, data, placeholder, labelKey, formatter) {
    const select = document.getElementById(selectId);
    select.innerHTML = `<option value="">${placeholder}</option>`;
    data.forEach(item => {
        const text = formatter
            ? formatter(item)
            : (item[labelKey] || "—").toUpperCase();
        select.innerHTML += `<option value="${item.id}">${text}</option>`;
    });
}