from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

knowledge = {
    "father job": "My father is an irrigation department officer. He helps farmers get water for crops.",
    "father does": "He organizes canal water and visits fields to check water flow.",
    "father work": "He works with canal systems, water distribution, and farmer water needs.",
    "irrigation officer": "An irrigation officer manages water distribution and canal maintenance for farms.",
    "father profession": "He serves in the irrigation department and supports farmers with water.",
    "tell father work": "He plans irrigation, fixes canals, and helps farmers get water on time.",
    "father department": "He works in the irrigation department that manages farm water supply.",
    "government officer": "Yes, he is a government irrigation officer who works for public water services.",
    "father rank": "His rank is part of the irrigation department structure and field management.",
    "father responsibilities": "He checks canals, plans water schedules, and helps resolve water problems.",
    "work with farmers": "Yes, he works closely with farmers to deliver water to their fields.",
    "irrigation officer work": "He watches canals, measures water, and keeps water flowing to farms.",
    "helps people": "He helps farmers by making sure their crops get the right water at the right time.",
    "officer role": "The officer manages water, maintains canals, and supports farming communities.",
    "daily routine": "He visits canals, checks water flow, writes reports, and solves water issues.",
    "visits canals": "Yes, he visits canals often to inspect water flow and canal condition.",
    "tools used": "He uses measuring tools, gates, maps, and field notes for canal work.",
    "education background": "He studied water management, engineering, or irrigation techniques for this job.",
    "aapke walid": "Mere walid irrigation department ke officer hain aur kisanon ki madad karte hain.",
    "aapke abu": "Mere abu pani aur canal ka kaam dekhte hain aur kisanon ko support karte hain.",
    "father ka department": "Mere father irrigation department mein kaam karte hain jo paani ka intazam karta hai.",
    "father irrigation": "Haan, mere father irrigation officer hain jo zameen ko paani pohanchate hain.",
    "father ka kaam": "Mere father paani aur canal ka kaam sambhalte hain aur kisanon ki madad karte hain.",
    "officer ka role": "Officer ka kaam irrigation, canal maintenance, aur kisanon ko paani dena hai.",
    "government officer bante": "Government officer banne ke liye exam dena padta hai aur training leni hoti hai.",
    "what is irrigation": "Irrigation means giving water to crops so they can grow well.",
    "why irrigation important": "Irrigation is important because crops need water to grow and farmers need good harvests.",
    "types of irrigation": "There are many types like canal, drip, sprinkler, surface, and basin irrigation.",
    "drip irrigation": "Drip irrigation gives water slowly to plant roots through pipes and saves water.",
    "flood irrigation": "Flood irrigation covers the field with water and lets it soak into the soil.",
    "sprinkler irrigation": "Sprinkler irrigation sprays water like rain over the crops.",
    "canal irrigation": "Canal irrigation brings water through canals from rivers to the fields.",
    "surface irrigation": "Surface irrigation lets water flow over the land and soak into the soil.",
    "subsurface irrigation": "Subsurface irrigation sends water under the soil surface to reach roots.",
    "farmers need irrigation": "Farmers need irrigation because rain is not always enough for crops.",
    "irrigation help crops": "Irrigation keeps soil moist so crops can grow healthy and strong.",
    "no irrigation": "Without irrigation, crops may dry out and farmers may lose their yield.",
    "irrigation first used": "Irrigation has been used for many centuries to grow crops in dry areas.",
    "irrigation pakistan": "Yes, irrigation is used widely in Pakistan for farms and canals.",
    "furrow irrigation": "Furrow irrigation waters crops in small channels between plant rows.",
    "basin irrigation": "Basin irrigation floods a flat field area and lets the water soak into the soil.",
    "micro irrigation": "Micro irrigation uses small drips or low sprays to save water and feed plants.",
    "irrigation role farming": "Irrigation gives water to farms so they can grow food and earn income.",
    "water reach farms": "Water reaches farms through canals, pipes, and field channels from the river.",
    "irrigation kya": "Irrigation fasal ko paani dena hai taake zameen gulzar rahe.",
    "irrigation pakistan hoti": "Haan, Pakistan mein irrigation canals aur tube wells se paani milta hai.",
    "canal kaam": "Canal paani ko kheton tak le jata hai aur zameen ko tar karta hai.",
    "drip irrigation kya": "Drip irrigation paani ko dheere dheere paudon ke naso tak pohanchata hai.",
    "sprinkler kise": "Sprinkler paani ko chhidakta hai jese barish hoti hai.",
    "fasal paani kyu": "Fasal ko paani chahiye taake wo theek tarah se barhe aur fal dein.",
    "what is a canal": "A canal is a man-made water channel that carries water to farms.",
    "how are canals built": "Canals are built by digging channels and making banks to guide the water.",
    "purpose of canal": "The purpose of a canal is to move river water to fields for irrigation.",
    "water distributed canal": "Water is distributed through canal gates and smaller channels to farms.",
    "canal water schedule": "A canal water schedule tells farmers when their fields will get water.",
    "find water schedule": "Ask the local irrigation office or check the canal schedule notice for your area.",
    "when water come": "Water will come based on the canal schedule and rotation from the office.",
    "warabandi": "Warabandi is the fixed schedule of water supply to farms in rotation.",
    "warabandi decided": "Warabandi is decided by the irrigation office and local water users groups.",
    "canal role": "A canal moves water from the river to farms and helps irrigate the fields.",
    "canal maintenance": "Canal maintenance means cleaning, repairing banks, and keeping gates working.",
    "who cleans canals": "Canal workers and irrigation staff clean canals and remove blockages.",
    "distributary canal": "A distributary canal is a small branch that takes water to local fields.",
    "main canal": "A main canal carries a large amount of river water to many branch canals.",
    "branch canal": "A branch canal carries water from the main canal to smaller outlets.",
    "measure water flow": "Water flow is measured using gauges, weirs, or flow meters in the canal.",
    "headworks": "Headworks are the structures at the river to take water into canals.",
    "regulator canal": "A regulator is a gate that controls water flow and level in the canal.",
    "canal drought": "A canal helps in drought by delivering available water carefully to the farms.",
    "pani schedule": "Canal water schedule aur time table ese milte hain jo aapko paani ka waqt batate hain.",
    "warabandi kya": "Warabandi paani ka ek tareeqa hai jisme har kisan ko nirdharit waqt milta hai.",
    "canal saaf": "Canal saaf canal se paani ki supply ke liye zaruri hota hai.",
    "time table kahan": "Paani ka time table irrigation office ya local patwari se mil sakta hai.",
    "meri zamin par": "Aapki zamin par paani us schedule ke mutabiq ayega jo canal office deta hai.",
    "canal kitni": "Canal kay kayi tarah hotay hain jaise main canal, distributary, branch aur watercourse.",
    "report water shortage": "Report water shortage to the local irrigation office with details of your field and canal.",
    "complain supply": "You can complain at the irrigation office or through the helpline about no water.",
    "water does not": "If water does not come, tell the canal patwari or officer immediately.",
    "contact irrigation office": "Visit or call your nearest irrigation office to report water issues.",
    "talk water problems": "Talk to the canal patwari, assistant, or irrigation officer about water problems.",
    "complaint process": "Submit a written or verbal complaint at the office and ask for a reference number.",
    "file complaint online": "Some offices may allow online complaints if they have a website or hotline.",
    "resolve water complaint": "It can take a few days based on the problem and the local office response.",
    "after submit complaint": "After you submit, the office will check the canal and try to fix the problem.",
    "call helpline": "Yes, you can call the irrigation helpline if your area has one.",
    "canal blocked": "If the canal is blocked, report it so workers can clear the blockage.",
    "stealing water": "If someone steals water, report it to the officer and the office may act.",
    "illegal water usage": "Report illegal water use to the irrigation office or local water committee.",
    "penalty water theft": "Yes, water theft can lead to fines or penalties by the irrigation department.",
    "farmer rights": "Farmers have rights to receive their water share fairly and to file complaints.",
    "emergency water": "You can request emergency water if your crop is in danger and the office may help.",
    "documents complaint": "Bring your name, land details, and any water allocation papers when filing a complaint.",
    "who investigates": "Local irrigation officers or patwaris investigate water shortage complaints.",
    "officer visit": "Yes, an officer may visit your farm to check the canal and water issue.",
    "paani nahi kya": "Agar paani nahi aa raha, office ko batayein aur shikayat darj karain.",
    "water shortage kahan": "Water shortage ki shikayat nearest irrigation office ya canal patwari se karein.",
    "canal band": "Canal band hone ki shikayat officer ko karein taake wo deekh sake.",
    "paani chori": "Paani chori report karne ke liye local officer ya water user group ko batayein.",
    "complaint darj": "Shikayat darj karne ke liye office mein likhit ya verbal request dein.",
    "meri shikayat": "Shikayat hal hone mein kuch din lag sakte hain, magar office aapko jawab dega.",
    "department help farmers": "The irrigation department helps farmers with water supply, scheduling, and canal repair.",
    "services for farmers": "The department provides water delivery, complaints support, and farming advice.",
    "free water": "Water is usually shared by schedule, not fully free, but farmers get their fair share.",
    "water allocated": "Water is allocated based on land size, crop need, and canal schedule.",
    "role farmers": "Farmers help water conservation by using it carefully and keeping channels clear.",
    "farmers save water": "Farmers can save water by using drip, timed irrigation, and fixing leaks.",
    "crops canal water": "Wheat, cotton, sugarcane, and rice grow well with canal water if shared properly.",
    "irrigate wheat": "Farmers should irrigate wheat at key growth stages like tillering and grain filling.",
    "irrigate rice": "Rice needs water during transplanting and a shallow flood during growth.",
    "water availability yield": "Better water availability usually gives better crop yield and healthy plants.",
    "best time irrigate": "The best time is early morning or late evening when water is used well.",
    "wheat water need": "Wheat needs moderate water at growth stages and less near harvest.",
    "cotton water need": "Cotton needs steady water after sowing and during flowering.",
    "sugarcane water": "Sugarcane needs a lot of water and regular supply over many months.",
    "expand water share": "Farmers cannot usually expand their water share without official approval.",
    "small farmers rights": "Small farmers get water rights based on their land and local water rules.",
    "water user association": "A water user association is a farmer group that helps manage local water use.",
    "coordinate water sharing": "Farmers coordinate with each other and the office for fair water distribution.",
    "training available": "Some irrigation offices offer training on water use and conservation.",
    "drought farmers": "During drought, farmers face less water and need to save water carefully.",
    "kisan paani": "Kisan paani canal schedule aur irrigation office se hasil karte hain.",
    "kisaan help": "Irrigation department kisanon ko paani aur canal problem solve karne mein help karta hai.",
    "wheat kitna": "Wheat ke liye paani zaruri hai lekin zyada paani sehmat nahi.",
    "cotton paani kab": "Cotton ko phool aur phal ke dauran paani dena chahiye.",
    "kisan paani bachaye": "Kisan paani bachane ke liye drip ya sahi waqt par paani den.",
    "what is irrigation department": "The irrigation department manages canals, water delivery, and farm irrigation systems.",
    "function irrigation department": "Its function is to provide water, maintain canals, and support farmers.",
    "ministry controls": "Provincial irrigation departments are usually controlled by the provincial water ministry.",
    "main offices": "The main offices include regional, divisional, and local irrigation offices.",
    "divisions irrigation": "The irrigation department is divided into zones, circles, divisions, and subdivisions.",
    "sub division irrigation": "A Sub-Division is a local area office that manages nearby canals and water supply.",
    "division irrigation": "A Division oversees several subdivisions and larger irrigation work.",
    "circle irrigation": "A Circle is an administrative area under a division for water management.",
    "zone irrigation": "A Zone groups several circles or divisions for broad irrigation planning.",
    "head irrigation": "The head of the irrigation department is usually a senior engineer or director.",
    "sub engineer role": "A Sub-Engineer helps supervise canal works and field water management.",
    "sdo role": "An SDO manages a subdivision and handles water distribution and complaints.",
    "xen role": "An XEN oversees large irrigation works and supervises engineers and maintenance.",
    "se role": "A SE (Superintending Engineer) manages major projects and technical planning.",
    "ce irrigation": "A CE (Chief Engineer) leads the irrigation department and makes major decisions.",
    "documents issue": "The department issues water permits, supply letters, and complaint records.",
    "contact irrigation": "Contact the local irrigation office by phone, visit, or through their website if available.",
    "provincial federal": "Irrigation is usually a provincial body, but some water issues involve federal agreements.",
    "department website": "If the department has a website, it may show contact details and services.",
    "irrigation kaam": "Irrigation department ka kaam paani ko kheton tak pohanchana hai.",
    "officers hote": "Department mein patwari, sub engineer, SDO, XEN aur CE jaise officers hote hain.",
    "xen irrigation kaun": "XEN ek senior engineer hota hai jo irrigation projects aur canals ko manage karta hai.",
    "sdo kya": "SDO subdivision ka head hota hai jo local paani aur canal kaam dekhta hai.",
    "sub engineer role": "Sub Engineer field mein canal repair aur paani distribution ka kaam karta hai.",
    "ce irrigation karta": "CE irrigation plan banata hai aur department ke monthly aur yearly kaam dekhta hai.",
    "irrigation laws pakistan": "There are laws for water use, canal management, and farmer rights in Pakistan.",
    "canal drainage act": "The Canal and Drainage Act is a law for canals, drainage, and farming water use.",
    "farmer water rights": "Farmers have rights to receive water and to complain if supply is unfair.",
    "cut water supply": "The department can cut water for repair, shortage, or rule violations.",
    "penalty damaging canal": "Damaging a canal can lead to fines or repair charges under department rules.",
    "punishment water theft": "Water theft can be punished with fines or legal action by the irrigation department.",
    "environmental regulations": "There are rules to protect canals, water quality, and land from misuse.",
    "water permit": "A water permit is permission to use irrigation water for a farm or project.",
    "get water permit": "You can get a water permit by applying to the irrigation office with your land papers.",
    "documents water permit": "You need land documents, ID, and farm details to apply for a water permit.",
    "water usage regulated": "Water usage is regulated by schedules, permits, and the irrigation office.",
    "water accord": "The Water Accord is an agreement on water sharing between provinces in Pakistan.",
    "indus waters treaty": "The Indus Waters Treaty is a river water agreement between Pakistan and India.",
    "water allocation provinces": "Water allocation between provinces is decided by IRSA and government agreements.",
    "irsa": "IRSA is the Indus River System Authority that manages river water sharing.",
    "irsa stands for": "IRSA stands for Indus River System Authority.",
    "irsa role": "IRSA decides water allocation and manages river water for provinces.",
    "groundwater laws": "Yes, there are laws for groundwater use to protect water resources.",
    "break irrigation rules": "If a farmer breaks irrigation rules, the department may warn or penalize them.",
    "appeal water decision": "A farmer can appeal a water decision through the local irrigation office.",
    "irrigation laws kya": "Pakistan mein irrigation laws canal aur paani istimal ko qanooni tor par hak dete hain.",
    "canal drainage kya": "Canal and Drainage Act canal aur zameen ki paani nikalne ki qanoon hai.",
    "paani churane saza": "Paani churane par fine ya saza mil sakti hai according to irrigation rules.",
    "water permit kaise": "Water permit ke liye office mein darkhwast dein aur zaroori documents dikhayen.",
    "irsa kya": "IRSA Indus River System Authority hai jo paani ka taqseem tay karti hai.",
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

    if any(word in text for word in ["father", "profession", "job", "work", "officer", "walid", "abu", "father ka", "walid ka", "abu ka"]):
        return knowledge["father profession"]
    if any(word in text for word in ["farmer", "farmers", "help", "support", "kisan", "kisanon", "fasal", "kisanon ko"]):
        return knowledge["how do you help farmers"]
    if any(word in text for word in ["schedule", "canal water", "water schedule", "availability", "warabandi", "time table", "paani ka time", "pani ka time", "paanee schedule"]):
        return knowledge["canal water schedule"]
    if any(word in text for word in ["shortage", "complaint", "report water", "water problem", "shikayat", "paani nahi", "paani nahi aa raha", "paanee chori", "water theft", "paani chori"]):
        return knowledge["water shortage complaint"]
    if any(word in text for word in ["law", "regulation", "rules", "irrigation law", "policy", "saza", "niyam", "qanun", "kaanoon", "qanoon"]):
        return knowledge["irrigation laws"]
    if any(word in text for word in ["nearest office", "office address", "office location", "nearest irrigation", "contact", "rabta", "patwari", "nazar"]):
        return knowledge["nearest irrigation office"]
    if any(word in text for word in ["availability", "water available", "paani available", "paanee available"]):
        return knowledge["water availability"]
    if any(word in text for word in ["department policy", "procedure", "policies", "procedures", "department", "irrigation department", "department ka", "department mein"]):
        return knowledge["department policies"]
    if any(word in text for word in ["report template", "report format", "template", "report form", "report", "forma"]):
        return knowledge["report templates"]
    if any(word in text for word in ["officer", "officers", "sub engineer", "xen", "sdo", "se", "ce", "subdivision", "division", "circle", "zone"]):
        return knowledge["officer job"]
    if "irrigation" in text or any(word in text for word in ["pani", "pani", "paanee", "irrigation kya", "irrigation hota"]):
        return knowledge["what is irrigation"]
    if any(word in text for word in ["education", "study", "degree", "background"]):
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
