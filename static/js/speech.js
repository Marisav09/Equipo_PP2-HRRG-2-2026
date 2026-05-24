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
        utterance.lang = "es-AR";

        // Obtener voces disponibles
        const voices = window.speechSynthesis.getVoices();

        // Buscar alguna voz latina (ej: Google español latinoamericano)
        const vozLatina = voices.find(v =>
            v.lang === "es-AR" ||
            v.lang === "es-MX" ||
            v.lang === "es-US" ||
            v.name.toLowerCase().includes("latino")
        );

        if (vozLatina) {
            utterance.voice = vozLatina;
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
