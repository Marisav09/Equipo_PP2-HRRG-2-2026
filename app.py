from flask import Flask, jsonify, render_template, request

from rag_engine import get_response


app = Flask(__name__)


MOCK_CHATS = [
    {
        "id": index,
        "title": title,
        "equipment": equipment,
        "preview": preview,
    }
    for index, (title, equipment, preview) in enumerate(
        [
            (
                "Bomba de infusion",
                "Infusomat Space",
                "Consulta sobre alarma de oclusion distal.",
            ),
            (
                "Monitor multiparametrico",
                "Mindray BeneVision N15",
                "Revision de protocolo de mantenimiento preventivo.",
            ),
            (
                "Ventilador mecanico",
                "Hamilton C6",
                "Parametros recomendados para prueba funcional.",
            ),
            (
                "Desfibrilador",
                "Zoll R Series",
                "Verificacion de bateria y prueba de descarga.",
            ),
            (
                "Electrobisturi",
                "Valleylab Force FX",
                "Analisis de falla en placa paciente.",
            ),
            (
                "Incubadora neonatal",
                "Drager Isolette",
                "Control de temperatura fuera de tolerancia.",
            ),
            (
                "Autoclave",
                "Tuttnauer 3870",
                "Ciclo incompleto durante esterilizacion.",
            ),
            (
                "Rayos X portatil",
                "MobileDaRt Evolution",
                "Checklist de seguridad radiologica.",
            ),
            (
                "Ecografo",
                "GE Logiq P9",
                "Problema de conectividad con transductor.",
            ),
            (
                "Cama UCI",
                "Hillrom Progressa",
                "Revision de actuadores y panel de control.",
            ),
        ],
        start=1,
    )
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        chats=MOCK_CHATS,
        active_equipment="Infusomat Space",
    )


@app.post("/ask")
def ask():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "La consulta no puede estar vacia."}), 400

    answer = get_response(query)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
