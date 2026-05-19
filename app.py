from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

knowledge = {
    "father profession": "My father is an irrigation department officer. He manages water supply and irrigation projects for farms.",
    "what is your job": "I work as an irrigation officer. I plan water distribution and maintain irrigation systems.",
    "what do you do": "I inspect canals, monitor water flow, and organize water delivery for crops.",
    "how do you help farmers": "I help farmers by making sure their fields receive water on time and by managing irrigation channels.",
    "what is irrigation": "Irrigation means giving water to land so crops can grow well.",
    "what education is needed": "A good path is civil engineering or water resources engineering to work in irrigation.",
    "what are your duties": "My duties include canal maintenance, field visits, water planning, and irrigation project monitoring.",
    "what is your department": "I work in the irrigation department, which manages water supply and farm irrigation.",
    "where do you work": "I work at farms, dams, canals, and irrigation project sites.",
    "do you have any query": "You can ask about irrigation, farmer water needs, or the irrigation department.",
    "canal water schedule": "Canal water schedules depend on the local system and season. Contact your nearby irrigation office for the exact schedule and availability.",
    "water availability": "Water availability varies by canal and region. The irrigation department publishes daily schedules and availability notices for farms.",
    "water shortage complaint": "To report a water shortage, contact your local irrigation office with details about the canal, location, and issue. They will register your complaint and investigate.",
    "irrigation laws": "Irrigation laws and regulations cover water distribution, canal maintenance, and farmer rights. For details, check your district irrigation department or official government documents.",
    "nearest irrigation office": "The nearest irrigation office can be found by giving your village or tehsil name to the district office helpline or visiting the local department website.",
    "department policies": "Department policies guide water allocation, maintenance, staff conduct, and complaint handling. Staff follow official procedure manuals and policies.",
    "report templates": "Report templates include water release logs, maintenance reports, and complaint records. Use the department-approved forms when preparing reports.",
    "officer job": "An irrigation officer inspects canals, plans water distribution, manages irrigation projects, and helps farmers with water-related needs.",
}

follow_up = "If you have another question, please ask one question at a time."
fallback = (
    "I do not have an exact answer for that. "
    "Please ask one simple question about irrigation or the irrigation department."
)
initial_message = (
    "Hello! This chatbot is about a father working as an irrigation department officer. "
    "Please ask one question at a time."
)


def normalize_text(text):
    return re.sub(r"[^a-z0-9\s]", "", text.lower()).strip()


def find_answer(question):
    text = normalize_text(question)
    for key, answer in knowledge.items():
        if key in text:
            return answer

    if any(word in text for word in ["father", "profession", "job", "work", "officer"]):
        return knowledge["father profession"]
    if any(word in text for word in ["farmer", "farmers", "help", "support"]):
        return knowledge["how do you help farmers"]
    if any(word in text for word in ["schedule", "canal water", "water schedule", "availability"]):
        return knowledge["canal water schedule"]
    if any(word in text for word in ["shortage", "complaint", "report water", "water problem"]):
        return knowledge["water shortage complaint"]
    if any(word in text for word in ["law", "regulation", "rules", "irrigation law", "policy"]):
        return knowledge["irrigation laws"]
    if any(word in text for word in ["nearest office", "office address", "office location", "nearest irrigation"]):
        return knowledge["nearest irrigation office"]
    if any(word in text for word in ["availability", "water available"]):
        return knowledge["water availability"]
    if any(word in text for word in ["department policy", "procedure", "policies", "procedures"]):
        return knowledge["department policies"]
    if any(word in text for word in ["report template", "report format", "template", "report form"]):
        return knowledge["report templates"]
    if any(word in text for word in ["officer", "officers"]):
        return knowledge["officer job"]
    if "irrigation" in text:
        return knowledge["what is irrigation"]
    if any(word in text for word in ["education", "study", "degree"]):
        return knowledge["what education is needed"]
    if any(word in text for word in ["duty", "duties", "responsibility", "responsibilities"]):
        return knowledge["what are your duties"]
    return None


@app.route("/")
def home():
    return render_template("index.html", initial_message=initial_message)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"reply": "Please type your question."})

    answer = find_answer(question)
    if answer:
        reply = f"{answer} {follow_up}"
    else:
        reply = fallback

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
