window.hrrgApi = {
    async getJson(url) {
        let response;
        try {
            response = await fetch(url);
        } catch (error) {
            throw new Error("No se pudo conectar con el servidor local.");
        }
        let data = {};
        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }
        if (!response.ok) {
            throw new Error(data.error || "No se pudo completar la solicitud.");
        }
        return data;
    },

    async postJson(url, payload) {
        let response;
        try {
            response = await fetch(url, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
        } catch (error) {
            throw new Error("No se pudo conectar con el servidor local.");
        }
        let data = {};
        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }
        if (!response.ok) {
            throw new Error(data.error || "No se pudo completar la solicitud.");
        }
        return data;
    },
};
