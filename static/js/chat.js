const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector("#chat-messages");
const newChatButton = document.querySelector("#new-chat-button");
const activeEquipmentTitle = document.querySelector("#active-equipment");
const equipmentModal = document.querySelector("#equipment-modal");
const closeEquipmentModalButton = document.querySelector("#close-equipment-modal");
const equipmentOptions = document.querySelectorAll(".equipment-option");
const ingestButton = document.querySelector("#ingest-button");
const voiceButton = document.querySelector("#voice-button");
const ticketButton = document.querySelector("#ticket-button");
const statusStrip = document.querySelector("#status-strip");
const submitButton = chatForm.querySelector(".send-button");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechSynthesisAvailable = "speechSynthesis" in window;

let selectedEquipment = activeEquipmentTitle.textContent.trim();
let recognition = null;
let isListening = false;
let activeRequestController = null;
let activeRequestId = null;
let activeLoadingMessage = null;
let lastQuestion = "";

function scrollToLatestMessage() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setStatus(message) {
    statusStrip.textContent = message;
}

function escapeHtml(value) {
    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderMarkdown(value) {
    let html = escapeHtml(value);
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    html = html.replace(/\n/g, "<br>");
    return html;
}

function createAvatar() {
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent = "AI";
    return avatar;
}

function createSourcesList(sources = []) {
    if (!sources.length) {
        return null;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "source-list";

    const title = document.createElement("div");
    title.className = "source-list-title";
    title.textContent = "Fuentes";
    wrapper.appendChild(title);

    sources.forEach((source, index) => {
        const link = document.createElement("a");
        link.className = "source-chip";
        link.href = source.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.innerHTML = `<span>${index + 1}</span><em>${escapeHtml(source.source_file)} · pagina ${escapeHtml(String(source.page))}</em>`;
        wrapper.appendChild(link);
    });

    return wrapper;
}

function createRegenerateButton() {
    const actions = document.createElement("div");
    actions.className = "message-actions";

    const button = document.createElement("button");
    button.className = "inline-action";
    button.type = "button";
    button.textContent = "Regenerar respuesta";
    button.addEventListener("click", async () => {
        if (lastQuestion) {
            await sendQuestion(lastQuestion, {repeatUserMessage: false});
        }
    });

    actions.appendChild(button);
    return actions;
}

function createMessage(role, content, options = {}) {
    const message = document.createElement("article");
    message.className = `message ${role}`;

    if (options.error) {
        message.classList.add("error");
    }

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (role === "assistant") {
        bubble.innerHTML = renderMarkdown(content);
    } else {
        bubble.textContent = content;
    }

    contentWrapper.appendChild(bubble);

    const sourcesList = createSourcesList(options.sources);
    if (sourcesList) {
        contentWrapper.appendChild(sourcesList);
    }

    if (role === "assistant" && options.regenerable) {
        contentWrapper.appendChild(createRegenerateButton());
    }

    if (role === "assistant") {
        message.appendChild(createAvatar());
    }

    message.appendChild(contentWrapper);
    chatMessages.appendChild(message);
    scrollToLatestMessage();

    return message;
}

function createLoadingMessage(query) {
    const message = document.createElement("article");
    message.className = "message assistant";

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "bubble loading-bubble";
    bubble.setAttribute("aria-label", "El asistente esta procesando la consulta");

    for (let i = 0; i < 3; i += 1) {
        const dot = document.createElement("span");
        dot.className = "loading-dot";
        bubble.appendChild(dot);
    }

    const actions = document.createElement("div");
    actions.className = "message-actions";

    const chromaButton = document.createElement("button");
    chromaButton.className = "inline-action chroma-action";
    chromaButton.type = "button";
    chromaButton.textContent = "Usar ChromaDB ahora";
    chromaButton.addEventListener("click", async () => {
        await useChromaNow(query);
    });

    actions.appendChild(chromaButton);
    contentWrapper.appendChild(bubble);
    contentWrapper.appendChild(actions);
    message.appendChild(createAvatar());
    message.appendChild(contentWrapper);
    chatMessages.appendChild(message);
    scrollToLatestMessage();

    return message;
}

function speak(text) {
    if (!speechSynthesisAvailable) {
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text.slice(0, 1200));
    utterance.lang = "es-AR";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}

function setComposerBusy(isBusy) {
    messageInput.disabled = isBusy;
    submitButton.disabled = isBusy;
}

function setListeningState(nextState) {
    isListening = nextState;
    voiceButton.classList.toggle("listening", isListening);
    voiceButton.setAttribute("aria-pressed", String(isListening));
    voiceButton.title = isListening ? "Escuchando..." : "Consulta por voz";
}

function ensureRecognition() {
    if (!SpeechRecognition) {
        return null;
    }

    if (recognition) {
        return recognition;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "es-AR";
    recognition.interimResults = false;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        setListeningState(true);
        setStatus("Escuchando consulta por voz...");
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.trim();
        messageInput.value = transcript;
        messageInput.focus();
        setStatus("Texto reconocido y cargado en la caja de consulta.");
    };

    recognition.onerror = (event) => {
        setStatus(`No se pudo capturar audio: ${event.error}.`);
    };

    recognition.onend = () => {
        setListeningState(false);
    };

    return recognition;
}

function toggleVoiceCapture() {
    const speechRecognition = ensureRecognition();

    if (!speechRecognition) {
        setStatus("El navegador no soporta entrada por voz.");
        return;
    }

    if (isListening) {
        speechRecognition.stop();
        return;
    }

    try {
        speechRecognition.start();
    } catch (error) {
        setListeningState(false);
        setStatus("La captura de voz ya estaba activa.");
    }
}

async function cancelActiveLlmRequest() {
    if (!activeRequestId) {
        return;
    }

    await fetch("/requests/cancel", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({request_id: activeRequestId}),
    });

    if (activeRequestController) {
        activeRequestController.abort();
    }
}

async function requestAnswer(query, options = {}) {
    const requestId = crypto.randomUUID();
    const controller = new AbortController();

    if (!options.forceFallback) {
        activeRequestId = requestId;
        activeRequestController = controller;
    }

    const response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        signal: controller.signal,
        body: JSON.stringify({
            query,
            equipment: selectedEquipment,
            force_fallback: Boolean(options.forceFallback),
            request_id: requestId,
        }),
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "No se pudo obtener una respuesta.");
    }
    return data;
}

async function useChromaNow(query) {
    setStatus("Suspendiendo espera del LLM y consultando ChromaDB...");
    await cancelActiveLlmRequest();

    try {
        const data = await requestAnswer(query, {forceFallback: true});
        if (activeLoadingMessage) {
            activeLoadingMessage.remove();
            activeLoadingMessage = null;
        }
        createMessage("assistant", data.answer, {
            sources: data.sources,
            regenerable: true,
        });
        setStatus("Respuesta documental generada con ChromaDB.");
    } catch (error) {
        if (error.name !== "AbortError") {
            createMessage("assistant", error.message, {error: true});
        }
    } finally {
        activeRequestController = null;
        activeRequestId = null;
        setComposerBusy(false);
        messageInput.focus();
    }
}

async function sendQuestion(query, options = {}) {
    lastQuestion = query;

    if (!options.repeatUserMessage) {
        createMessage("user", query);
    }

    messageInput.value = "";
    setComposerBusy(true);
    activeLoadingMessage = createLoadingMessage(query);

    try {
        const data = await requestAnswer(query);
        if (activeLoadingMessage) {
            activeLoadingMessage.remove();
            activeLoadingMessage = null;
        }
        createMessage("assistant", data.answer, {
            sources: data.sources,
            regenerable: true,
        });
        setStatus(`Modo de respuesta: ${data.mode}${data.ticket_id ? ` | Ticket #${data.ticket_id}` : ""}`);
        speak(data.answer);
    } catch (error) {
        if (activeLoadingMessage) {
            activeLoadingMessage.remove();
            activeLoadingMessage = null;
        }
        if (error.name !== "AbortError") {
            createMessage("assistant", error.message, {error: true});
            setStatus("Se produjo un error en la consulta.");
        }
    } finally {
        activeRequestController = null;
        activeRequestId = null;
        setComposerBusy(false);
        messageInput.focus();
        scrollToLatestMessage();
    }
}

function openEquipmentModal() {
    equipmentModal.classList.add("visible");
    equipmentModal.setAttribute("aria-hidden", "false");
    equipmentOptions[0].focus();
}

function closeEquipmentModal() {
    equipmentModal.classList.remove("visible");
    equipmentModal.setAttribute("aria-hidden", "true");
    newChatButton.focus();
}

async function clearServerMemory() {
    try {
        await fetch("/memory/clear", {method: "POST"});
    } catch (error) {
        setStatus("No se pudo limpiar la memoria de la sesion.");
    }
}

async function selectEquipment(equipment) {
    selectedEquipment = equipment;
    activeEquipmentTitle.textContent = equipment;
    chatMessages.innerHTML = "";
    lastQuestion = "";
    await clearServerMemory();
    createMessage("assistant", `Nuevo chat iniciado para ${equipment}.`);
    setStatus(`Equipo seleccionado: ${equipment}.`);
    closeEquipmentModal();
    messageInput.focus();
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = messageInput.value.trim();
    if (query) {
        await sendQuestion(query);
    }
});

ingestButton.addEventListener("click", async () => {
    setStatus("Indexando PDFs desde data/raw...");
    try {
        const response = await fetch("/ingest", {method: "POST"});
        const data = await response.json();
        setStatus(`${data.message} Archivos: ${data.processed_files}. Chunks: ${data.indexed_chunks}.`);
        if (data.errors && data.errors.length > 0) {
            createMessage("assistant", `Ingesta finalizada con errores:\n${data.errors.join("\n")}`, {error: true});
        }
    } catch (error) {
        setStatus(`No se pudo ejecutar la ingesta: ${error.message}`);
    }
});

ticketButton.addEventListener("click", async () => {
    const question = messageInput.value.trim() || "Solicitud manual del tecnico sin detalle adicional.";
    const response = await fetch("/tickets", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            question,
            equipment: selectedEquipment,
            reason: "Ticket manual generado desde la interfaz tecnica.",
        }),
    });
    const data = await response.json();
    if (response.ok) {
        setStatus(`Ticket manual #${data.ticket_id} creado.`);
    } else {
        setStatus(data.error || "No se pudo crear el ticket.");
    }
});

voiceButton.addEventListener("click", toggleVoiceCapture);
newChatButton.addEventListener("click", openEquipmentModal);
closeEquipmentModalButton.addEventListener("click", closeEquipmentModal);

equipmentOptions.forEach((option) => {
    option.addEventListener("click", async () => {
        await selectEquipment(option.dataset.equipment);
    });
});

equipmentModal.addEventListener("click", (event) => {
    if (event.target === equipmentModal) {
        closeEquipmentModal();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && equipmentModal.classList.contains("visible")) {
        closeEquipmentModal();
    }
});

scrollToLatestMessage();
