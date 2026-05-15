const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const chatMessages = document.querySelector("#chat-messages");
const newChatButton = document.querySelector("#new-chat-button");
const activeEquipmentTitle = document.querySelector("#active-equipment");
const equipmentModal = document.querySelector("#equipment-modal");
const closeEquipmentModalButton = document.querySelector("#close-equipment-modal");
const equipmentOptions = document.querySelectorAll(".equipment-option");

let selectedEquipment = activeEquipmentTitle.textContent.trim();

function scrollToLatestMessage() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createMessage(role, content, options = {}) {
    const message = document.createElement("article");
    message.className = `message ${role}`;

    if (options.error) {
        message.classList.add("error");
    }

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = content;

    message.appendChild(bubble);
    chatMessages.appendChild(message);
    scrollToLatestMessage();

    return message;
}

function createLoadingMessage() {
    const message = document.createElement("article");
    message.className = "message assistant";
    message.id = "loading-message";

    const bubble = document.createElement("div");
    bubble.className = "bubble loading-bubble";
    bubble.setAttribute("aria-label", "El asistente esta generando una respuesta");

    for (let i = 0; i < 3; i += 1) {
        const dot = document.createElement("span");
        dot.className = "loading-dot";
        bubble.appendChild(dot);
    }

    message.appendChild(bubble);
    chatMessages.appendChild(message);
    scrollToLatestMessage();

    return message;
}

function setComposerBusy(isBusy) {
    messageInput.disabled = isBusy;
    chatForm.querySelector("button").disabled = isBusy;
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

function startNewChat(equipment) {
    selectedEquipment = equipment;
    activeEquipmentTitle.textContent = equipment;
    chatMessages.innerHTML = "";

    if (equipment === "Busqueda general") {
        createMessage(
            "assistant",
            "Nuevo chat de busqueda general iniciado. Describe el equipo, sintoma, alarma o contexto clinico que tengas disponible."
        );
    } else {
        createMessage(
            "assistant",
            `Nuevo chat iniciado para ${equipment}. Puedes consultar fallas, mantenimiento, seguridad o documentacion tecnica.`
        );
    }

    closeEquipmentModal();
    messageInput.focus();
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = messageInput.value.trim();

    if (!query) {
        return;
    }

    createMessage("user", query);
    messageInput.value = "";
    setComposerBusy(true);

    const loadingMessage = createLoadingMessage();

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query, equipment: selectedEquipment }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "No se pudo obtener una respuesta.");
        }

        loadingMessage.remove();
        createMessage("assistant", data.answer);
    } catch (error) {
        loadingMessage.remove();
        createMessage("assistant", error.message, { error: true });
    } finally {
        setComposerBusy(false);
        messageInput.focus();
        scrollToLatestMessage();
    }
});

newChatButton.addEventListener("click", () => {
    openEquipmentModal();
});

closeEquipmentModalButton.addEventListener("click", closeEquipmentModal);

equipmentOptions.forEach((option) => {
    option.addEventListener("click", () => {
        startNewChat(option.dataset.equipment);
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
