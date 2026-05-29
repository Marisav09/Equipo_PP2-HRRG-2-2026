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
const qrCopyButton = document.querySelector("#qr-copy-button");
const activeEquipmentTitle = document.querySelector("#active-equipment");
const equipmentSelect = document.querySelector("#equipment-select");
const historyList = document.querySelector("#history-list");

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

function modeLabel(mode) {
    const labels = {
        llm: "MODO: ASISTENTE INTELIGENTE (AI)",
        fallback_chromadb: "MODO: DIRECTO A FUENTE",
        fallback_timeout: "MODO: DIRECTO A FUENTE POR TIEMPO AGOTADO",
        fallback_llm_error: "MODO: DIRECTO A FUENTE POR FALLA DEL MODELO LOCAL",
        guardrail: "MODO: GUARDRAIL DE SEGURIDAD",
        cancelled: "MODO: CONSULTA DETENIDA",
        sin_documentos: "MODO: SIN DOCUMENTOS INDEXADOS",
        sin_informacion: "MODO: SIN INFORMACION DOCUMENTAL",
        contexto_insuficiente_operador: "MODO: SEGURIDAD CLINICA",
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

function visibleSourcePage(source = {}) {
    return source.pdf_page || source.page || "sin pagina";
}

function visibleSourceLabel(source = {}) {
    return `Fuente: ${visibleSourceName(source)}, pag. ${visibleSourcePage(source)}`;
}

function createSourceList(sources = []) {
    if (!sources.length) return null;

    const wrapper = document.createElement("div");
    wrapper.className = "source-list";

    sources.forEach((source, index) => {
        const link = document.createElement("a");
        link.className = "source-chip";
        link.href = source.url || "#";
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.title = `${visibleSourceName(source)}, pagina ${visibleSourcePage(source)}`;

        const badge = document.createElement("span");
        badge.textContent = String(index + 1);

        const label = document.createTextNode(visibleSourceLabel(source));

        link.appendChild(badge);
        link.appendChild(label);
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
        preview.alt = image.label || `Imagen pagina ${image.page}`;

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
    String(text || "").split("\n").forEach((line, index) => {
        if (index > 0) container.appendChild(document.createElement("br"));
        container.appendChild(document.createTextNode(line));
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

        bubble.appendChild(document.createTextNode(line));
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

function createSpeechAction(content) {
    const button = document.createElement("button");
    button.className = "inline-action speech-action";
    button.type = "button";
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
        avatar.className = "avatar";
        avatar.textContent = "AI";
        message.appendChild(avatar);
    }

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    const visibleContent = role === "assistant" && shell.dataset.role === "tecnico" && !fallbackMode
        ? stripSourceLines(content)
        : content;

    if (role === "assistant" && fallbackMode) {
        renderFallbackBubble(bubble, visibleContent, options.sources || []);
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
    avatar.className = "avatar";
    avatar.textContent = "AI";
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
        empty.textContent = "Todavia no hay documentos auditados. Ejecute la ingesta de manuales.";
        manualsList.appendChild(empty);
        return;
    }

    documents.forEach((documentInfo) => {
        const row = document.createElement("article");
        row.className = "manual-row";

        const title = document.createElement("div");
        title.className = "manual-title";

        const source = document.createElement("strong");
        source.textContent = documentInfo.display_source || documentInfo.original_pdf || documentInfo.source_file;

        const date = document.createElement("span");
        date.textContent = documentInfo.created_at || "Sin fecha";

        title.appendChild(source);
        title.appendChild(date);

        const equipment = document.createElement("div");
        equipment.className = "manual-equipment";

        const equipmentName = document.createElement("strong");
        equipmentName.textContent = documentInfo.equipment_name || "Sin equipo asociado";

        const metrics = document.createElement("span");
        metrics.className = "manual-metrics";
        metrics.textContent = `${documentInfo.page_count || 0} paginas - ${documentInfo.chunk_count || 0} chunks - ${documentInfo.image_count || 0} imagenes`;

        equipment.appendChild(equipmentName);
        equipment.appendChild(metrics);

        const status = document.createElement("span");
        status.className = `manual-status ${documentInfo.status}`;
        status.title = documentInfo.message || "";
        status.textContent = statusLabel(documentInfo.status);

        row.appendChild(title);
        row.appendChild(equipment);
        row.appendChild(status);
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

    addMessage("assistant", `Chat nuevo iniciado para ${selectedEquipmentName}.`);
    setStatus(`Chat nuevo para ${selectedEquipmentName}. Memoria de sesion limpiada.`);
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

    addMessage("assistant", `Nuevo chat iniciado para ${selectedEquipmentName}.`);
    document.querySelector("#equipment-dialog")?.close();
    setStatus(`Equipo seleccionado: ${selectedEquipmentName}. Memoria de sesion limpiada.`);
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
        });

        if (activeRequestCancelled || activeRequestId !== requestId) return;

        removeLoadingMessage();
        addMessage("assistant", data.answer, {
            sources: shell.dataset.role === "tecnico" ? data.sources : [],
            mode: data.mode,
            regenerable: true,
        });

        saveHistoryEntry(selectedEquipmentName);
        setStatus(modeLabel(data.mode));

        if (!speechMuted) {
            window.hrrgSpeech.speak(data.answer);
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

document.querySelectorAll(".equipment-card").forEach((button) => {
    button.addEventListener("click", async () => {
        await selectEquipment(button.dataset.equipmentId, button.dataset.equipmentName);
    });
});

renderHistory();