let hrrgPreferredVoice = null;

function normalizeVoiceText(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
}

function choosePreferredVoice() {
    if (!("speechSynthesis" in window)) {
        return null;
    }

    const voices = window.speechSynthesis.getVoices();
    if (!voices.length) {
        return null;
    }

    hrrgPreferredVoice = voices.find((voice) => voice.lang === "es-AR")
        || voices.find((voice) => voice.lang === "es-MX")
        || voices.find((voice) => voice.lang === "es-US")
        || voices.find((voice) => voice.lang === "es-419")
        || voices.find((voice) => {
            const name = normalizeVoiceText(voice.name);
            return voice.lang.startsWith("es")
                && (name.includes("latino")
                    || name.includes("latin")
                    || name.includes("argentina")
                    || name.includes("mexico"));
        })
        || voices.find((voice) => voice.lang.startsWith("es") && voice.lang !== "es-ES")
        || voices.find((voice) => voice.lang.startsWith("es"))
        || null;

    return hrrgPreferredVoice;
}

if ("speechSynthesis" in window) {
    choosePreferredVoice();
    window.speechSynthesis.addEventListener?.("voiceschanged", choosePreferredVoice);
}

window.hrrgSpeech = {
    createRecognition(onText, onStatus) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            return null;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = "es-AR";
        recognition.interimResults = false;
        recognition.continuous = false;
        recognition.onresult = (event) => onText(event.results[0][0].transcript.trim());
        recognition.onerror = (event) => onStatus(`No se pudo capturar audio: ${event.error}.`);
        return recognition;
    },

    speak(text) {
        if (!("speechSynthesis" in window)) {
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text.slice(0, 1200));
        const voice = hrrgPreferredVoice || choosePreferredVoice();

        utterance.lang = "es-AR";
        if (voice) {
            utterance.voice = voice;
            utterance.lang = voice.lang || "es-AR";
        }

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    },

    stop() {
        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }
    },
};
