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
const statusStrip = document.querySelector("#status-strip");
const submitButton = chatForm.querySelector(".send-button");

// --- ELEMENTOS DE LOGIN ---
const loginModal = document.querySelector("#login-modal");
const loginForm = document.querySelector("#login-form");
const loginError = document.querySelector("#login-error");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechSynthesisAvailable = "speechSynthesis" in window;

// --- LECTURA DE CÓDIGO QR Y ROLES ---
const urlParams = new URLSearchParams(window.location.search);
const urlEquipment = urlParams.get('equipo');
const urlRole = urlParams.get('rol') || 'tecnico'; // Por defecto es técnico
const currentRole = urlRole.toLowerCase() === 'operador' ? 'operador' : 'tecnico';

// Inicializar el equipo activo (priorizando la URL si viene del QR)
let selectedEquipment = urlEquipment || activeEquipmentTitle.textContent.trim();
if (urlEquipment) {
    activeEquipmentTitle.textContent = selectedEquipment;
}

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

    // Solo mostrar el botón de forzar ChromaDB si es técnico
    if (currentRole === 'tecnico') {
        const chromaButton = document.createElement("button");
        chromaButton.className = "inline-action chroma-action";
        chromaButton.type = "button";
        chromaButton.textContent = "Usar ChromaDB ahora";
        chromaButton.addEventListener("click", async () => {
            await useChromaNow(query);
        });
        actions.appendChild(chromaButton);
    }

    contentWrapper.appendChild(bubble);
    if (currentRole === 'tecnico') {
        contentWrapper.appendChild(actions);
    }
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
            user_role: currentRole // Enviamos el rol al backend
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
        setStatus(`Modo de respuesta: ${data.mode}`);
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
    // Si es operador, bloqueamos la apertura del modal
    if (currentRole === 'operador') return;
    
    equipmentModal.classList.add("visible");
    equipmentModal.setAttribute("aria-hidden", "false");
    if (equipmentOptions.length > 0) {
        equipmentOptions[0].focus();
    }
}

function closeEquipmentModal() {
    equipmentModal.classList.remove("visible");
    equipmentModal.setAttribute("aria-hidden", "true");
    if(newChatButton) newChatButton.focus();
}

async function clearServerMemory() {
    try {
        await fetch("/memory/clear", {method: "POST"});
    } catch (error) {
        setStatus("No se pudo limpiar la memoria de la sesion.");
    }
}

async function selectEquipment(equipment) {
    if (currentRole === 'operador') return; // Seguridad extra
    
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

// Verificación defensiva por si el botón fue ocultado/eliminado
if (ingestButton) {
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
}

if (voiceButton) {
    voiceButton.addEventListener("click", toggleVoiceCapture);
}

if (newChatButton) newChatButton.addEventListener("click", openEquipmentModal);
if (closeEquipmentModalButton) closeEquipmentModalButton.addEventListener("click", closeEquipmentModal);

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

// --- LÓGICA DE INICIO (LOGIN Y RESTRICCIONES VISUALES) ---
function initializeApp() {
    if (currentRole === 'tecnico') {
        // Bloquear pantalla con el login si el modal existe en el HTML
        if (loginModal && loginForm) {
            loginModal.classList.add("visible");
            loginModal.setAttribute("aria-hidden", "false");
            const userField = document.querySelector("#username");
            if (userField) userField.focus();

            loginForm.addEventListener("submit", (e) => {
                e.preventDefault();
                const passField = document.querySelector("#password");
                const pass = passField ? passField.value.trim() : "";
                
                // Validación frontend de prototipo
                if (pass === "tecnico-hrrg") {
                    loginModal.classList.remove("visible");
                    loginModal.setAttribute("aria-hidden", "true");
                    if (loginError) loginError.style.display = "none";
                    openEquipmentModal(); // Obligamos a elegir el equipo
                } else {
                    if (loginError) loginError.style.display = "block";
                }
            });
        }
    } else if (currentRole === 'operador') {
        // Ocultar modal de login si existiera
        if(loginModal) {
            loginModal.classList.remove("visible");
            loginModal.setAttribute("aria-hidden", "true");
        }

        // Ocultar botones de la barra lateral
        if(newChatButton) newChatButton.style.display = 'none';
        if(ingestButton) ingestButton.style.display = 'none';
        
        // Ocultar la barra lateral completamente
        const toolSidebar = document.querySelector('.tool-sidebar');
        if(toolSidebar) toolSidebar.style.display = 'none';

        // --- MAGIA RESPONSIVA PARA PC ---
        const appShell = document.querySelector('.app-shell');
        if(appShell) {
            appShell.style.display = 'flex';
            appShell.style.justifyContent = 'center';
            // Se quita la grilla (grid) predeterminada para que el panel tome el control
            appShell.style.gridTemplateColumns = '1fr'; 
        }
        
        const chatPanel = document.querySelector('.chat-panel');
        if(chatPanel) {
            chatPanel.style.width = '100%';
            chatPanel.style.maxWidth = '900px'; // Centrado y de lectura cómoda
            chatPanel.style.margin = '0 auto';
            chatPanel.style.borderLeft = 'none';
        }

        // Mensaje de bienvenida adaptado a Primera Línea
        chatMessages.innerHTML = ''; 
        createMessage("assistant", `**Asistencia Clínica de Primera Línea**\n\nEstás operando el equipo: **${selectedEquipment}**.\n\nEscribe o dicta el síntoma o la alarma que presenta el equipo para recibir instrucciones. Recuerda que si hay riesgo, debes contactar a Ingeniería Clínica inmediatamente.`);
    }
}

// Ejecutar inicialización al cargar
initializeApp();
scrollToLatestMessage();
