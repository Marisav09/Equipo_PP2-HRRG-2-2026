const shell = document.querySelector("[data-role]");
const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector("#chat-messages");
const statusStrip = document.querySelector("#status-strip");
const abortButton = document.querySelector("#abort-button");
const voiceButton = document.querySelector("#voice-button");
const ingestButton = document.querySelector("#ingest-button");
const manualsButton = document.querySelector("#manuals-button");
const manualsDialog = document.querySelector("#manuals-dialog");
const manualsCloseButton = document.querySelector("#manuals-close-button");
const manualsSummary = document.querySelector("#manuals-summary");
const manualsList = document.querySelector("#manuals-list");
const newChatButton = document.querySelector("#new-chat-button");
const equipmentDialogButton = document.querySelector("#equipment-dialog-button");
const logoutButton = document.querySelector("#logout-button");
const qrButton = document.querySelector("#qr-button");
const qrDialog = document.querySelector("#qr-dialog");
const qrTitle = document.querySelector("#qr-title");
const qrImage = document.querySelector("#qr-image");
const qrUrl = document.querySelector("#qr-url");
const qrOpenLink = document.querySelector("#qr-open-link");
const qrDownloadLink = document.querySelector("#qr-download-link");
const qrPrintLink = document.querySelector("#qr-print-link");
const qrCopyButton = document.querySelector("#qr-copy-button");
const activeEquipmentTitle = document.querySelector("#active-equipment");
const equipmentSelect = document.querySelector("#equipment-select");
const historyList = document.querySelector("#history-list");
const speechToggleButton = document.querySelector("#speech-toggle-button");
const monitoringButton = document.querySelector("#monitoring-button");
const monitoringDialog = document.querySelector("#monitoring-dialog");
const monitoringCloseButton = document.querySelector("#monitoring-close-button");
const monitoringSearchInput = document.querySelector("#monitoring-search-input");
const monitoringUserFilter = document.querySelector("#monitoring-user-filter");
const monitoringEquipmentFilter = document.querySelector("#monitoring-equipment-filter");
const monitoringDateFromFilter = document.querySelector("#monitoring-date-from-filter");
const monitoringDateToFilter = document.querySelector("#monitoring-date-to-filter");
const myConsultationsButton = document.querySelector("#my-consultations-button");
const myConsultationsDialog = document.querySelector("#my-consultations-dialog");
const myConsultationsCloseButton = document.querySelector("#my-consultations-close-button");
const myConsultationsList = document.querySelector("#my-consultations-list");
const technicianRecentList = document.querySelector("#technician-recent-list");
const operatorHistoryList = document.querySelector("#operator-history-list");

let activeRequestId = null;
let selectedEquipmentId = shell?.dataset.equipmentId || "";
let selectedEquipmentName = shell?.dataset.equipmentName || "";
let lastQuery = "";
let activeQuery = "";
let recognition = null;
let activeLoadingMessage = null;
let activeRequestCancelled = false;
let speechMuted = localStorage.getItem("hrrgSpeechMuted") === "1";
let conversationMessages = [];
let activeChatId = sessionStorage.getItem(`hrrgActiveChatId:${shell?.dataset.role || "default"}`) || crypto.randomUUID();

function setActiveChatId(chatId = crypto.randomUUID()) {
    activeChatId = chatId;
    sessionStorage.setItem(`hrrgActiveChatId:${shell?.dataset.role || "default"}`, activeChatId);
}

setActiveChatId(activeChatId);

function modeLabel(mode) {
    const labels = {
        llm: "MODO: ASISTENTE INTELIGENTE (AI)",
        fallback_chromadb: "MODO: DIRECTO A FUENTE",
        fallback_timeout: "MODO: DIRECTO A FUENTE POR TIEMPO AGOTADO",
        fallback_llm_error: "MODO: DIRECTO A FUENTE POR FALLA DEL MODELO LOCAL",
        guardrail: "MODO: GUARDRAIL DE SEGURIDAD",
        cancelled: "MODO: CONSULTA DETENIDA",
        sin_documentos: "MODO: SIN DOCUMENTOS INDEXADOS",
        sin_informacion: "MODO: SIN INFORMACIÓN DOCUMENTAL",
        contexto_insuficiente_operador: "MODO: SEGURIDAD CLÍNICA",
    };
    return labels[mode] || `MODO: ${String(mode || "DESCONOCIDO").toUpperCase()}`;
}

function setStatus(message) {
    if (!statusStrip) return;
    const label = statusStrip.querySelector("span");
    if (label) {
        label.textContent = message;
    } else {
        statusStrip.textContent = message;
    }
}

function visibleSourceName(source = {}) {
    return source.display_source || source.original_pdf || source.source_file || "Fuente documental";
}

function readableSourceName(source = {}) {
    const rawName = visibleSourceName(source);
    return String(rawName)
        .replace(/\.[a-z0-9]+$/i, "")
        .replace(/[_-]+/g, " ")
        .replace(/\s+/g, " ")
        .trim();
}

function visibleSourcePage(source = {}) {
    return source.pdf_page || source.page || "sin página";
}

function visibleSourceLabel(source = {}) {
    return `Fuente: ${visibleSourceName(source)}, pag. ${visibleSourcePage(source)}`;
}

function inlineSourceLabel(source = {}, index = 0) {
    return `Fuente ${index + 1}: ${readableSourceName(source)}, pag. ${visibleSourcePage(source)}`;
}

function createCitationSup(index = 0) {
    const sup = document.createElement("sup");
    sup.className = "notebook-citation-sup";
    sup.textContent = String(index + 1);
    return sup;
}

function stripMarkdownMarkers(text) {
    return String(text || "")
        .replace(/\*\*([^*]+)\*\*/g, "$1")
        .replace(/\*([^*\n]+)\*/g, "$1")
        .replace(/`([^`]+)`/g, "$1")
        .split("\n")
        .map((line) => line.replace(/^\s*[*-]\s+/g, ""))
        .join("\n")
        .replace(/[*_]{2,}/g, "")
        .replace(/\s+\*/g, " ")
        .replace(/\*\s+/g, " ")
        .trim();
}

function speechSafeText(text) {
    return stripMarkdownMarkers(text)
        .replace(/^#{1,6}\s+/gm, "")
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
        .replace(/\s{2,}/g, " ")
        .trim();
}

function speechIconSvg(isMuted = false) {
    const slash = isMuted ? '<path d="M4 4l16 16"/>' : "";
    const waves = isMuted
        ? '<path d="M16 9.5 19 12l-3 2.5"/>'
        : '<path d="M16 8.5a4.5 4.5 0 0 1 0 7"/><path d="M19 6a8 8 0 0 1 0 12"/>';
    return `
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 9v6h4l5 4V5L8 9H4z"/>
            ${waves}
            ${slash}
        </svg>
        <span>${isMuted ? "Audio silenciado" : "Audio activo"}</span>
    `;
}

function updateSpeechControls() {
    const title = speechMuted ? "Activar lectura en voz alta" : "Silenciar lectura en voz alta";
    document.querySelectorAll(".speech-action, #speech-toggle-button").forEach((button) => {
        button.innerHTML = speechIconSvg(speechMuted);
        button.dataset.muted = speechMuted ? "true" : "false";
        button.title = title;
        button.setAttribute("aria-label", title);
    });
}

function setSpeechMuted(isMuted) {
    speechMuted = Boolean(isMuted);
    localStorage.setItem("hrrgSpeechMuted", speechMuted ? "1" : "0");
    if (speechMuted) {
        window.hrrgSpeech?.stop?.();
    }
    updateSpeechControls();
}

function createSourceList(sources = []) {
    if (!sources.length) return null;

    const wrapper = document.createElement("div");
    wrapper.className = "source-list notebook-source-list";

    const title = document.createElement("div");
    title.className = "notebook-source-title";
    title.textContent = "Fuentes:";
    wrapper.appendChild(title);

    sources.forEach((source, index) => {
        const link = document.createElement("a");
        link.className = "notebook-source-link";
        link.href = source.url || "#";
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.title = `${visibleSourceName(source)}, página ${visibleSourcePage(source)}`;
        link.appendChild(createCitationSup(index));
        link.appendChild(document.createTextNode(` Fuente: ${readableSourceName(source)}, pag. ${visibleSourcePage(source)}`));

        wrapper.appendChild(link);
    });

    return wrapper;
}

function createImageList(sources = []) {
    const images = sources.flatMap((source) => source.images || []);
    if (!images.length) return null;

    const wrapper = document.createElement("div");
    wrapper.className = "image-list";
    images.slice(0, 6).forEach((image) => {
        const link = document.createElement("a");
        link.className = "image-thumb";
        link.href = image.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.title = image.label || `Pagina ${image.page}`;

        const preview = document.createElement("img");
        preview.src = image.url;
        preview.alt = image.label || `Imagen página ${image.page}`;

        const label = document.createElement("span");
        label.textContent = `Pag. ${image.page}`;

        link.appendChild(preview);
        link.appendChild(label);
        wrapper.appendChild(link);
    });
    return wrapper;
}

function isFallbackMode(mode) {
    return String(mode || "").startsWith("fallback");
}

function stripSourceLines(content) {
    return String(content || "")
        .split("\n")
        .filter((line) => {
            const normalized = line.trim().toLowerCase();
            return !normalized.startsWith("fuente:") && !normalized.startsWith("fuentes:");
        })
        .join("\n")
        .trim();
}

function appendTextWithBreaks(container, text) {
    stripMarkdownMarkers(text).split("\n").forEach((line, index) => {
        if (index > 0) container.appendChild(document.createElement("br"));
        container.appendChild(document.createTextNode(line));
    });
}

function appendCitedTextWithBreaks(container, text, sources = []) {
    const cleanText = stripMarkdownMarkers(text);
    if (!sources.length) {
        appendTextWithBreaks(container, cleanText);
        return;
    }

    let citationIndex = 0;
    cleanText.split("\n").forEach((line, lineIndex) => {
        if (lineIndex > 0) container.appendChild(document.createElement("br"));

        const segments = line.match(/[^.!?]+[.!?]?|\s+/g) || [line];
        segments.forEach((segment) => {
            const trimmed = segment.trim();
            container.appendChild(document.createTextNode(segment));
            if (!trimmed || !/[A-Za-zÁÉÍÓÚáéíóúÑñ0-9]/.test(trimmed)) return;

            const sourceIndex = Math.min(citationIndex, sources.length - 1);
            container.appendChild(createCitationSup(sourceIndex));
            citationIndex += 1;
        });
    });
}

function renderFallbackBubble(bubble, content, sources = []) {
    let sourceIndex = 0;
    const lines = String(content || "").split("\n");

    lines.forEach((line, index) => {
        if (index > 0) bubble.appendChild(document.createElement("br"));

        const normalized = line.trim().toLowerCase();
        if (normalized.startsWith("fuente:")) {
            const source = sources[sourceIndex] || sources[sources.length - 1];
            sourceIndex += 1;

            if (source?.url) {
                const link = document.createElement("a");
                link.className = "fallback-source-link";
                link.href = source.url;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.textContent = visibleSourceLabel(source);
                bubble.appendChild(link);
                return;
            }
        }

        if (normalized.startsWith("extracto ")) {
            const label = document.createElement("strong");
            label.className = "extract-title";
            label.textContent = stripMarkdownMarkers(line);
            bubble.appendChild(label);
            return;
        }

        bubble.appendChild(document.createTextNode(stripMarkdownMarkers(line)));
    });
}

function createRegenerateAction() {
    if (!lastQuery) return null;

    const actions = document.createElement("div");
    actions.className = "message-actions";

    const button = document.createElement("button");
    button.className = "inline-action";
    button.type = "button";
    button.textContent = "Regenerar respuesta";
    button.addEventListener("click", async () => {
        await ask(lastQuery, {repeatUserMessage: false});
    });

    actions.appendChild(button);
    return actions;
}

function createAuditRow({label, count}) {
    const row = document.createElement("div");
    row.className = "audit-metric-row";

    const name = document.createElement("span");
    name.textContent = label;

    const value = document.createElement("strong");
    value.textContent = count;

    row.appendChild(name);
    row.appendChild(value);
    return row;
}

function monitoringLabel(label) {
    const labels = {
        "Calibracion": "Calibración",
        "Energia": "Energía",
        "Consulta tecnica": "Consulta técnica",
        "Pantalla tactil": "Pantalla táctil",
        "Bateria / carga": "Batería / carga",
        "Presion": "Presión",
        "Técnicos": "Técnicos",
    };
    return labels[String(label || "")] || label;
}

function createChartRow(item, maxCount, index = 0) {
    const row = document.createElement("div");
    row.className = "monitoring-chart-row";

    const top = document.createElement("div");
    top.className = "monitoring-chart-topline";

    const label = document.createElement("span");
    label.textContent = monitoringLabel(item.label);

    const value = document.createElement("strong");
    value.textContent = item.count;

    top.appendChild(label);
    top.appendChild(value);

    const track = document.createElement("div");
    track.className = "monitoring-chart-track";

    const bar = document.createElement("div");
    bar.className = `monitoring-chart-bar chart-color-${(index % 4) + 1}`;
    const percent = maxCount ? Math.max(6, Math.round((Number(item.count || 0) / maxCount) * 100)) : 0;
    bar.style.width = `${percent}%`;
    bar.setAttribute("aria-label", `${monitoringLabel(item.label)}: ${item.count}`);

    track.appendChild(bar);
    row.appendChild(top);
    row.appendChild(track);
    return row;
}

function renderAuditList(elementId, items = [], emptyLabel = "Sin datos registrados") {
    const container = document.querySelector(`#${elementId}`);
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = emptyLabel;
        container.appendChild(empty);
        return;
    }

    const maxCount = Math.max(...items.map((item) => Number(item.count || 0)), 0);
    items.slice(0, 8).forEach((item, index) => {
        container.appendChild(createChartRow(item, maxCount, index));
    });
}

function renderIncidentPrompt(consultationId) {
    if (!consultationId || !chatMessages) return;

    const prompt = document.createElement("article");
    prompt.className = "incident-prompt";

    const text = document.createElement("span");
    text.textContent = "Esta consulta parece una falla. ¿Desea registrarla como incidente?";

    const actions = document.createElement("div");
    actions.className = "incident-actions";

    const yesButton = document.createElement("button");
    yesButton.type = "button";
    yesButton.textContent = "SI";
    yesButton.addEventListener("click", async () => {
        try {
            await window.hrrgApi.postJson(`/api/monitoring/consultations/${consultationId}/incident`, {});
            prompt.remove();
            setStatus("Incidente registrado para trazabilidad de Ingeniería Clínica.");
        } catch (error) {
            setStatus(error.message || "No se pudo registrar el incidente.");
        }
    });

    const noButton = document.createElement("button");
    noButton.type = "button";
    noButton.textContent = "NO";
    noButton.addEventListener("click", () => {
        prompt.remove();
        setStatus("Consulta guardada sin incidente formal.");
    });

    actions.appendChild(yesButton);
    actions.appendChild(noButton);
    prompt.appendChild(text);
    prompt.appendChild(actions);
    chatMessages.appendChild(prompt);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createSpeechAction(content) {
    const button = document.createElement("button");
    button.className = "inline-action speech-action";
    button.type = "button";
    button.innerHTML = speechIconSvg(speechMuted);
    button.title = speechMuted ? "Activar lectura en voz alta" : "Silenciar lectura en voz alta";
    button.setAttribute("aria-label", button.title);
    button.addEventListener("click", () => {
        const shouldMute = !speechMuted;
        setSpeechMuted(shouldMute);
        if (!shouldMute) window.hrrgSpeech?.speak?.(speechSafeText(content));
    });
    updateSpeechControls();
    return button;
    button.textContent = speechMuted ? "🔇" : "🔊";
    button.title = speechMuted ? "Activar lectura en voz alta" : "Leer en voz alta";
    button.setAttribute("aria-label", button.title);

    button.addEventListener("click", () => {
        speechMuted = !speechMuted;
        localStorage.setItem("hrrgSpeechMuted", speechMuted ? "1" : "0");
        button.textContent = speechMuted ? "🔇" : "🔊";
        button.title = speechMuted ? "Activar lectura en voz alta" : "Leer en voz alta";
        button.setAttribute("aria-label", button.title);

        if (speechMuted) {
            window.hrrgSpeech?.stop?.();
        } else {
            window.hrrgSpeech?.speak?.(content);
        }
    });

    return button;
}

function addMessage(role, content, options = {}) {
    const mode = options.mode || "";
    const fallbackMode = isFallbackMode(mode);

    const message = document.createElement("article");
    message.className = `message ${role}`;

    if (role === "assistant") {
        const avatar = document.createElement("div");
        avatar.className = "avatar ai-avatar";
        avatar.setAttribute("aria-hidden", "true");
        message.appendChild(avatar);
    }

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    const sourceCleanContent = role === "assistant" && shell.dataset.role === "tecnico" && !fallbackMode
        ? stripSourceLines(content)
        : content;
    const visibleContent = role === "assistant" ? stripMarkdownMarkers(sourceCleanContent) : sourceCleanContent;

    if (role === "assistant" && fallbackMode) {
        renderFallbackBubble(bubble, visibleContent, options.sources || []);
    } else if (role === "assistant" && options.sources?.length) {
        appendCitedTextWithBreaks(bubble, visibleContent, options.sources);
    } else {
        appendTextWithBreaks(bubble, visibleContent);
    }

    contentWrapper.appendChild(bubble);

    const images = createImageList(options.sources);
    if (images) contentWrapper.appendChild(images);

    const sources = !fallbackMode ? createSourceList(options.sources) : null;
    if (sources) contentWrapper.appendChild(sources);

    if (role === "assistant" && options.regenerable) {
        const actions = document.createElement("div");
        actions.className = "message-actions";
        actions.appendChild(createSpeechAction(visibleContent));

        const regenerate = createRegenerateAction();
        if (regenerate?.firstChild) actions.appendChild(regenerate.firstChild);

        contentWrapper.appendChild(actions);
    }

    message.appendChild(contentWrapper);
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    if (options.track !== false) {
        conversationMessages.push({
            role,
            content,
            options: {
                mode: options.mode || "",
                sources: options.sources || [],
            },
        });
    }

    return message;
}

function addLoadingMessage() {
    const message = document.createElement("article");
    message.className = "message assistant";

    const avatar = document.createElement("div");
    avatar.className = "avatar ai-avatar";
    avatar.setAttribute("aria-hidden", "true");
    message.appendChild(avatar);

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble loading-bubble";
    bubble.setAttribute("aria-label", "El asistente esta procesando la respuesta");

    for (let i = 0; i < 3; i += 1) {
        const dot = document.createElement("span");
        dot.className = "loading-dot";
        bubble.appendChild(dot);
    }

    if (shell.dataset.role === "tecnico") {
        const fallbackAction = document.createElement("button");
        fallbackAction.className = "direct-source-button loading-source-button";
        fallbackAction.type = "button";
        fallbackAction.textContent = "Directo a fuente";
        fallbackAction.addEventListener("click", async () => {
            const query = activeQuery || lastQuery;
            if (!query) return;

            if (activeRequestId) {
                activeRequestCancelled = true;
                await window.hrrgApi.postJson("/api/chat/cancel", {request_id: activeRequestId});
            }

            removeLoadingMessage();
            await ask(query, {forceFallback: true, repeatUserMessage: false});
        });
        bubble.appendChild(fallbackAction);
    }

    contentWrapper.appendChild(bubble);
    message.appendChild(contentWrapper);
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}

function removeLoadingMessage() {
    if (activeLoadingMessage) {
        activeLoadingMessage.remove();
        activeLoadingMessage = null;
    }
}

function statusLabel(status) {
    const labels = {
        indexed: "Indexado",
        unchanged: "Sin cambios",
        skipped: "Omitido",
        error: "Error",
    };
    return labels[status] || status;
}

function renderManualsAudit(documents = []) {
    if (!manualsSummary || !manualsList) return;

    const indexed = documents.filter((item) => ["indexed", "unchanged"].includes(item.status)).length;
    const skipped = documents.filter((item) => item.status === "skipped").length;
    const errors = documents.filter((item) => item.status === "error").length;
    const chunks = documents.reduce((total, item) => total + Number(item.chunk_count || 0), 0);

    manualsSummary.innerHTML = "";
    [
        `${documents.length} documentos`,
        `${indexed} activos`,
        `${skipped} omitidos`,
        `${errors} errores`,
        `${chunks} chunks`,
    ].forEach((label) => {
        const stat = document.createElement("span");
        stat.className = "manual-stat";
        stat.textContent = label;
        manualsSummary.appendChild(stat);
    });

    manualsList.innerHTML = "";
    if (!documents.length) {
        const empty = document.createElement("p");
        empty.className = "manual-empty";
        empty.textContent = "Todavía no hay documentos auditados. Ejecute la ingesta de manuales.";
        manualsList.appendChild(empty);
        return;
    }

    documents.forEach((documentInfo) => {
        const row = document.createElement("article");
        row.className = "manual-row";

        const pdfLink = document.createElement("a");
        pdfLink.className = "manual-pdf-button";
        pdfLink.href = documentInfo.source_url || `/manuals/${encodeURIComponent(documentInfo.original_pdf || documentInfo.display_source || documentInfo.source_file || "")}`;
        pdfLink.target = "_blank";
        pdfLink.rel = "noopener noreferrer";
        pdfLink.title = "Abrir PDF";
        pdfLink.setAttribute("aria-label", "Abrir PDF del manual");
        pdfLink.textContent = "PDF";

        const title = document.createElement("div");
        title.className = "manual-title";

        const source = document.createElement("strong");
        source.textContent = documentInfo.display_source || documentInfo.original_pdf || documentInfo.source_file;

        const date = document.createElement("span");
        date.textContent = documentInfo.created_at || "Fecha de ingesta no registrada";

        title.appendChild(source);
        title.appendChild(date);

        const metrics = document.createElement("span");
        metrics.className = "manual-metrics";
        metrics.textContent = `${documentInfo.page_count || 0} páginas - ${documentInfo.chunk_count || 0} chunks - ${documentInfo.image_count || 0} imágenes`;

        const status = document.createElement("span");
        status.className = `manual-status ${documentInfo.status}`;
        status.title = documentInfo.message || "";
        status.textContent = statusLabel(documentInfo.status);

        const statusGroup = document.createElement("div");
        statusGroup.className = "manual-status-group";
        statusGroup.appendChild(status);
        statusGroup.appendChild(metrics);

        row.appendChild(pdfLink);
        row.appendChild(title);
        row.appendChild(statusGroup);
        manualsList.appendChild(row);
    });
}

async function openManualsAudit() {
    if (!manualsDialog) return;

    setStatus("Cargando manifiesto de ingesta...");
    try {
        const data = await window.hrrgApi.getJson("/api/ingest/audit");
        renderManualsAudit(data.documents || []);
        manualsDialog.showModal();
        setStatus("Manifiesto documental cargado.");
    } catch (error) {
        addMessage("assistant", error.message || "No se pudo cargar el manifiesto documental.");
        setStatus("No se pudo cargar el manifiesto documental.");
    }
}

function setBusy(isBusy) {
    if (messageInput) messageInput.disabled = isBusy;
    if (abortButton) {
        abortButton.disabled = !isBusy;
        abortButton.classList.toggle("active", isBusy);
    }
}

async function startNewChat() {
    if (!selectedEquipmentId) {
        setStatus("Seleccione un equipo para iniciar un chat nuevo.");
        document.querySelector("#equipment-dialog")?.showModal();
        return;
    }

    await window.hrrgApi.postJson("/api/chat/memory/clear", {});
    chatMessages.innerHTML = "";
    conversationMessages = [];
    lastQuery = "";
    activeQuery = "";
    removeLoadingMessage();
    setActiveChatId();

    addMessage("assistant", `Chat nuevo iniciado para ${selectedEquipmentName}.`);
    setStatus(`Chat nuevo para ${selectedEquipmentName}. Memoria de sesión limpiada.`);
}

async function selectEquipment(equipmentId, equipmentName) {
    if (!equipmentId || !equipmentName) return;

    selectedEquipmentId = equipmentId;
    selectedEquipmentName = equipmentName;

    if (activeEquipmentTitle) {
        activeEquipmentTitle.textContent = selectedEquipmentName;
    }

    if (equipmentSelect && equipmentSelect.value !== selectedEquipmentId) {
        equipmentSelect.value = selectedEquipmentId;
    }

    await window.hrrgApi.postJson("/api/chat/memory/clear", {});
    chatMessages.innerHTML = "";
    conversationMessages = [];
    lastQuery = "";
    activeQuery = "";
    setActiveChatId();

    addMessage("assistant", `Nuevo chat iniciado para ${selectedEquipmentName}.`);
    document.querySelector("#equipment-dialog")?.close();
    setStatus(`Equipo seleccionado: ${selectedEquipmentName}. Memoria de sesión limpiada.`);
}

function loadHistory() {
    try {
        const entries = JSON.parse(localStorage.getItem("hrrgChatHistory") || "[]");
        return Array.isArray(entries) ? entries : [];
    } catch {
        return [];
    }
}

function saveHistoryEntry(equipmentName) {
    if (!equipmentName) return;

    const role = shell?.dataset.role || "tecnico";
    const previousEntries = loadHistory().filter(
        (item) => !(item.equipmentName === equipmentName && (item.role || role) === role),
    );

    const currentEntry = {
        role,
        equipmentId: selectedEquipmentId,
        equipmentName,
        createdAt: new Date().toLocaleString("es-AR", {dateStyle: "short", timeStyle: "short"}),
        messages: conversationMessages.slice(-30),
    };

    const sameRoleEntries = previousEntries.filter((entry) => (entry.role || role) === role).slice(0, 4);
    const otherRoleEntries = previousEntries.filter((entry) => (entry.role || role) !== role);

    localStorage.setItem("hrrgChatHistory", JSON.stringify([currentEntry, ...sameRoleEntries, ...otherRoleEntries]));
    renderHistory();
}

function restoreHistoryEntry(entry) {
    const messages = Array.isArray(entry.messages) ? entry.messages : [];
    if (!messages.length) {
        setStatus("Este historial no tiene mensajes guardados. Las nuevas conversaciones si se podran abrir desde aqui.");
        return;
    }

    selectedEquipmentId = entry.equipmentId || selectedEquipmentId;
    selectedEquipmentName = entry.equipmentName || selectedEquipmentName;

    if (activeEquipmentTitle && selectedEquipmentName) {
        activeEquipmentTitle.textContent = selectedEquipmentName;
    }

    if (equipmentSelect && selectedEquipmentId && equipmentSelect.value !== selectedEquipmentId) {
        equipmentSelect.value = selectedEquipmentId;
    }

    removeLoadingMessage();
    activeRequestId = null;
    activeQuery = "";
    activeRequestCancelled = false;
    setBusy(false);
    chatMessages.innerHTML = "";
    conversationMessages = [];

    messages.forEach((message) => {
        addMessage(message.role, message.content, {
            ...(message.options || {}),
            regenerable: false,
            track: false,
        });
    });

    conversationMessages = messages.map((message) => ({
        role: message.role,
        content: message.content,
        options: {
            mode: message.options?.mode || "",
            sources: message.options?.sources || [],
        },
    }));

    const lastUserMessage = [...conversationMessages].reverse().find((message) => message.role === "user");
    lastQuery = lastUserMessage?.content || "";

    setStatus(`Historial cargado: ${selectedEquipmentName}.`);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderHistory() {
    if (!historyList) return;

    historyList.innerHTML = "";
    const role = shell?.dataset.role || "tecnico";
    const entries = loadHistory()
        .filter((entry) => !entry.role || entry.role === role)
        .slice(0, 5);

    if (!entries.length) {
        const empty = document.createElement("p");
        empty.className = "history-empty";
        empty.textContent = "Sin chats recientes";
        historyList.appendChild(empty);
        return;
    }

    entries.forEach((entry) => {
        const card = document.createElement("button");
        card.className = "history-card";
        card.type = "button";

        const name = document.createElement("strong");
        name.textContent = entry.equipmentName;

        const date = document.createElement("span");
        date.textContent = entry.createdAt;

        card.appendChild(name);
        card.appendChild(date);
        card.addEventListener("click", () => restoreHistoryEntry(entry));
        historyList.appendChild(card);
    });
}

async function ask(query, options = {}) {
    const requestId = crypto.randomUUID();
    activeRequestId = requestId;
    activeRequestCancelled = false;
    activeQuery = query;

    setBusy(true);
    setStatus(options.forceFallback ? "Consultando directo a fuente..." : "Procesando consulta...");
    activeLoadingMessage = addLoadingMessage();

    try {
        const data = await window.hrrgApi.postJson("/api/chat/ask", {
            query,
            role: shell.dataset.role,
            equipment_id: selectedEquipmentId,
            equipment_name: selectedEquipmentName,
            force_fallback: Boolean(options.forceFallback),
            request_id: requestId,
            chat_id: activeChatId,
        });

        if (activeRequestCancelled || activeRequestId !== requestId) return;

        removeLoadingMessage();
        addMessage("assistant", data.answer, {
            sources: shell.dataset.role === "tecnico" ? data.sources : [],
            mode: data.mode,
            regenerable: true,
        });

        if (data.incident_candidate && data.consultation_id) {
            renderIncidentPrompt(data.consultation_id);
        }

        saveHistoryEntry(selectedEquipmentName);
        await loadTechnicianRecentChats();
        await loadOperatorChatHistory();
        setStatus(modeLabel(data.mode));

        if (!speechMuted) {
            window.hrrgSpeech.speak(speechSafeText(data.answer));
        }
    } catch (error) {
        if (activeRequestCancelled || activeRequestId !== requestId) return;

        removeLoadingMessage();
        addMessage("assistant", error.message || "No se pudo completar la consulta.");
        setStatus("Error en la consulta.");
    } finally {
        if (activeRequestId === requestId) {
            activeRequestId = null;
            activeQuery = "";
            setBusy(false);
        }
        messageInput.focus();
    }
}

function renderConsultationCards(container, items = [], options = {}) {
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = options.emptyClass || "audit-empty";
        empty.textContent = options.emptyText || "Todavía no hay consultas registradas.";
        container.appendChild(empty);
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = options.cardClass || "personal-query-card";

        const title = document.createElement("strong");
        title.textContent = item.equipment_name;

        const date = document.createElement("span");
        date.textContent = `${item.date} ${item.time}`;

        const question = document.createElement("p");
        question.textContent = item.question;

        const meta = document.createElement("small");
        meta.textContent = item.es_incidente ? `${monitoringLabel(item.category)} - incidente registrado` : monitoringLabel(item.category);

        card.appendChild(title);
        card.appendChild(date);
        card.appendChild(question);
        card.appendChild(meta);
        container.appendChild(card);
    });
}

function renderMyConsultations(items = []) {
    renderConsultationCards(myConsultationsList, items, {
        cardClass: "personal-query-card",
        emptyClass: "audit-empty",
        emptyText: "Todavía no hay consultas registradas.",
    });
}

function renderPersonalChatHistory(container, items = [], options = {}) {
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = options.emptyClass || "operator-history-empty";
        empty.textContent = options.emptyText || "Sin chats recientes";
        container.appendChild(empty);
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("button");
        card.className = options.cardClass || "operator-history-card";
        card.type = "button";
        card.dataset.chatId = item.chat_id;
        if (item.chat_id === activeChatId) card.classList.add("active");

        const title = document.createElement("strong");
        title.textContent = item.equipment_name || "Equipo no registrado";

        const preview = document.createElement("span");
        preview.textContent = item.last_question || "Chat sin consultas";

        const meta = document.createElement("small");
        meta.textContent = `${item.last_at || ""} · ${item.message_count || 0} consulta${Number(item.message_count || 0) === 1 ? "" : "s"}`;

        card.appendChild(title);
        card.appendChild(preview);
        card.appendChild(meta);
        card.addEventListener("click", () => restoreOperatorChat(item.chat_id));
        container.appendChild(card);
    });
}

function renderTechnicianRecent(items = []) {
    renderPersonalChatHistory(technicianRecentList, items, {
        cardClass: "technician-recent-item",
        emptyClass: "technician-recent-empty",
        emptyText: "Sin chats propios todavía",
    });
}

async function openMyConsultations() {
    if (!myConsultationsDialog) return;
    setStatus("Cargando historial personal...");
    try {
        const data = await window.hrrgApi.getJson("/api/monitoring/my-consultations?limit=10");
        renderMyConsultations(data.items || []);
        myConsultationsDialog.showModal();
        setStatus("Historial personal cargado.");
    } catch (error) {
        setStatus(error.message || "No se pudo cargar el historial personal.");
    }
}

async function loadTechnicianRecentChats() {
    if (!technicianRecentList) return;
    try {
        const data = await window.hrrgApi.getJson("/api/monitoring/my-chats?limit=5");
        renderTechnicianRecent(data.items || []);
    } catch (error) {
        renderTechnicianRecent([]);
    }
}

function renderOperatorChatHistory(items = []) {
    renderPersonalChatHistory(operatorHistoryList, items, {
        cardClass: "operator-history-card",
        emptyClass: "operator-history-empty",
        emptyText: "Sin chats recientes",
    });
}

async function loadOperatorChatHistory() {
    if (!operatorHistoryList) return;
    try {
        const data = await window.hrrgApi.getJson("/api/monitoring/my-chats?limit=5");
        renderOperatorChatHistory(data.items || []);
    } catch (error) {
        renderOperatorChatHistory([]);
    }
}

async function restoreOperatorChat(chatId) {
    if (!chatId) return;

    try {
        const data = await window.hrrgApi.getJson(`/api/monitoring/my-chats/${encodeURIComponent(chatId)}`);
        setActiveChatId(data.chat_id);
        selectedEquipmentId = data.equipment_id || selectedEquipmentId;
        selectedEquipmentName = data.equipment_name || selectedEquipmentName;

        if (activeEquipmentTitle && selectedEquipmentName) {
            activeEquipmentTitle.textContent = selectedEquipmentName;
        }

        removeLoadingMessage();
        activeRequestId = null;
        activeQuery = "";
        activeRequestCancelled = false;
        setBusy(false);
        chatMessages.innerHTML = "";
        conversationMessages = [];

        (data.turns || []).forEach((turn) => {
            addMessage("user", turn.question, {track: false});
            addMessage("assistant", turn.answer, {
                mode: "",
                sources: [],
                regenerable: false,
                track: false,
            });
        });

        conversationMessages = (data.turns || []).flatMap((turn) => [
            {role: "user", content: turn.question, options: {mode: "", sources: []}},
            {role: "assistant", content: turn.answer, options: {mode: "", sources: []}},
        ]);

        lastQuery = [...conversationMessages].reverse().find((message) => message.role === "user")?.content || "";
        await loadOperatorChatHistory();
        await loadTechnicianRecentChats();
        setStatus(`Chat reabierto: ${selectedEquipmentName}.`);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } catch (error) {
        setStatus(error.message || "No se pudo reabrir el chat.");
    }
}

function renderMonitoringKpis(indicators = {}) {
    const container = document.querySelector("#monitoring-kpis");
    if (!container) return;

    container.innerHTML = "";
    const total = Number(indicators.total_consultations || 0);
    [
        ["Consultas hoy", indicators.consultations_today || 0, total],
        ["Equipos consultados", indicators.consulted_equipment || 0, Math.max(total, indicators.consulted_equipment || 0)],
        ["Usuarios activos", indicators.active_users || 0, Math.max(total, indicators.active_users || 0)],
        ["Fallas recurrentes", indicators.recurrent_failures || 0, Math.max(total, indicators.recurrent_failures || 0)],
    ].forEach(([label, value, maxValue], index) => {
        const card = document.createElement("div");
        card.className = "monitoring-kpi";
        const strong = document.createElement("strong");
        strong.textContent = value;
        const span = document.createElement("span");
        span.textContent = label;
        const track = document.createElement("div");
        track.className = "monitoring-kpi-track";
        const bar = document.createElement("div");
        bar.className = `monitoring-kpi-bar chart-color-${(index % 4) + 1}`;
        const percent = maxValue ? Math.max(4, Math.min(100, Math.round((Number(value || 0) / maxValue) * 100))) : 0;
        bar.style.width = `${percent}%`;
        track.appendChild(bar);
        card.appendChild(strong);
        card.appendChild(span);
        card.appendChild(track);
        container.appendChild(card);
    });
}

function renderMonitoringInsights(data = {}) {
    const container = document.querySelector("#monitoring-insights");
    if (!container) return;

    container.innerHTML = "";
    const topEquipment = data.top_equipment?.[0];
    const topCategory = data.by_category?.[0];
    const topProfile = data.by_profile?.[0];
    const total = data.indicators?.total_consultations || 0;
    const insights = [
        topEquipment ? ["Equipo crítico", topEquipment.label, `${topEquipment.count} consultas`] : ["Equipo crítico", "Sin datos", "0 consultas"],
        topCategory ? ["Falla dominante", monitoringLabel(topCategory.label), `${topCategory.count} eventos`] : ["Falla dominante", "Sin datos", "0 eventos"],
        topProfile ? ["Perfil con mayor uso", topProfile.label, `${topProfile.count} consultas`] : ["Perfil con mayor uso", "Sin datos", "0 consultas"],
        ["Base analizada", `${total} consultas`, "Historial registrado"],
    ];

    insights.forEach(([label, value, note]) => {
        const card = document.createElement("article");
        card.className = "monitoring-insight-card";
        const small = document.createElement("span");
        small.textContent = label;
        const strong = document.createElement("strong");
        strong.textContent = value;
        const foot = document.createElement("small");
        foot.textContent = note;
        card.appendChild(small);
        card.appendChild(strong);
        card.appendChild(foot);
        container.appendChild(card);
    });
}

function renderMonitoringAlerts(items = []) {
    const container = document.querySelector("#monitoring-alerts");
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = "Sin alertas recurrentes dentro del periodo analizado.";
        container.appendChild(empty);
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = `monitoring-alert-card alert-${String(item.level || "media").toLowerCase()}`;
        const badge = document.createElement("span");
        badge.textContent = item.level || "Media";
        const title = document.createElement("strong");
        title.textContent = item.equipment || "Equipo sin identificar";
        const detail = document.createElement("p");
        detail.textContent = `${item.failure || "Falla recurrente"}: ${item.count || 0} ocurrencias`;
        const message = document.createElement("small");
        message.textContent = item.message || "Revisar recurrencia.";
        card.appendChild(badge);
        card.appendChild(title);
        card.appendChild(detail);
        card.appendChild(message);
        container.appendChild(card);
    });
}

function renderFailureMap(items = []) {
    const container = document.querySelector("#monitoring-failure-map");
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = "Sin recurrencias detectadas todavía.";
        container.appendChild(empty);
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "failure-card";
        const title = document.createElement("strong");
        title.textContent = item.equipment;
        const total = document.createElement("span");
        total.className = "failure-total";
        total.textContent = `${item.total} consultas asociadas`;
        card.appendChild(title);
        card.appendChild(total);

        const failures = item.failures || [];
        const maxCount = Math.max(...failures.map((failure) => Number(failure.count || 0)), 0);
        failures.forEach((failure, index) => {
            card.appendChild(createChartRow(failure, maxCount, index));
        });
        container.appendChild(card);
    });
}

function profileLabel(profile) {
    const value = String(profile || "").toLowerCase();
    if (value === "operador") return "Operador";
    if (value === "tecnico") return "Técnico";
    return "Sin perfil";
}

function renderMonitoringConsultations(items = []) {
    const container = document.querySelector("#monitoring-consultation-list");
    if (!container) return;

    container.innerHTML = "";
    if (!items.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = "No hay consultas para los filtros seleccionados.";
        container.appendChild(empty);
        return;
    }

    const count = document.createElement("p");
    count.className = "monitoring-search-count";
    count.textContent = `${items.length} consulta${items.length === 1 ? "" : "s"} encontradas`;
    container.appendChild(count);

    items.slice(0, 30).forEach((item) => {
        const card = document.createElement("article");
        card.className = "monitoring-consultation-card";
        const title = document.createElement("strong");
        title.textContent = item.equipment_name || "Equipo no registrado";
        const meta = document.createElement("span");
        meta.textContent = `${item.username || "Sin usuario"} · ${profileLabel(item.profile)} · ${item.date} ${item.time}`;
        const question = document.createElement("p");
        question.textContent = item.question || "Consulta sin detalle";
        const category = document.createElement("small");
        category.textContent = item.es_incidente ? `${monitoringLabel(item.category)} · incidente` : monitoringLabel(item.category);
        card.appendChild(title);
        card.appendChild(meta);
        card.appendChild(question);
        card.appendChild(category);
        container.appendChild(card);
    });
}

function monitoringFilterParams() {
    const params = new URLSearchParams();
    [
        ["search", monitoringSearchInput?.value],
        ["username", monitoringUserFilter?.value],
        ["equipment", monitoringEquipmentFilter?.value],
        ["date_from", monitoringDateFromFilter?.value],
        ["date_to", monitoringDateToFilter?.value],
    ].forEach(([key, value]) => {
        if (String(value || "").trim()) params.set(key, String(value).trim());
    });
    return params;
}

async function loadMonitoringSearch() {
    const container = document.querySelector("#monitoring-consultation-list");
    if (!container) return [];

    const params = monitoringFilterParams();
    const path = `/api/monitoring/consultations${params.toString() ? `?${params}` : ""}`;
    const consultations = await window.hrrgApi.getJson(path);
    const items = consultations.items || [];
    renderMonitoringConsultations(items);
    return items;
}

function groupCounts(items = [], keyBuilder) {
    const grouped = new Map();
    items.forEach((item) => {
        const key = keyBuilder(item);
        if (!key) return;
        grouped.set(key, (grouped.get(key) || 0) + 1);
    });
    return [...grouped.entries()]
        .map(([label, count]) => ({label, count}))
        .sort((a, b) => b.count - a.count);
}

function renderPriorityList(data = {}, consultations = []) {
    const container = document.querySelector("#monitoring-priority-list");
    if (!container) return;

    container.innerHTML = "";
    const topFailureMap = data.failure_map || [];
    const topCategory = data.by_category?.[0];
    const topEquipment = data.top_equipment?.[0];
    const priorities = [];

    topFailureMap.slice(0, 4).forEach((item) => {
        const mainFailure = item.failures?.[0];
        priorities.push({
            title: item.equipment,
            detail: mainFailure ? `${monitoringLabel(mainFailure.label)}: ${mainFailure.count} registros` : `${item.total} consultas`,
            action: "Revisar recurrencia técnica y validar si requiere intervención preventiva.",
            level: item.total >= 5 ? "Alta" : "Media",
        });
    });

    if (!priorities.length && topEquipment) {
        priorities.push({
            title: topEquipment.label,
            detail: `${topEquipment.count} consultas acumuladas`,
            action: "Analizar preguntas frecuentes y preparar guía operativa corta.",
            level: "Media",
        });
    }

    if (topCategory) {
        priorities.push({
            title: monitoringLabel(topCategory.label),
            detail: `${topCategory.count} eventos clasificados`,
            action: "Estandarizar respuesta y revisar necesidad de capacitación o checklist.",
            level: topCategory.count >= 5 ? "Alta" : "Media",
        });
    }

    if (!priorities.length && consultations.length) {
        const frequentEquipment = groupCounts(consultations, (item) => item.equipment_name)[0];
        priorities.push({
            title: frequentEquipment.label,
            detail: `${frequentEquipment.count} consultas registradas`,
            action: "Observar evolución durante los próximos turnos.",
            level: "Baja",
        });
    }

    if (!priorities.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = "Sin datos suficientes para priorizar intervenciones.";
        container.appendChild(empty);
        return;
    }

    priorities.slice(0, 5).forEach((item) => {
        const card = document.createElement("article");
        card.className = `priority-card priority-${item.level.toLowerCase()}`;
        const level = document.createElement("span");
        level.className = "priority-level";
        level.textContent = item.level;
        const title = document.createElement("strong");
        title.textContent = item.title;
        const detail = document.createElement("p");
        detail.textContent = item.detail;
        const action = document.createElement("small");
        action.textContent = item.action;
        card.appendChild(level);
        card.appendChild(title);
        card.appendChild(detail);
        card.appendChild(action);
        container.appendChild(card);
    });
}

function renderProfileFailureHeatmap(consultations = []) {
    const container = document.querySelector("#monitoring-heatmap");
    if (!container) return;

    container.innerHTML = "";
    if (!consultations.length) {
        const empty = document.createElement("p");
        empty.className = "audit-empty";
        empty.textContent = "Sin consultas suficientes para armar la matriz.";
        container.appendChild(empty);
        return;
    }

    const profiles = groupCounts(consultations, (item) => profileLabel(item.profile)).slice(0, 5).map((item) => item.label);
    const categories = groupCounts(consultations, (item) => monitoringLabel(item.category) || "Sin categoría").slice(0, 6).map((item) => item.label);
    const counts = new Map();
    consultations.forEach((item) => {
        const profile = profileLabel(item.profile);
        const category = monitoringLabel(item.category) || "Sin categoría";
        counts.set(`${profile}|${category}`, (counts.get(`${profile}|${category}`) || 0) + 1);
    });
    const maxCount = Math.max(...counts.values(), 1);

    const table = document.createElement("div");
    table.className = "heatmap-grid";
    table.style.gridTemplateColumns = `minmax(120px, 1.1fr) repeat(${categories.length}, minmax(82px, 1fr))`;

    const corner = document.createElement("div");
    corner.className = "heatmap-head heatmap-corner";
    corner.textContent = "Perfil";
    table.appendChild(corner);

    categories.forEach((category) => {
        const cell = document.createElement("div");
        cell.className = "heatmap-head";
        cell.textContent = category;
        table.appendChild(cell);
    });

    profiles.forEach((profile) => {
        const serviceCell = document.createElement("div");
        serviceCell.className = "heatmap-service";
        serviceCell.textContent = profile;
        table.appendChild(serviceCell);

        categories.forEach((category) => {
            const count = counts.get(`${profile}|${category}`) || 0;
            const cell = document.createElement("div");
            const intensity = count ? Math.max(0.16, count / maxCount) : 0;
            cell.className = "heatmap-cell";
            cell.style.setProperty("--heat", String(intensity));
            cell.textContent = count ? String(count) : "-";
            cell.title = `${profile} · ${category}: ${count}`;
            table.appendChild(cell);
        });
    });

    container.appendChild(table);
}

async function openMonitoringCenter() {
    if (!monitoringDialog) return;
    setStatus("Cargando Centro de Monitoreo...");
    try {
        const data = await window.hrrgApi.getJson("/api/monitoring/dashboard");
        renderMonitoringKpis(data.indicators || {});
        renderMonitoringInsights(data);
        renderMonitoringAlerts(data.alerts || []);
        renderAuditList("monitoring-equipment-list", data.top_equipment || []);
        renderAuditList("monitoring-users-list", data.top_users || []);
        renderAuditList("monitoring-service-list", data.by_profile || []);
        renderAuditList("monitoring-category-list", data.by_category || []);
        renderFailureMap(data.failure_map || []);
        const consultationItems = await loadMonitoringSearch();
        renderPriorityList(data, consultationItems);
        renderProfileFailureHeatmap(consultationItems);
        monitoringDialog.showModal();
        setStatus("Centro de Monitoreo actualizado.");
    } catch (error) {
        setStatus(error.message || "No se pudo cargar el Centro de Monitoreo.");
    }
}

if (chatForm) {
    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const query = messageInput.value.trim();
        if (!query) return;

        lastQuery = query;
        if (!event.detail?.skipUserMessage) addMessage("user", query);

        messageInput.value = "";
        await ask(query);
    });
}

if (abortButton) {
    abortButton.addEventListener("click", async () => {
        if (!activeRequestId) return;

        const requestId = activeRequestId;
        activeRequestCancelled = true;
        removeLoadingMessage();
        setBusy(false);
        activeRequestId = null;
        activeQuery = "";

        setStatus("Consulta detenida por el usuario.");
        window.hrrgSpeech?.stop?.();

        await window.hrrgApi.postJson("/api/chat/cancel", {request_id: requestId});
    });
}

if (ingestButton) {
    ingestButton.addEventListener("click", async () => {
        setStatus("Indexando Markdown desde data/processed...");
        ingestButton.disabled = true;

        try {
            const data = await window.hrrgApi.postJson("/api/ingest/", {});
            setStatus(
                `Ingesta finalizada: ${data.processed_files} Markdown, ${data.indexed_chunks} chunks, ${data.skipped_files.length} omitidos.`,
            );
            renderManualsAudit(data.audit || []);
        } catch (error) {
            addMessage("assistant", error.message || "No se pudo ejecutar la ingesta.");
            setStatus("No se pudo ejecutar la ingesta.");
        } finally {
            ingestButton.disabled = false;
        }
    });
}

if (manualsButton) {
    manualsButton.addEventListener("click", openManualsAudit);
}

if (monitoringButton) {
    monitoringButton.addEventListener("click", openMonitoringCenter);
}

if (monitoringCloseButton) {
    monitoringCloseButton.addEventListener("click", () => {
        monitoringDialog?.close();
    });
}

if (monitoringSearchInput) {
    monitoringSearchInput.addEventListener("input", async () => {
        await loadMonitoringSearch();
    });
}

[monitoringUserFilter, monitoringEquipmentFilter, monitoringDateFromFilter, monitoringDateToFilter]
    .filter(Boolean)
    .forEach((control) => {
        control.addEventListener("input", async () => {
            await loadMonitoringSearch();
        });
        control.addEventListener("change", async () => {
            await loadMonitoringSearch();
        });
    });

if (myConsultationsButton) {
    myConsultationsButton.addEventListener("click", openMyConsultations);
}

if (myConsultationsCloseButton) {
    myConsultationsCloseButton.addEventListener("click", () => {
        myConsultationsDialog?.close();
    });
}

if (manualsCloseButton) {
    manualsCloseButton.addEventListener("click", () => {
        manualsDialog?.close();
    });
}

if (newChatButton) {
    newChatButton.addEventListener("click", startNewChat);
}

if (equipmentDialogButton) {
    equipmentDialogButton.addEventListener("click", () => {
        document.querySelector("#equipment-dialog")?.showModal();
    });
}

if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
        const data = await window.hrrgApi.postJson("/api/auth/logout", {});
        window.location.href = data.redirect_url || "/login";
    });
}

if (equipmentSelect) {
    equipmentSelect.addEventListener("change", async () => {
        const selectedOption = equipmentSelect.selectedOptions[0];
        await selectEquipment(
            selectedOption.value,
            selectedOption.dataset.equipmentName,
        );
    });
}

if (qrButton) {
    qrButton.addEventListener("click", async () => {
        if (!selectedEquipmentId) {
            setStatus("Seleccione un equipo antes de generar su QR.");
            document.querySelector("#equipment-dialog")?.showModal();
            return;
        }

        qrButton.disabled = true;
        setStatus("Generando codigo QR del equipo seleccionado...");

        try {
            const data = await window.hrrgApi.postJson("/api/qr/", {
                equipment_id: selectedEquipmentId,
                base_url: window.location.origin,
            });

            const result = data.generated[0];
            const imageUrl = `/static/img/qr/qr_${result.equipment_id}.png?ts=${Date.now()}`;

            qrTitle.textContent = result.equipment_name;
            qrImage.src = imageUrl;
            qrUrl.textContent = result.url;
            qrOpenLink.href = result.url;
            if (qrDownloadLink) {
                qrDownloadLink.href = `/api/qr/${encodeURIComponent(result.equipment_id)}/download`;
            }
            if (qrPrintLink) {
                qrPrintLink.href = `/api/qr/${encodeURIComponent(result.equipment_id)}/print`;
            }
            qrDialog.showModal();

            setStatus(`QR listo para ${result.equipment_name}.`);
        } catch (error) {
            addMessage("assistant", error.message);
            setStatus("No se pudo generar el QR.");
        } finally {
            qrButton.disabled = false;
        }
    });
}

if (qrCopyButton) {
    qrCopyButton.addEventListener("click", async () => {
        const value = qrUrl.textContent.trim();
        if (!value) return;

        await navigator.clipboard.writeText(value);
        setStatus("URL del QR copiada.");
    });
}

if (voiceButton) {
    recognition = window.hrrgSpeech.createRecognition(
        (text) => {
            messageInput.value = text;
            setStatus("Texto reconocido por voz.");
        },
        setStatus,
    );

    voiceButton.addEventListener("click", () => {
        if (!recognition) {
            setStatus("El navegador no soporta entrada por voz.");
            return;
        }

        recognition.start();
        setStatus("Escuchando...");
    });
}

if (speechToggleButton) {
    speechToggleButton.addEventListener("click", () => {
        setSpeechMuted(!speechMuted);
    });
}

document.querySelectorAll(".equipment-card").forEach((button) => {
    button.addEventListener("click", async () => {
        await selectEquipment(button.dataset.equipmentId, button.dataset.equipmentName);
    });
});

updateSpeechControls();
renderHistory();
loadTechnicianRecentChats();
loadOperatorChatHistory();
