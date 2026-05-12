"""
HomeStock AI — Flask Backend
Toda la lógica de negocio e IA en Python.
El frontend HTML/JS solo hace llamadas a esta API.
"""

from flask import Flask, jsonify, request, render_template
from datetime import datetime, date
import json, os, uuid, math

app = Flask(__name__)

# ── Persistencia ────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

CATEGORIES = ["Cocina", "Uso personal", "Aseo", "Bebeca"]
UNIT_TYPE   = {"ml":"liquid","l":"liquid","g":"solid","kg":"solid",
               "und":"count","pastillas":"count"}

SEED_PRODUCTS = [
    {"id":"p1","name":"Azúcar","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s1a","qty":1000,"opened":"2025-09-02","closed":"2025-11-07","price":None},
        {"id":"s1b","qty":1000,"opened":"2025-11-07","closed":"2025-12-12","price":None},
        {"id":"s1c","qty":1000,"opened":"2026-02-06","closed":None,"price":None},
    ]},
    {"id":"p2","name":"Leche","category":"Cocina","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s2a","qty":7800,"opened":"2025-09-08","closed":"2025-09-22","price":None},
        {"id":"s2b","qty":7800,"opened":"2025-09-22","closed":"2025-10-04","price":None},
        {"id":"s2c","qty":7800,"opened":"2025-10-04","closed":"2025-10-19","price":None},
        {"id":"s2d","qty":7800,"opened":"2025-10-20","closed":"2025-11-04","price":None},
        {"id":"s2e","qty":7800,"opened":"2025-11-04","closed":"2025-12-04","price":None},
        {"id":"s2f","qty":6000,"opened":"2026-01-11","closed":None,"price":None},
    ]},
    {"id":"p3","name":"Sal","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s3a","qty":547,"opened":"2025-09-09","closed":"2025-11-30","price":None},
        {"id":"s3b","qty":1000,"opened":"2025-11-15","closed":None,"price":None},
    ]},
    {"id":"p4","name":"Café","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s4a","qty":250,"opened":"2025-08-25","closed":"2025-09-02","price":None},
        {"id":"s4b","qty":500,"opened":"2025-09-03","closed":"2025-09-15","price":None},
        {"id":"s4c","qty":250,"opened":"2025-09-15","closed":"2025-09-22","price":None},
        {"id":"s4d","qty":500,"opened":"2025-09-22","closed":"2025-10-05","price":None},
        {"id":"s4e","qty":500,"opened":"2025-10-06","closed":"2025-10-20","price":None},
        {"id":"s4f","qty":500,"opened":"2025-10-21","closed":"2025-11-13","price":None},
        {"id":"s4g","qty":220,"opened":"2025-11-13","closed":"2025-11-23","price":None},
        {"id":"s4h","qty":250,"opened":"2025-11-24","closed":"2025-12-04","price":None},
        {"id":"s4i","qty":500,"opened":"2026-01-10","closed":None,"price":None},
    ]},
    {"id":"p5","name":"Huevos","category":"Cocina","unit":"und","dailyRate":None,"price":None,"entries":[
        {"id":"s5a","qty":30,"opened":"2025-09-01","closed":"2025-09-08","price":None},
        {"id":"s5b","qty":30,"opened":"2025-09-09","closed":"2025-09-23","price":None},
        {"id":"s5c","qty":12,"opened":"2025-09-24","closed":"2025-09-26","price":None},
        {"id":"s5d","qty":30,"opened":"2025-09-26","closed":"2025-10-03","price":None},
        {"id":"s5e","qty":30,"opened":"2025-10-03","closed":"2025-10-11","price":None},
        {"id":"s5f","qty":15,"opened":"2025-10-12","closed":"2025-10-16","price":None},
        {"id":"s5g","qty":30,"opened":"2025-10-17","closed":"2025-10-26","price":None},
        {"id":"s5h","qty":6, "opened":"2025-10-26","closed":"2025-10-28","price":None},
        {"id":"s5i","qty":30,"opened":"2025-10-28","closed":None,"price":None},
    ]},
    {"id":"p6","name":"Harina de maíz","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s6a","qty":1000,"opened":"2025-08-15","closed":"2025-09-23","price":None},
        {"id":"s6b","qty":1000,"opened":"2025-10-13","closed":"2025-11-25","price":None},
    ]},
    {"id":"p7","name":"Chocolate","category":"Cocina","unit":"pastillas","dailyRate":None,"price":None,"entries":[
        {"id":"s7a","qty":18,"opened":"2025-09-09","closed":"2025-09-26","price":None},
        {"id":"s7b","qty":18,"opened":"2025-10-01","closed":"2025-11-01","price":None},
        {"id":"s7c","qty":18,"opened":"2025-11-15","closed":None,"price":None},
    ]},
    {"id":"p8","name":"Avena","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s8a","qty":500,"opened":"2025-09-01","closed":"2025-10-15","price":None},
        {"id":"s8b","qty":500,"opened":"2025-10-16","closed":"2025-11-30","price":None},
        {"id":"s8c","qty":500,"opened":"2025-12-01","closed":"2026-01-20","price":None},
        {"id":"s8d","qty":500,"opened":"2026-01-21","closed":None,"price":None},
    ]},
    {"id":"p9","name":"Arroz","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s9a","qty":2000,"opened":"2025-09-01","closed":"2025-10-25","price":None},
        {"id":"s9b","qty":2000,"opened":"2025-10-26","closed":None,"price":None},
    ]},
    {"id":"p10","name":"Cereal","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s10a","qty":700,"opened":"2025-10-01","closed":"2025-11-04","price":None},
        {"id":"s10b","qty":700,"opened":"2025-11-05","closed":None,"price":None},
    ]},
    {"id":"p11","name":"Harina para pancakes","category":"Cocina","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s11a","qty":454,"opened":"2025-09-15","closed":"2025-11-05","price":None},
        {"id":"s11b","qty":454,"opened":"2025-11-06","closed":None,"price":None},
    ]},
    {"id":"p12","name":"Crema para peinar","category":"Uso personal","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s12a","qty":300,"opened":"2025-09-01","closed":"2025-11-10","price":None},
        {"id":"s12b","qty":300,"opened":"2025-11-10","closed":None,"price":None},
    ]},
    {"id":"p13","name":"Jabón de manos","category":"Uso personal","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s13a","qty":270,"opened":"2025-09-12","closed":"2025-11-17","price":None},
        {"id":"s13b","qty":270,"opened":"2025-11-17","closed":None,"price":None},
    ]},
    {"id":"p14","name":"Crema dental","category":"Uso personal","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s14a","qty":75,"opened":"2025-09-09","closed":"2025-09-30","price":None},
        {"id":"s14b","qty":75,"opened":"2025-09-30","closed":"2025-10-21","price":None},
        {"id":"s14c","qty":75,"opened":"2025-10-22","closed":"2025-11-15","price":None},
        {"id":"s14d","qty":75,"opened":"2025-11-16","closed":"2025-12-08","price":None},
        {"id":"s14e","qty":75,"opened":"2025-12-08","closed":None,"price":None},
    ]},
    {"id":"p15","name":"Desodorante","category":"Uso personal","unit":"g","dailyRate":None,"price":None,"entries":[
        {"id":"s15a","qty":30,"opened":"2025-09-10","closed":None,"price":None},
    ]},
    {"id":"p16","name":"Protectores diarios","category":"Uso personal","unit":"und","dailyRate":None,"price":None,"entries":[
        {"id":"s16a","qty":60, "opened":"2025-09-10","closed":"2025-10-05","price":None},
        {"id":"s16b","qty":180,"opened":"2025-10-12","closed":None,"price":None},
    ]},
    {"id":"p17","name":"Jabón para loza","category":"Aseo","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s17a","qty":3750,"opened":"2025-08-15","closed":"2026-01-19","price":None},
        {"id":"s17b","qty":3800,"opened":"2026-01-21","closed":None,"price":None},
    ]},
    {"id":"p18","name":"Desengrasante D1","category":"Aseo","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s18a","qty":7800,"opened":"2025-07-26","closed":"2025-08-19","price":None},
        {"id":"s18b","qty":7800,"opened":"2025-08-26","closed":"2025-10-17","price":None},
        {"id":"s18c","qty":7800,"opened":"2025-10-21","closed":"2025-12-05","price":None},
    ]},
    {"id":"p19","name":"Suavizante de ropa","category":"Aseo","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s19a","qty":3750,"opened":"2025-11-11","closed":None,"price":None},
    ]},
    {"id":"p20","name":"Pañales","category":"Bebeca","unit":"und","dailyRate":None,"price":None,"entries":[
        {"id":"s20a","qty":96,"opened":"2025-08-17","closed":"2025-09-08","price":None},
        {"id":"s20b","qty":96,"opened":"2025-09-08","closed":"2025-10-01","price":None},
        {"id":"s20c","qty":96,"opened":"2025-10-01","closed":"2025-10-23","price":None},
        {"id":"s20d","qty":96,"opened":"2025-10-23","closed":"2025-11-13","price":None},
        {"id":"s20e","qty":96,"opened":"2025-11-13","closed":"2025-12-05","price":None},
        {"id":"s20f","qty":96,"opened":"2025-12-05","closed":None,"price":None},
    ]},
    {"id":"p21","name":"Shampoo bebé","category":"Bebeca","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s21a","qty":400,"opened":"2025-08-17","closed":"2025-11-28","price":None},
        {"id":"s21b","qty":400,"opened":"2025-11-28","closed":None,"price":None},
    ]},
    {"id":"p22","name":"Colonia bebé","category":"Bebeca","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s22a","qty":120,"opened":"2024-09-19","closed":"2025-09-04","price":None},
    ]},
    {"id":"p23","name":"Crema para cuerpo bebé","category":"Bebeca","unit":"ml","dailyRate":None,"price":None,"entries":[
        {"id":"s23a","qty":400,"opened":"2025-09-06","closed":"2025-11-05","price":None},
        {"id":"s23b","qty":220,"opened":"2025-11-06","closed":"2025-12-08","price":None},
        {"id":"s23c","qty":440,"opened":"2025-12-09","closed":None,"price":None},
    ]},
]

# ── Persistencia ────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    data = {"products": SEED_PRODUCTS, "mercadoHistory": []}
    save_data(data)
    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Lógica de IA / predicción ───────────────────────────────────
def parse_date(s):
    """Convierte string YYYY-MM-DD a date, o None."""
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except Exception:
        return None

def recalc_rate(product):
    """
    Calcula la tasa diaria promedio basada en entradas cerradas.
    Si n >= 5, aplica suavizamiento exponencial (ETS simple).
    Si n < 5, usa promedio simple.
    Retorna float o None.
    """
    done = [e for e in product["entries"] if e.get("opened") and e.get("closed")]
    if not done:
        return product.get("dailyRate")

    rates = []
    for e in done:
        d_open  = parse_date(e["opened"])
        d_close = parse_date(e["closed"])
        if d_open and d_close:
            days = (d_close - d_open).days
            if days > 0:
                rates.append(e["qty"] / days)

    if not rates:
        return product.get("dailyRate")

    if len(rates) >= 5:
        # ETS simple: alpha = 0.3 — más peso a entradas recientes
        alpha = 0.3
        smoothed = rates[0]
        for r in rates[1:]:
            smoothed = alpha * r + (1 - alpha) * smoothed
        return round(smoothed, 4)
    else:
        return round(sum(rates) / len(rates), 4)

def get_last_open(product):
    """Retorna la entrada abierta más reciente (sin closed), o None."""
    open_entries = [e for e in product["entries"] if e.get("opened") and not e.get("closed")]
    if not open_entries:
        return None
    return sorted(open_entries, key=lambda e: e["opened"], reverse=True)[0]

def get_days_left(product):
    """
    Días estimados hasta agotamiento basados en la tasa de consumo.
    Retorna float o None.
    """
    rate = recalc_rate(product)
    if not rate:
        return None
    last = get_last_open(product)
    if not last:
        return None
    d_open = parse_date(last["opened"])
    if not d_open:
        return None
    days_used = (date.today() - d_open).days
    remaining = last["qty"] - (rate * days_used)
    return max(0.0, remaining / rate)

def get_status(days_left):
    if days_left is None:
        return "unknown"
    if days_left <= 3:
        return "critical"
    if days_left <= 7:
        return "warning"
    return "ok"

def enrich_product(p):
    """Agrega campos calculados a un producto para enviar al frontend."""
    rate      = recalc_rate(p)
    days_left = get_days_left(p)
    last      = get_last_open(p)
    return {
        **p,
        "_rate":     rate,
        "_daysLeft": round(days_left, 1) if days_left is not None else None,
        "_status":   get_status(days_left),
        "_hasOpen":  last is not None,
    }

def monthly_qty(product, year, month):
    """
    Cantidad consumida estimada en un mes dado, prorrateada por días de solapamiento.
    Usado para gráficas de consumo mensual.
    """
    from calendar import monthrange
    m_start = date(year, month, 1)
    m_end   = date(year, month, monthrange(year, month)[1])
    total   = 0.0
    for e in product["entries"]:
        if not e.get("opened"):
            continue
        e_start = parse_date(e["opened"])
        e_end   = parse_date(e["closed"]) if e.get("closed") else date.today()
        if not e_start or not e_end:
            continue
        total_days = (e_end - e_start).days or 1
        rate_e     = e["qty"] / total_days
        overlap_s  = max(e_start, m_start)
        overlap_e  = min(e_end, m_end)
        overlap_d  = (overlap_e - overlap_s).days
        if overlap_d > 0:
            total += rate_e * overlap_d
    return round(total, 1)

def get_month_range(products):
    """Retorna lista de (year, month) desde el primer registro hasta hoy."""
    all_dates = []
    for p in products:
        for e in p["entries"]:
            d = parse_date(e.get("opened"))
            if d:
                all_dates.append(d)
    if not all_dates:
        return []
    start = min(all_dates)
    end   = date.today()
    months = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months

# ── Rutas ────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# GET todos los productos (enriquecidos con campos calculados)
@app.route("/api/products", methods=["GET"])
def get_products():
    data = load_data()
    return jsonify([enrich_product(p) for p in data["products"]])

# POST nuevo producto
@app.route("/api/products", methods=["POST"])
def create_product():
    data = load_data()
    body = request.get_json()
    new_product = {
        "id":       "p" + uuid.uuid4().hex[:8],
        "name":     body["name"],
        "category": body["category"],
        "unit":     body["unit"],
        "dailyRate":body.get("dailyRate"),
        "price":    body.get("price"),
        "entries":  [],
    }
    data["products"].append(new_product)
    save_data(data)
    return jsonify(enrich_product(new_product)), 201

# PUT editar producto
@app.route("/api/products/<pid>", methods=["PUT"])
def update_product(pid):
    data = load_data()
    p = next((x for x in data["products"] if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "No encontrado"}), 404
    body = request.get_json()
    for field in ("name", "category", "unit", "dailyRate", "price"):
        if field in body:
            p[field] = body[field]
    save_data(data)
    return jsonify(enrich_product(p))

# DELETE producto
@app.route("/api/products/<pid>", methods=["DELETE"])
def delete_product(pid):
    data = load_data()
    data["products"] = [x for x in data["products"] if x["id"] != pid]
    save_data(data)
    return jsonify({"ok": True})

# POST nueva entrada a un producto
@app.route("/api/products/<pid>/entries", methods=["POST"])
def add_entry(pid):
    data = load_data()
    p = next((x for x in data["products"] if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "No encontrado"}), 404
    body = request.get_json()
    # Cierra la entrada abierta anterior si existe
    for e in p["entries"]:
        if e.get("opened") and not e.get("closed"):
            e["closed"] = body.get("opened") or date.today().isoformat()
    entry = {
        "id":     "e" + uuid.uuid4().hex[:8],
        "qty":    float(body["qty"]),
        "opened": body.get("opened"),
        "closed": body.get("closed") or None,
        "price":  body.get("price"),
    }
    p["entries"].append(entry)
    if entry.get("price"):
        p["price"] = entry["price"]
    save_data(data)
    return jsonify(enrich_product(p)), 201

# DELETE una entrada específica
@app.route("/api/products/<pid>/entries/<eid>", methods=["DELETE"])
def delete_entry(pid, eid):
    data = load_data()
    p = next((x for x in data["products"] if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "No encontrado"}), 404
    p["entries"] = [e for e in p["entries"] if e["id"] != eid]
    save_data(data)
    return jsonify(enrich_product(p))

# PATCH cerrar entrada abierta (Terminé esto)
@app.route("/api/products/<pid>/close", methods=["PATCH"])
def close_product(pid):
    data = load_data()
    p = next((x for x in data["products"] if x["id"] == pid), None)
    if not p:
        return jsonify({"error": "No encontrado"}), 404
    body    = request.get_json()
    closed  = body.get("closed") or date.today().isoformat()
    last    = get_last_open(p)
    if last:
        last["closed"] = closed
    save_data(data)
    return jsonify(enrich_product(p))

# POST registrar mercado completo
@app.route("/api/mercado", methods=["POST"])
def register_mercado():
    data = load_data()
    body  = request.get_json()
    items = body.get("items", [])   # [{pid, qty, price}]
    fecha = body.get("date") or date.today().isoformat()
    saved = []
    for item in items:
        p = next((x for x in data["products"] if x["id"] == item["pid"]), None)
        if not p or not item.get("qty"):
            continue
        # Cierra entrada anterior abierta
        for e in p["entries"]:
            if e.get("opened") and not e.get("closed"):
                e["closed"] = fecha
        entry = {
            "id":     "e" + uuid.uuid4().hex[:8],
            "qty":    float(item["qty"]),
            "opened": fecha,
            "closed": None,
            "price":  item.get("price"),
        }
        p["entries"].append(entry)
        if item.get("price"):
            p["price"] = item["price"]
        saved.append(item["pid"])
    data["mercadoHistory"].append({"date": fecha, "items": items})
    save_data(data)
    return jsonify({"ok": True, "saved": saved})

# GET datos para gráficas
@app.route("/api/charts", methods=["GET"])
def get_charts():
    data     = load_data()
    products = data["products"]
    months   = get_month_range(products)

    # Consumo mensual por producto (para el selector)
    monthly = {}
    for p in products:
        if any(e.get("opened") for e in p["entries"]):
            monthly[p["id"]] = {
                "name":   p["name"],
                "unit":   p["unit"],
                "category": p["category"],
                "data":   [monthly_qty(p, y, m) for (y, m) in months],
            }

    # Etiquetas de meses
    month_labels = []
    for (y, m) in months:
        d = date(y, m, 1)
        month_labels.append(d.strftime("%b %y"))

    # Tasa diaria por producto
    rates = []
    for p in products:
        r = recalc_rate(p)
        if r:
            rates.append({
                "id":       p["id"],
                "name":     p["name"],
                "unit":     p["unit"],
                "category": p["category"],
                "unitType": UNIT_TYPE.get(p["unit"], "count"),
                "rate":     round(r, 2),
            })
    rates.sort(key=lambda x: x["rate"], reverse=True)

    # Duración promedio por producto y categoría
    durations = {}
    for p in products:
        done = [e for e in p["entries"] if e.get("opened") and e.get("closed")]
        if not done:
            continue
        avg_days = []
        for e in done:
            d1 = parse_date(e["opened"])
            d2 = parse_date(e["closed"])
            if d1 and d2:
                dd = (d2 - d1).days
                if dd > 0:
                    avg_days.append(dd)
        if avg_days:
            durations[p["id"]] = {
                "name":     p["name"],
                "category": p["category"],
                "avg":      round(sum(avg_days) / len(avg_days)),
                "n":        len(avg_days),
            }

    return jsonify({
        "monthLabels": month_labels,
        "monthly":     monthly,
        "rates":       rates,
        "durations":   durations,
    })

# GET lista de mercado propuesta
@app.route("/api/lista-mercado", methods=["GET"])
def lista_mercado():
    data     = load_data()
    next_days = int(request.args.get("days", 14))
    result   = []
    for p in data["products"]:
        days_left = get_days_left(p)
        rate      = recalc_rate(p)
        last      = get_last_open(p)
        # Productos que se acaban antes del próximo mercado
        if days_left is not None and days_left <= next_days:
            result.append({
                "id":       p["id"],
                "name":     p["name"],
                "category": p["category"],
                "unit":     p["unit"],
                "daysLeft": round(days_left, 1),
                "status":   get_status(days_left),
                "needed":   math.ceil(rate * next_days) if rate else None,
                "price":    p.get("price"),
                "reason":   "ending",
            })
        # Productos con historial pero sin entrada abierta (sin stock)
        elif p["entries"] and not last:
            result.append({
                "id":       p["id"],
                "name":     p["name"],
                "category": p["category"],
                "unit":     p["unit"],
                "daysLeft": None,
                "status":   "nostock",
                "needed":   None,
                "price":    p.get("price"),
                "reason":   "nostock",
            })
    result.sort(key=lambda x: (x["daysLeft"] if x["daysLeft"] is not None else 999))
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
