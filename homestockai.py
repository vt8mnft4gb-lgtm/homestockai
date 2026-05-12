# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
HomeStock AI � convertida de HTML a Python (Flask)
Ejecutar:  pip install flask   (solo la primera vez)
           python homestockai.py
Abrir:     http://localhost:5000
Los datos se guardan en homestockai_data.json (mismo directorio).
"""

import json
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homestockai_data.json")

# ?? Datos iniciales (equivalente al SEED de JS) ?????????????????????????????
SEED = {
    "products": [
        {"id": "p1",  "name": "Az�car",               "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s1a", "qty": 1000, "opened": "2025-09-02", "closed": "2025-11-07", "price": None},
            {"id": "s1b", "qty": 1000, "opened": "2025-11-07", "closed": "2025-12-12", "price": None},
            {"id": "s1c", "qty": 1000, "opened": "2026-02-06", "closed": None,         "price": None},
        ]},
        {"id": "p2",  "name": "Leche",                "category": "Cocina",        "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s2a", "qty": 7800, "opened": "2025-09-08", "closed": "2025-09-22", "price": None},
            {"id": "s2b", "qty": 7800, "opened": "2025-09-22", "closed": "2025-10-04", "price": None},
            {"id": "s2c", "qty": 7800, "opened": "2025-10-04", "closed": "2025-10-19", "price": None},
            {"id": "s2d", "qty": 7800, "opened": "2025-10-20", "closed": "2025-11-04", "price": None},
            {"id": "s2e", "qty": 7800, "opened": "2025-11-04", "closed": "2025-12-04", "price": None},
            {"id": "s2f", "qty": 6000, "opened": "2026-01-11", "closed": None,         "price": None},
        ]},
        {"id": "p3",  "name": "Sal",                  "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s3a", "qty": 547,  "opened": "2025-09-09", "closed": "2025-11-30", "price": None},
            {"id": "s3b", "qty": 1000, "opened": "2025-11-15", "closed": None,         "price": None},
        ]},
        {"id": "p4",  "name": "Caf�",                 "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s4a", "qty": 250,  "opened": "2025-08-25", "closed": "2025-09-02", "price": None},
            {"id": "s4b", "qty": 500,  "opened": "2025-09-03", "closed": "2025-09-15", "price": None},
            {"id": "s4c", "qty": 250,  "opened": "2025-09-15", "closed": "2025-09-22", "price": None},
            {"id": "s4d", "qty": 500,  "opened": "2025-09-22", "closed": "2025-10-05", "price": None},
            {"id": "s4e", "qty": 500,  "opened": "2025-10-06", "closed": "2025-10-20", "price": None},
            {"id": "s4f", "qty": 500,  "opened": "2025-10-21", "closed": "2025-11-13", "price": None},
            {"id": "s4g", "qty": 220,  "opened": "2025-11-13", "closed": "2025-11-23", "price": None},
            {"id": "s4h", "qty": 250,  "opened": "2025-11-24", "closed": "2025-12-04", "price": None},
            {"id": "s4i", "qty": 500,  "opened": "2026-01-10", "closed": None,         "price": None},
        ]},
        {"id": "p5",  "name": "Huevos",               "category": "Cocina",        "unit": "und",       "dailyRate": None, "price": None, "entries": [
            {"id": "s5a", "qty": 30,   "opened": "2025-09-01", "closed": "2025-09-08", "price": None},
            {"id": "s5b", "qty": 30,   "opened": "2025-09-09", "closed": "2025-09-23", "price": None},
            {"id": "s5c", "qty": 12,   "opened": "2025-09-24", "closed": "2025-09-26", "price": None},
            {"id": "s5d", "qty": 30,   "opened": "2025-09-26", "closed": "2025-10-03", "price": None},
            {"id": "s5e", "qty": 30,   "opened": "2025-10-03", "closed": "2025-10-11", "price": None},
            {"id": "s5f", "qty": 15,   "opened": "2025-10-12", "closed": "2025-10-16", "price": None},
            {"id": "s5g", "qty": 30,   "opened": "2025-10-17", "closed": "2025-10-26", "price": None},
            {"id": "s5h", "qty": 6,    "opened": "2025-10-26", "closed": "2025-10-28", "price": None},
            {"id": "s5i", "qty": 30,   "opened": "2025-10-28", "closed": None,         "price": None},
        ]},
        {"id": "p6",  "name": "Harina de ma�z",       "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s6a", "qty": 1000, "opened": "2025-08-15", "closed": "2025-09-23", "price": None},
            {"id": "s6b", "qty": 1000, "opened": "2025-10-13", "closed": "2025-11-25", "price": None},
        ]},
        {"id": "p7",  "name": "Chocolate",            "category": "Cocina",        "unit": "pastillas", "dailyRate": None, "price": None, "entries": [
            {"id": "s7a", "qty": 18,   "opened": "2025-09-09", "closed": "2025-09-26", "price": None},
            {"id": "s7b", "qty": 18,   "opened": "2025-10-01", "closed": "2025-11-01", "price": None},
            {"id": "s7c", "qty": 18,   "opened": "2025-11-15", "closed": None,         "price": None},
        ]},
        {"id": "p8",  "name": "Avena",                "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s8a", "qty": 500,  "opened": "2025-09-01", "closed": "2025-10-15", "price": None},
            {"id": "s8b", "qty": 500,  "opened": "2025-10-16", "closed": "2025-11-30", "price": None},
            {"id": "s8c", "qty": 500,  "opened": "2025-12-01", "closed": "2026-01-20", "price": None},
            {"id": "s8d", "qty": 500,  "opened": "2026-01-21", "closed": None,         "price": None},
        ]},
        {"id": "p9",  "name": "Arroz",                "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s9a", "qty": 2000, "opened": "2025-09-01", "closed": "2025-10-25", "price": None},
            {"id": "s9b", "qty": 2000, "opened": "2025-10-26", "closed": None,         "price": None},
        ]},
        {"id": "p10", "name": "Cereal",               "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s10a","qty": 700,  "opened": "2025-10-01", "closed": "2025-11-04", "price": None},
            {"id": "s10b","qty": 700,  "opened": "2025-11-05", "closed": None,         "price": None},
        ]},
        {"id": "p11", "name": "Harina para pancakes", "category": "Cocina",        "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s11a","qty": 454,  "opened": "2025-09-15", "closed": "2025-11-05", "price": None},
            {"id": "s11b","qty": 454,  "opened": "2025-11-06", "closed": None,         "price": None},
        ]},
        {"id": "p12", "name": "Crema para peinar",    "category": "Uso personal",  "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s12a","qty": 300,  "opened": "2025-09-01", "closed": "2025-11-10", "price": None},
            {"id": "s12b","qty": 300,  "opened": "2025-11-10", "closed": None,         "price": None},
        ]},
        {"id": "p13", "name": "Jab�n de manos",       "category": "Uso personal",  "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s13a","qty": 270,  "opened": "2025-09-12", "closed": "2025-11-17", "price": None},
            {"id": "s13b","qty": 270,  "opened": "2025-11-17", "closed": None,         "price": None},
        ]},
        {"id": "p14", "name": "Crema dental",         "category": "Uso personal",  "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s14a","qty": 75,   "opened": "2025-09-09", "closed": "2025-09-30", "price": None},
            {"id": "s14b","qty": 75,   "opened": "2025-09-30", "closed": "2025-10-21", "price": None},
            {"id": "s14c","qty": 75,   "opened": "2025-10-22", "closed": "2025-11-15", "price": None},
            {"id": "s14d","qty": 75,   "opened": "2025-11-16", "closed": "2025-12-08", "price": None},
            {"id": "s14e","qty": 75,   "opened": "2025-12-08", "closed": None,         "price": None},
        ]},
        {"id": "p15", "name": "Desodorante",          "category": "Uso personal",  "unit": "g",         "dailyRate": None, "price": None, "entries": [
            {"id": "s15a","qty": 30,   "opened": "2025-09-10", "closed": None,         "price": None},
        ]},
        {"id": "p16", "name": "Protectores diarios",  "category": "Uso personal",  "unit": "und",       "dailyRate": None, "price": None, "entries": [
            {"id": "s16a","qty": 60,   "opened": "2025-09-10", "closed": "2025-10-05", "price": None},
            {"id": "s16b","qty": 180,  "opened": "2025-10-12", "closed": None,         "price": None},
        ]},
        {"id": "p17", "name": "Jab�n para loza",      "category": "Aseo",          "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s17a","qty": 3750, "opened": "2025-08-15", "closed": "2026-01-19", "price": None},
            {"id": "s17b","qty": 3800, "opened": "2026-01-21", "closed": None,         "price": None},
        ]},
        {"id": "p18", "name": "Desengrasante D1",     "category": "Aseo",          "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s18a","qty": 7800, "opened": "2025-07-26", "closed": "2025-08-19", "price": None},
            {"id": "s18b","qty": 7800, "opened": "2025-08-26", "closed": "2025-10-17", "price": None},
            {"id": "s18c","qty": 7800, "opened": "2025-10-21", "closed": "2025-12-05", "price": None},
        ]},
        {"id": "p19", "name": "Suavizante de ropa",   "category": "Aseo",          "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s19a","qty": 3750, "opened": "2025-11-11", "closed": None,         "price": None},
        ]},
        {"id": "p20", "name": "Pa�ales",              "category": "Bebeca",        "unit": "und",       "dailyRate": None, "price": None, "entries": [
            {"id": "s20a","qty": 96,   "opened": "2025-08-17", "closed": "2025-09-08", "price": None},
            {"id": "s20b","qty": 96,   "opened": "2025-09-08", "closed": "2025-10-01", "price": None},
            {"id": "s20c","qty": 96,   "opened": "2025-10-01", "closed": "2025-10-23", "price": None},
            {"id": "s20d","qty": 96,   "opened": "2025-10-23", "closed": "2025-11-13", "price": None},
            {"id": "s20e","qty": 96,   "opened": "2025-11-13", "closed": "2025-12-05", "price": None},
            {"id": "s20f","qty": 96,   "opened": "2025-12-05", "closed": None,         "price": None},
        ]},
        {"id": "p21", "name": "Shampoo beb�",         "category": "Bebeca",        "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s21a","qty": 400,  "opened": "2025-08-17", "closed": "2025-11-28", "price": None},
            {"id": "s21b","qty": 400,  "opened": "2025-11-28", "closed": None,         "price": None},
        ]},
        {"id": "p22", "name": "Colonia beb�",         "category": "Bebeca",        "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s22a","qty": 120,  "opened": "2024-09-19", "closed": "2025-09-04", "price": None},
        ]},
        {"id": "p23", "name": "Crema para cuerpo beb�","category": "Bebeca",       "unit": "ml",        "dailyRate": None, "price": None, "entries": [
            {"id": "s23a","qty": 400,  "opened": "2025-09-06", "closed": "2025-11-05", "price": None},
            {"id": "s23b","qty": 220,  "opened": "2025-11-06", "closed": "2025-12-08", "price": None},
            {"id": "s23c","qty": 440,  "opened": "2025-12-09", "closed": None,         "price": None},
        ]},
    ],
    "mercadoHistory": []
}


# ?? Persistencia ?????????????????????????????????????????????????????????????

def load_data():
    """Carga datos desde JSON; si no existe el archivo usa SEED."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as exc:
        print(f"[WARN] No se pudo leer {DATA_FILE}: {exc}")
    data = json.loads(json.dumps(SEED))
    save_data(data)
    return data


def save_data(data):
    """Persiste datos en homestockai_data.json."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ?? Plantilla HTML ????????????????????????????????????????????????????????????
# Es pr�cticamente id�ntica al archivo original; los �nicos cambios son:
#   1. Se inyecta window.__INITIAL_DATA__ desde el servidor (Jinja2).
#   2. loadData() lee esa variable en lugar de localStorage.
#   3. saveData(d) hace POST /api/save adem�s de actualizar la variable en memoria.
#   4. Se eliminan STORAGE_KEY y SEED (ya no son necesarios en el cliente).

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>HomeStock AI</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root {
  --bg:#F5F2ED; --surface:#FFF; --surface2:#EDE9E2;
  --teal:#1A7B6E; --teal-light:#D4EDE9; --teal-dark:#0F5248;
  --amber:#D97706; --amber-light:#FEF3C7;
  --red:#DC2626; --red-light:#FEE2E2;
  --navy:#1C2B3A; --gray:#6B7280; --gray-light:#E5E0D8;
  --text:#1C2B3A; --text-muted:#7C8A96; --border:#E2DDD5;
  --shadow:0 2px 12px rgba(28,43,58,.08); --shadow-lg:0 8px 32px rgba(28,43,58,.16);
  --radius:14px; --radius-sm:8px;
  --sidebar:220px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}

/* ?? SIDEBAR ?? */
.sidebar{position:fixed;left:0;top:0;bottom:0;width:var(--sidebar);background:var(--navy);display:flex;flex-direction:column;z-index:200;transition:transform .25s}
.sidebar-logo{padding:24px 20px 18px;border-bottom:1px solid rgba(255,255,255,.08)}
.sidebar-logo h1{font-family:'DM Serif Display',serif;font-size:21px;color:#fff;letter-spacing:-.5px}
.sidebar-logo span{color:#4DB8AB}
.sidebar-logo p{font-size:11px;color:rgba(255,255,255,.35);margin-top:2px}
.sidebar-nav{padding:14px 10px;flex:1;overflow-y:auto}
.nav-section{font-size:10px;font-weight:600;color:rgba(255,255,255,.3);letter-spacing:1.2px;text-transform:uppercase;padding:0 10px 7px;margin-top:10px}
.nav-item{display:flex;align-items:center;gap:9px;padding:10px 10px;border-radius:var(--radius-sm);color:rgba(255,255,255,.6);font-size:13px;font-weight:400;cursor:pointer;transition:all .15s;margin-bottom:2px;border:none;background:none;width:100%;text-align:left}
.nav-item:hover{background:rgba(255,255,255,.07);color:#fff}
.nav-item.active{background:var(--teal);color:#fff;font-weight:500}
.nav-item svg{width:15px;height:15px;flex-shrink:0}
.cat-badge{margin-left:auto;font-size:10px;padding:2px 7px;border-radius:20px;background:rgba(255,255,255,.1);color:rgba(255,255,255,.5)}
.nav-item.active .cat-badge{background:rgba(255,255,255,.2);color:rgba(255,255,255,.8)}

/* hamburger */
.hamburger{display:none;position:fixed;top:14px;left:14px;z-index:300;width:40px;height:40px;background:var(--navy);border:none;border-radius:10px;cursor:pointer;align-items:center;justify-content:center;color:#fff}
.sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:150;backdrop-filter:blur(2px)}

/* ?? MAIN ?? */
.main{margin-left:var(--sidebar);padding:28px 32px;min-height:100vh}

/* ?? TOPBAR ?? */
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.topbar-title h2{font-family:'DM Serif Display',serif;font-size:26px;letter-spacing:-.5px}
.topbar-title p{font-size:12.5px;color:var(--text-muted);margin-top:2px}
.topbar-actions{display:flex;gap:8px;flex-wrap:wrap}

/* ?? BUTTONS ?? */
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 16px;border-radius:var(--radius-sm);font-size:13px;font-weight:500;cursor:pointer;border:none;transition:all .15s;font-family:inherit}
.btn-primary{background:var(--teal);color:#fff}
.btn-primary:hover{background:var(--teal-dark)}
.btn-secondary{background:var(--surface);color:var(--text);border:1.5px solid var(--border)}
.btn-secondary:hover{background:var(--surface2)}
.btn-danger{background:var(--red-light);color:var(--red)}
.btn-danger:hover{background:#fecaca}
.btn-sm{padding:6px 11px;font-size:12px}

/* ?? ALERT ?? */
.alert-strip{background:var(--amber-light);border:1.5px solid #FCD34D;border-radius:var(--radius);padding:12px 16px;display:flex;align-items:center;gap:10px;margin-bottom:20px}
.alert-strip svg{color:var(--amber);flex-shrink:0;width:18px;height:18px}
.alert-strip p{font-size:12.5px;color:#92400E}
.alert-strip strong{font-weight:600}
.alert-count{margin-left:auto;background:var(--amber);color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px}

/* ?? SUMMARY CARDS ?? */
.summary-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
.summary-card{background:var(--surface);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow);border:1.5px solid var(--border)}
.summary-card .label{font-size:11px;color:var(--text-muted);font-weight:500;letter-spacing:.3px}
.summary-card .value{font-family:'DM Serif Display',serif;font-size:30px;margin:5px 0 2px}
.summary-card .sub{font-size:11px;color:var(--text-muted)}
.summary-card.warning .value{color:var(--amber)}
.summary-card.danger .value{color:var(--red)}
.summary-card.good .value{color:var(--teal)}

/* ?? TOOLBAR ?? */
.toolbar{display:flex;gap:8px;margin-bottom:18px;align-items:center;flex-wrap:wrap}
.search-wrap{position:relative;flex:1;min-width:180px;max-width:320px}
.search-wrap svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--text-muted);width:14px}
.search-input{width:100%;padding:9px 12px 9px 33px;border-radius:var(--radius-sm);border:1.5px solid var(--border);background:var(--surface);font-family:inherit;font-size:13px;color:var(--text);outline:none;transition:border .15s}
.search-input:focus{border-color:var(--teal)}
.filter-tabs{display:flex;gap:5px;flex-wrap:wrap}
.filter-tab{padding:7px 12px;border-radius:var(--radius-sm);font-size:12px;font-weight:500;cursor:pointer;border:1.5px solid var(--border);background:var(--surface);color:var(--text-muted);transition:all .15s}
.filter-tab.active{background:var(--teal);border-color:var(--teal);color:#fff}

/* ?? PRODUCT CARDS ?? */
.products-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.product-card{background:var(--surface);border-radius:var(--radius);border:1.5px solid var(--border);box-shadow:var(--shadow);padding:16px;cursor:pointer;transition:all .15s}
.product-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-1px);border-color:var(--teal)}
.product-card.status-critical{border-left:4px solid var(--red)}
.product-card.status-warning{border-left:4px solid var(--amber)}
.product-card.status-ok{border-left:4px solid var(--teal)}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.card-name{font-weight:600;font-size:14.5px}
.card-cat{font-size:11px;color:var(--text-muted);margin-top:2px}
.status-pill{font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:20px;white-space:nowrap;flex-shrink:0}
.pill-critical{background:var(--red-light);color:var(--red)}
.pill-warning{background:var(--amber-light);color:var(--amber)}
.pill-ok{background:var(--teal-light);color:var(--teal-dark)}
.pill-unknown{background:var(--gray-light);color:var(--gray)}
.progress-wrap{margin:8px 0 5px}
.progress-label{display:flex;justify-content:space-between;font-size:11px;color:var(--text-muted);margin-bottom:4px}
.progress-bar{height:5px;background:var(--gray-light);border-radius:3px;overflow:hidden}
.progress-fill{height:100%;border-radius:3px;transition:width .4s}
.fill-ok{background:var(--teal)}.fill-warning{background:var(--amber)}.fill-critical{background:var(--red)}
.card-stats{display:flex;gap:10px;margin-top:9px}
.stat{font-size:11px;color:var(--text-muted)}
.stat strong{color:var(--text);font-weight:600;display:block;font-size:12.5px}

/* ?? CHARTS VIEW ?? */
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.chart-card{background:var(--surface);border-radius:var(--radius);padding:20px;border:1.5px solid var(--border);box-shadow:var(--shadow)}
.chart-card.full{grid-column:1/-1}
.chart-card h4{font-size:13px;font-weight:600;color:var(--text-muted);letter-spacing:.3px;margin-bottom:14px;text-transform:uppercase}

/* ?? MODAL ?? */
.modal-overlay{position:fixed;inset:0;background:rgba(28,43,58,.5);backdrop-filter:blur(4px);z-index:500;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .2s;padding:16px}
.modal-overlay.open{opacity:1;pointer-events:all}
.modal{background:var(--surface);border-radius:18px;width:100%;max-width:540px;max-height:90vh;overflow-y:auto;box-shadow:var(--shadow-lg);transform:translateY(20px);transition:transform .2s}
.modal-overlay.open .modal{transform:translateY(0)}
.modal-header{padding:22px 24px 0;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:var(--surface);z-index:1}
.modal-header h3{font-family:'DM Serif Display',serif;font-size:20px}
.modal-close{width:30px;height:30px;border-radius:50%;border:none;background:var(--surface2);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--gray);font-size:17px}
.modal-close:hover{background:var(--gray-light)}
.modal-body{padding:18px 24px 24px}

/* ?? PRODUCT PICKER POPUP ?? */
.picker-overlay{position:fixed;inset:0;background:rgba(28,43,58,.5);backdrop-filter:blur(4px);z-index:600;display:flex;align-items:flex-end;justify-content:center;padding:0;opacity:0;pointer-events:none;transition:opacity .2s}
.picker-overlay.open{opacity:1;pointer-events:all}
.picker-sheet{background:var(--surface);border-radius:20px 20px 0 0;width:100%;max-width:600px;max-height:85vh;display:flex;flex-direction:column;transform:translateY(100%);transition:transform .3s cubic-bezier(.4,0,.2,1)}
.picker-overlay.open .picker-sheet{transform:translateY(0)}
.picker-header{padding:16px 20px 0;display:flex;align-items:center;justify-content:space-between}
.picker-header h3{font-family:'DM Serif Display',serif;font-size:19px}
.picker-search-wrap{padding:12px 20px}
.picker-search{width:100%;padding:10px 14px 10px 36px;border-radius:var(--radius-sm);border:1.5px solid var(--border);background:var(--bg);font-family:inherit;font-size:13.5px;outline:none}
.picker-search:focus{border-color:var(--teal)}
.picker-search-icon{position:absolute;left:32px;top:50%;transform:translateY(-50%);width:14px;color:var(--text-muted)}
.picker-search-wrap{position:relative}
.picker-body{overflow-y:auto;flex:1;padding:0 20px 20px}
.picker-cat-label{font-size:11px;font-weight:700;color:var(--text-muted);letter-spacing:1px;text-transform:uppercase;margin:14px 0 7px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.picker-product-btn{display:flex;align-items:center;justify-content:space-between;width:100%;padding:11px 12px;border-radius:var(--radius-sm);border:1.5px solid var(--border);background:var(--surface);font-family:inherit;font-size:13.5px;cursor:pointer;margin-bottom:5px;transition:all .15s;text-align:left}
.picker-product-btn:hover{border-color:var(--teal);background:var(--teal-light)}
.picker-product-btn.selected{border-color:var(--teal);background:var(--teal-light);color:var(--teal-dark)}
.picker-product-meta{font-size:11px;color:var(--text-muted)}
.picker-new-btn{display:flex;align-items:center;gap:8px;width:100%;padding:11px 12px;border-radius:var(--radius-sm);border:1.5px dashed var(--border);background:none;font-family:inherit;font-size:13px;cursor:pointer;color:var(--text-muted);margin-top:10px;transition:all .15s}
.picker-new-btn:hover{border-color:var(--teal);color:var(--teal);background:var(--teal-light)}

/* ?? FORM ?? */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.form-group{display:flex;flex-direction:column;gap:5px}
.form-group.full{grid-column:1/-1}
.form-label{font-size:11.5px;font-weight:600;color:var(--text-muted);letter-spacing:.3px}
.form-input,.form-select{padding:9px 11px;border-radius:var(--radius-sm);border:1.5px solid var(--border);background:var(--bg);font-family:inherit;font-size:13px;color:var(--text);outline:none;transition:border .15s;width:100%}
.form-input:focus,.form-select:focus{border-color:var(--teal);background:var(--surface)}
.form-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:18px}

/* ?? DETAIL TABS ?? */
.detail-tabs{display:flex;gap:0;border-bottom:2px solid var(--border);margin-bottom:18px}
.detail-tab{padding:9px 16px;font-size:12.5px;font-weight:500;cursor:pointer;color:var(--text-muted);border:none;background:none;font-family:inherit;border-bottom:2px solid transparent;margin-bottom:-2px}
.detail-tab.active{color:var(--teal);border-bottom-color:var(--teal)}
.chart-wrap{background:var(--bg);border-radius:var(--radius);padding:14px;margin-bottom:12px}
.chart-title{font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:8px;letter-spacing:.3px;text-transform:uppercase}
.history-table{width:100%;border-collapse:collapse;font-size:12.5px}
.history-table th{text-align:left;padding:7px 10px;font-size:10.5px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;border-bottom:1.5px solid var(--border)}
.history-table td{padding:9px 10px;border-bottom:1px solid var(--gray-light)}
.history-table tr:last-child td{border-bottom:none}
.history-table tr:hover td{background:var(--bg)}

/* ?? MERCADO VIEW ?? */
.mercado-hero{background:linear-gradient(135deg,var(--teal-dark),var(--teal));border-radius:var(--radius);padding:24px 28px;color:#fff;margin-bottom:20px}
.mercado-hero h3{font-family:'DM Serif Display',serif;font-size:20px;margin-bottom:5px}
.mercado-hero p{font-size:13px;opacity:.8}
.mercado-form{background:var(--surface);border-radius:var(--radius);padding:20px;border:1.5px solid var(--border);margin-bottom:20px}
.mercado-list{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}
.mercado-row{display:grid;grid-template-columns:1fr 100px 100px 36px;gap:8px;align-items:center}
.mercado-row-head{display:grid;grid-template-columns:1fr 100px 100px 36px;gap:8px;margin-bottom:4px}
.mercado-row-head span{font-size:10.5px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px}
.product-pill-btn{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-radius:var(--radius-sm);border:1.5px solid var(--border);background:var(--bg);font-family:inherit;font-size:13px;cursor:pointer;transition:all .15s;width:100%;text-align:left;overflow:hidden}
.product-pill-btn:hover{border-color:var(--teal)}
.product-pill-btn.filled{border-color:var(--teal);background:var(--teal-light);color:var(--teal-dark);font-weight:500}
.product-pill-text{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:13px}
.remove-btn{width:34px;height:34px;border-radius:6px;border:none;background:var(--red-light);color:var(--red);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0}
.remove-btn:hover{background:#fecaca}
.add-item-btn{display:flex;align-items:center;gap:8px;background:none;border:1.5px dashed var(--border);color:var(--text-muted);border-radius:var(--radius-sm);padding:9px 16px;font-size:13px;cursor:pointer;font-family:inherit;transition:all .15s;width:100%;justify-content:center}
.add-item-btn:hover{border-color:var(--teal);color:var(--teal);background:var(--teal-light)}
.prediction-card{background:var(--surface);border-radius:var(--radius);border:1.5px solid var(--border);padding:18px;margin-bottom:12px}
.prediction-card h4{font-size:14px;font-weight:600;margin-bottom:12px}
.pred-item{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--gray-light);gap:8px;flex-wrap:wrap}
.pred-item:last-child{border-bottom:none}
.pred-name{font-size:13px;font-weight:500}
.pred-detail{font-size:11.5px;color:var(--text-muted);margin-top:1px}
.pred-days{text-align:right;flex-shrink:0}
.pred-days strong{font-family:'DM Serif Display',serif;font-size:20px;display:block}
.pred-days span{font-size:11px;color:var(--text-muted)}

/* ?? TOAST ?? */
.toast{position:fixed;bottom:24px;right:24px;z-index:999;background:var(--navy);color:#fff;padding:11px 18px;border-radius:10px;font-size:13px;box-shadow:var(--shadow-lg);transform:translateY(80px);opacity:0;transition:all .3s;max-width:calc(100vw - 48px)}
.toast.show{transform:translateY(0);opacity:1}

/* ?? RESPONSIVE ?? */
@media(max-width:768px){
  :root{--sidebar:0px}
  .sidebar{transform:translateX(-220px);width:220px}
  .sidebar.open{transform:translateX(0)}
  .sidebar-overlay.open{display:block}
  .hamburger{display:flex}
  .main{margin-left:0;padding:70px 16px 24px}
  .topbar{margin-bottom:16px}
  .topbar-title h2{font-size:22px}
  .summary-cards{grid-template-columns:1fr 1fr;gap:10px}
  .summary-card{padding:14px}
  .summary-card .value{font-size:24px}
  .charts-grid{grid-template-columns:1fr}
  .chart-card.full{grid-column:1}
  .products-grid{grid-template-columns:1fr}
  .toolbar{gap:6px}
  .filter-tabs{display:none}
  .mercado-row{grid-template-columns:1fr 90px 34px}
  .mercado-row-head{grid-template-columns:1fr 90px 34px}
  .mercado-row .price-col{display:none}
  .mercado-row-head .price-head{display:none}
  .modal{border-radius:18px}
  .picker-sheet{max-height:92vh}
  .topbar-actions .btn span{display:none}
}
@media(max-width:480px){
  .summary-cards{grid-template-columns:1fr 1fr}
  .form-grid{grid-template-columns:1fr}
  .form-group.full{grid-column:1}
}
</style>
<!-- Datos inyectados por Flask (reemplazan localStorage) -->
<script>window.__INITIAL_DATA__ = FLASK_DATA_PLACEHOLDER;</script>
</head>
<body>

<!-- HAMBURGER -->
<button class="hamburger" onclick="toggleSidebar()" id="hamburger">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
</button>

<!-- SIDEBAR OVERLAY -->
<div class="sidebar-overlay" id="sidebar-overlay" onclick="toggleSidebar()"></div>

<!-- SIDEBAR -->
<nav class="sidebar" id="sidebar">
  <div class="sidebar-logo">
    <h1>Home<span>Stock</span></h1>
    <p>Inventario inteligente</p>
  </div>
  <div class="sidebar-nav">
    <div class="nav-section">Vistas</div>
    <button class="nav-item active" onclick="setView('dashboard')" id="nav-dashboard">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
      Dashboard
    </button>
    <button class="nav-item" onclick="setView('mercado')" id="nav-mercado">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
      Registrar Mercado
    </button>
    <button class="nav-item" onclick="setView('graficas')" id="nav-graficas">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
      Gr�ficas
    </button>

    <div class="nav-section" style="margin-top:14px">Categor�as</div>
    <button class="nav-item" onclick="setView('cat','Cocina')" id="nav-Cocina">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>
      Cocina <span class="cat-badge" id="badge-Cocina">0</span>
    </button>
    <button class="nav-item" onclick="setView('cat','Uso personal')" id="nav-Uso personal">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      Uso personal <span class="cat-badge" id="badge-Uso personal">0</span>
    </button>
    <button class="nav-item" onclick="setView('cat','Aseo')" id="nav-Aseo">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9.06 11.9 8.07-8.06a2.85 2.85 0 1 1 4.03 4.03l-8.06 8.08"/><path d="M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1 1 2.4 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02z"/></svg>
      Aseo <span class="cat-badge" id="badge-Aseo">0</span>
    </button>
    <button class="nav-item" onclick="setView('cat','Bebeca')" id="nav-Bebeca">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12h.01"/><path d="M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><path d="M19 6.3a9 9 0 0 1 1.8 3.9 2 2 0 0 1 0 3.6 9 9 0 0 1-17.6 0 2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5 1.1 3.5 2.5s-.9 2.5-2 3"/></svg>
      Bebeca <span class="cat-badge" id="badge-Bebeca">0</span>
    </button>
  </div>
</nav>

<main class="main" id="main-content"></main>

<!-- MAIN MODAL -->
<div class="modal-overlay" id="modal-overlay" onclick="closeModalOutside(event)">
  <div class="modal" id="modal-box">
    <div class="modal-header">
      <h3 id="modal-title"></h3>
      <button class="modal-close" onclick="closeModal()">�</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<!-- PRODUCT PICKER BOTTOM SHEET -->
<div class="picker-overlay" id="picker-overlay" onclick="closePickerOutside(event)">
  <div class="picker-sheet" id="picker-sheet">
    <div class="picker-header">
      <h3>Seleccionar producto</h3>
      <button class="modal-close" onclick="closePicker()">�</button>
    </div>
    <div class="picker-search-wrap">
      <svg class="picker-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input class="picker-search" id="picker-search" placeholder="Buscar producto..." oninput="filterPicker()">
    </div>
    <div class="picker-body" id="picker-body"></div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
// ??????????????????????????????????????????????
// DATA  �  ahora viene del servidor Python
// ??????????????????????????????????????????????
const CATEGORIES = ['Cocina','Uso personal','Aseo','Bebeca'];
const UNIT_TYPE={ml:'liquid',l:'liquid',g:'solid',kg:'solid',und:'count',pastillas:'count'};

function loadData(){ return JSON.parse(JSON.stringify(window.__INITIAL_DATA__)); }
function saveData(d){
  window.__INITIAL_DATA__ = JSON.parse(JSON.stringify(d));
  fetch('/api/save', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(d)
  }).catch(err => console.warn('Error al guardar:', err));
}
let DATA=loadData();

// ??????????????????????????????????????????????
// HELPERS
// ??????????????????????????????????????????????
function recalcRate(p){
  const done=p.entries.filter(e=>e.opened&&e.closed);
  if(!done.length) return p.dailyRate||null;
  const rates=done.map(e=>{const d=(new Date(e.closed)-new Date(e.opened))/86400000;return d>0?e.qty/d:null}).filter(Boolean);
  if(!rates.length) return p.dailyRate||null;
  return rates.reduce((a,b)=>a+b,0)/rates.length;
}
function getLastOpen(p){ return p.entries.filter(e=>e.opened&&!e.closed).sort((a,b)=>new Date(b.opened)-new Date(a.opened))[0]||null; }
function getDaysLeft(p){
  const rate=recalcRate(p); if(!rate) return null;
  const last=getLastOpen(p); if(!last) return null;
  const used=(Date.now()-new Date(last.opened))/86400000;
  return Math.max(0,(last.qty-(rate*used))/rate);
}
function getStatus(d){ if(d===null) return 'unknown'; if(d<=3) return 'critical'; if(d<=7) return 'warning'; return 'ok'; }
function statusLabel(s,d){ if(s==='unknown') return 'Sin datos'; if(s==='critical') return d<1?'�Agotado!':`${Math.round(d)}d cr�tico`; return `${Math.round(d)}d quedan`; }
function fmtDate(d){ if(!d) return '�'; return new Date(d).toLocaleDateString('es-CO',{day:'2-digit',month:'short',year:'numeric'}); }
function fmtN(n,u){ if(n===null||n===undefined) return '�'; return (u==='und'||u==='pastillas')?`${Math.round(n)}`:n<10?n.toFixed(1):Math.round(n).toLocaleString('es-CO'); }
function uid(){ return 'e'+Date.now()+Math.random().toString(36).slice(2); }

function updateBadges(){
  CATEGORIES.forEach(cat=>{
    const ps=DATA.products.filter(p=>p.category===cat);
    const alerts=ps.filter(p=>{ const d=getDaysLeft(p); return d!==null&&d<=7; }).length;
    const el=document.getElementById('badge-'+cat);
    if(el){ el.textContent=ps.length; el.style.background=alerts>0?'rgba(220,38,38,.3)':''; el.style.color=alerts>0?'#fca5a5':''; }
  });
}

// ??????????????????????????????????????????????
// LISTA DE MERCADO PROPUESTA
// ??????????????????????????????????????????????
function renderListaMercado(){
  const NEXT = 14;
  const all = DATA.products;
  const runningOut = all.filter(p=>{
    const d=getDaysLeft(p);
    return d!==null && d<=NEXT;
  }).sort((a,b)=>(getDaysLeft(a)||99)-(getDaysLeft(b)||99));
  const noStock = all.filter(p=>{
    const hasHistory=p.entries.length>0;
    const isOpen=!!getLastOpen(p);
    return hasHistory && !isOpen;
  });
  const total = runningOut.length + noStock.length;
  if(total===0) return `<div style="background:var(--teal-light);border:1.5px solid var(--teal);border-radius:var(--radius);padding:14px 18px;margin-bottom:20px;display:flex;align-items:center;gap:10px">
    <span style="font-size:20px">??</span>
    <div><div style="font-weight:600;color:var(--teal-dark);font-size:13px">�Todo en orden!</div>
    <div style="font-size:12px;color:var(--teal-dark);opacity:.8">No hay productos que se est�n terminando en los pr�ximos ${NEXT} d�as.</div></div>
  </div>`;
  const items = [
    ...runningOut.map(p=>{
      const d=getDaysLeft(p);
      const rate=recalcRate(p);
      const needed = rate ? Math.ceil(rate*NEXT) : null;
      return {p, daysLeft:Math.round(d), needed, reason:'ending'};
    }),
    ...noStock.map(p=>({p, daysLeft:null, needed:null, reason:'nostock'}))
  ];
  return `<div style="background:var(--surface);border:1.5px solid var(--border);border-radius:var(--radius);padding:18px 20px;margin-bottom:20px;box-shadow:var(--shadow)">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:18px">??</span>
        <div>
          <div style="font-weight:600;font-size:14px">Lista para el pr�ximo mercado</div>
          <div style="font-size:11.5px;color:var(--text-muted)">${total} producto${total>1?'s':''} en los pr�ximos ${NEXT} d�as</div>
        </div>
      </div>
      <button class="btn btn-primary btn-sm" onclick="setView('mercado')">Ir a registrar mercado</button>
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      ${items.map(({p,daysLeft,needed,reason})=>{
        const s = daysLeft!==null ? getStatus(daysLeft) : 'unknown';
        const dotColor = s==='critical'?'var(--red)':s==='warning'?'var(--amber)':'var(--gray)';
        const badge = daysLeft!==null
          ? `<span style="font-size:11px;font-weight:600;color:${dotColor};background:${s==='critical'?'var(--red-light)':s==='warning'?'var(--amber-light)':'var(--gray-light)'};padding:2px 8px;border-radius:20px">${daysLeft}d</span>`
          : `<span style="font-size:11px;color:var(--gray);background:var(--gray-light);padding:2px 8px;border-radius:20px">sin stock</span>`;
        const hint = needed
          ? `<span style="font-size:11px;color:var(--text-muted)">~${needed} ${p.unit} para ${NEXT}d</span>`
          : `<span style="font-size:11px;color:var(--text-muted)">reabastecer</span>`;
        return `<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;background:var(--bg);border-radius:8px;gap:8px;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:8px">
            <div style="width:8px;height:8px;border-radius:50%;background:${dotColor};flex-shrink:0"></div>
            <span style="font-size:13px;font-weight:500">${p.name}</span>
            <span style="font-size:11px;color:var(--text-muted)">${p.category}</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px">${hint}${badge}</div>
        </div>`;
      }).join('')}
    </div>
  </div>`;
}

// ??????????????????????????????????????????????
// ROUTING
// ??????????????????????????????????????????????
let currentView='dashboard', currentCat=null;
function setView(v,cat){
  currentView=v; currentCat=cat||null;
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  const id=cat?'nav-'+cat:'nav-'+v;
  const el=document.getElementById(id); if(el) el.classList.add('active');
  closeSidebar(); render();
}
function render(){
  updateBadges();
  const m=document.getElementById('main-content');
  if(currentView==='dashboard') m.innerHTML=renderDashboard();
  else if(currentView==='mercado') m.innerHTML=renderMercado();
  else if(currentView==='graficas') { m.innerHTML=renderGraficas(); setTimeout(()=>{ if(document.getElementById('gc-select')){ document.getElementById('gc-select').selectedIndex=1; } gcDraw(); },80); }
  else if(currentView==='cat') m.innerHTML=renderCategory(currentCat);
}

// ??????????????????????????????????????????????
// SIDEBAR MOBILE
// ??????????????????????????????????????????????
function toggleSidebar(){
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebar-overlay').classList.toggle('open');
}
function closeSidebar(){
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebar-overlay').classList.remove('open');
}

// ??????????????????????????????????????????????
// DASHBOARD
// ??????????????????????????????????????????????
function renderDashboard(){
  const all=DATA.products;
  const wData=all.filter(p=>getDaysLeft(p)!==null);
  const crit=wData.filter(p=>getStatus(getDaysLeft(p))==='critical');
  const warn=wData.filter(p=>getStatus(getDaysLeft(p))==='warning');
  const ok=wData.filter(p=>getStatus(getDaysLeft(p))==='ok');
  const alerts=[...crit,...warn].slice(0,5);
  return `
    <div class="topbar">
      <div class="topbar-title">
        <h2>Dashboard</h2>
        <p>${new Date().toLocaleDateString('es-CO',{weekday:'long',day:'numeric',month:'long'})}</p>
      </div>
      <div class="topbar-actions">
        <button class="btn btn-primary" onclick="openNewProduct()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
          <span>Nuevo producto</span>
        </button>
      </div>
    </div>
    ${alerts.length?`<div class="alert-strip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
      <p><strong>${alerts.length} producto${alerts.length>1?'s':''}</strong> necesitan atenci�n: ${alerts.map(p=>p.name).join(', ')}</p>
      <span class="alert-count">${alerts.length}</span>
    </div>`:''}
    <div class="summary-cards">
      <div class="summary-card"><div class="label">TOTAL</div><div class="value">${all.length}</div><div class="sub">${CATEGORIES.length} categor�as</div></div>
      <div class="summary-card good"><div class="label">OK</div><div class="value">${ok.length}</div><div class="sub">+7 d�as de stock</div></div>
      <div class="summary-card warning"><div class="label">ATENCI�N</div><div class="value">${warn.length}</div><div class="sub">menos de 7 d�as</div></div>
      <div class="summary-card danger"><div class="label">CR�TICOS</div><div class="value">${crit.length}</div><div class="sub">menos de 3 d�as</div></div>
    </div>
    ${renderListaMercado()}
    <div class="toolbar">
      <div class="search-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="search-input" id="search-input" placeholder="Buscar producto..." oninput="filterCards()">
      </div>
      <div class="filter-tabs">
        <button class="filter-tab active" onclick="setFilter('all',this)">Todos</button>
        <button class="filter-tab" onclick="setFilter('critical',this)">Cr�ticos</button>
        <button class="filter-tab" onclick="setFilter('warning',this)">Atenci�n</button>
        <button class="filter-tab" onclick="setFilter('ok',this)">OK</button>
        <button class="filter-tab" onclick="setFilter('unknown',this)">Sin datos</button>
      </div>
    </div>
    <div class="products-grid" id="products-grid">${all.filter(p=>getLastOpen(p)).map(p=>renderCard(p)).join('')}
    ${all.filter(p=>getLastOpen(p)).length===0?'<div style="grid-column:1/-1;text-align:center;padding:48px 20px;color:var(--text-muted)"><div style="font-size:32px;margin-bottom:10px">??</div><p style="font-size:14px">No hay productos abiertos. <br>Registra un mercado para empezar.</p></div>':''}
    </div>`;
}

let activeFilter='all';
function setFilter(f,btn){
  activeFilter=f;
  document.querySelectorAll('.filter-tab').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active'); filterCards();
}
function filterCards(){
  const q=(document.getElementById('search-input')?.value||'').toLowerCase();
  document.querySelectorAll('.product-card[data-pid]').forEach(card=>{
    const p=DATA.products.find(x=>x.id===card.dataset.pid); if(!p) return;
    const s=getStatus(getDaysLeft(p));
    card.style.display=(activeFilter==='all'||s===activeFilter)&&(!q||p.name.toLowerCase().includes(q)||p.category.toLowerCase().includes(q))?'':'none';
  });
}

function renderCard(p){
  const d=getDaysLeft(p), s=getStatus(d), rate=recalcRate(p), last=getLastOpen(p);
  let pct=0, fillCls='fill-ok';
  if(d!==null&&last){ const max=last.qty/(rate||1); pct=Math.min(100,Math.max(0,(d/max)*100)); fillCls=s==='critical'?'fill-critical':s==='warning'?'fill-warning':'fill-ok'; }
  const pillCls={critical:'pill-critical',warning:'pill-warning',ok:'pill-ok',unknown:'pill-unknown'}[s];
  return `<div class="product-card status-${s}" data-pid="${p.id}" onclick="openDetail('${p.id}')">
    <div class="card-top">
      <div><div class="card-name">${p.name}</div><div class="card-cat">${p.category}</div></div>
      <span class="status-pill ${pillCls}">${statusLabel(s,d)}</span>
    </div>
    ${d!==null?`<div class="progress-wrap"><div class="progress-label"><span>Stock</span><span>${Math.round(d)}d</span></div><div class="progress-bar"><div class="progress-fill ${fillCls}" style="width:${pct}%"></div></div></div>`:'<div style="height:6px"></div>'}
    <div class="card-stats">
      <div class="stat"><strong>${rate?fmtN(rate,p.unit)+' '+p.unit+'/d':'�'}</strong>Consumo</div>
      <div class="stat"><strong>${p.entries.length}</strong>Entradas</div>
      ${p.price?`<div class="stat"><strong>$${p.price.toLocaleString('es-CO')}</strong>Precio</div>`:''}
    </div>
    ${last?`<div style="margin-top:10px;display:flex;gap:6px" onclick="event.stopPropagation()">
      <button class="btn btn-sm" style="background:var(--red-light);color:var(--red);font-size:11px;padding:5px 10px" onclick="quickClose('${p.id}')">? Termin� esto</button>
    </div>`:''}
  </div>`;
}

// ??????????????????????????????????????????????
// CATEGORY VIEW
// ??????????????????????????????????????????????
function renderCategory(cat){
  const ps=DATA.products.filter(p=>p.category===cat);
  return `<div class="topbar">
    <div class="topbar-title"><h2>${cat}</h2><p>${ps.length} productos</p></div>
    <div class="topbar-actions"><button class="btn btn-primary" onclick="openNewProduct('${cat}')">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
      <span>Nuevo</span></button></div>
  </div>
  <div class="products-grid">${ps.map(p=>renderCard(p)).join('')}</div>`;
}

// ??????????????????????????????????????????????
// GRAFICAS VIEW
// ??????????????????????????????????????????????
function renderGraficas(){
  const withEntries=DATA.products.filter(p=>p.entries.some(e=>e.opened));
  const opts=withEntries.map(p=>`<option value="${p.id}">${p.name} (${p.unit})</option>`).join('');
  return `
    <div class="topbar">
      <div class="topbar-title"><h2>Gr�ficas</h2><p>Consumo hist�rico desde el inicio de tu registro</p></div>
    </div>
    <div class="charts-grid">
      <div class="chart-card full">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:10px">
          <h4 style="margin:0" id="gc-title">?? Consumo mensual</h4>
          <select class="form-select" id="gc-select" style="max-width:220px;font-size:13px" onchange="gcDraw()">
            <option value="">� Selecciona un producto �</option>
            ${opts}
          </select>
        </div>
        <canvas id="gc-consumo"></canvas>
      </div>
      <div class="chart-card">
        <h4>?? Tasa diaria � S�lidos (g/d�a)</h4>
        <canvas id="gc-rate-solid"></canvas>
      </div>
      <div class="chart-card">
        <h4>?? Tasa diaria � L�quidos (ml/d�a)</h4>
        <canvas id="gc-rate-liquid"></canvas>
      </div>
      <div class="chart-card">
        <h4>? Cocina � d�as por presentaci�n</h4>
        <canvas id="gc-dur-Cocina"></canvas>
      </div>
      <div class="chart-card">
        <h4>? Uso personal � d�as por presentaci�n</h4>
        <canvas id="gc-dur-Uso personal"></canvas>
      </div>
      <div class="chart-card">
        <h4>? Aseo � d�as por presentaci�n</h4>
        <canvas id="gc-dur-Aseo"></canvas>
      </div>
      <div class="chart-card">
        <h4>? Bebeca � d�as por presentaci�n</h4>
        <canvas id="gc-dur-Bebeca"></canvas>
      </div>
    </div>`;
}

// ?? CHART HELPERS ??????????????????????????????
function getMonthRange(){
  const all=[];
  DATA.products.forEach(p=>p.entries.forEach(e=>{ if(e.opened) all.push(new Date(e.opened)); }));
  if(!all.length) return [];
  all.sort((a,b)=>a-b);
  const start=new Date(all[0].getFullYear(),all[0].getMonth(),1);
  const end=new Date(); end.setDate(1);
  const months=[]; let cur=new Date(start);
  while(cur<=end){ months.push(new Date(cur)); cur.setMonth(cur.getMonth()+1); }
  return months;
}
function daysOverlap(opened,closed,m){
  const mS=new Date(m.getFullYear(),m.getMonth(),1);
  const mE=new Date(m.getFullYear(),m.getMonth()+1,0,23,59,59);
  const eS=new Date(opened);
  const eE=closed?new Date(closed):new Date();
  const s=eS>mS?eS:mS, e=eE<mE?eE:mE;
  const d=(e-s)/86400000; return d>0?d:0;
}
function monthlyQty(p,m){
  return p.entries.filter(e=>e.opened).reduce((acc,e)=>{
    const span=(new Date(e.closed||Date.now())-new Date(e.opened))/86400000||1;
    return acc+(e.qty/span)*daysOverlap(e.opened,e.closed,m);
  },0);
}
const GC={};
function gcMake(id,cfg){
  if(GC[id]){ try{GC[id].destroy();}catch(_){} delete GC[id]; }
  const el=document.getElementById(id); if(!el) return;
  try{ const ex=Chart.getChart(el); if(ex) ex.destroy(); }catch(_){}
  GC[id]=new Chart(el,cfg);
}
const CAT_COLOR={'Cocina':'#1A7B6E','Uso personal':'#D97706','Aseo':'#3B82F6','Bebeca':'#EC4899'};

function gcDraw(){
  const months=getMonthRange();
  if(!months.length) return;
  const mLabels=months.map(m=>m.toLocaleDateString('es-CO',{month:'short',year:'2-digit'}));
  const sel=document.getElementById('gc-select');
  const pid=sel?sel.value:'';
  const p=pid?DATA.products.find(x=>x.id===pid):null;
  if(p){
    const title=document.getElementById('gc-title');
    if(title) title.textContent=`?? ${p.name} � consumo mensual (${p.unit})`;
    const data=months.map(m=>+monthlyQty(p,m).toFixed(1));
    const col=CAT_COLOR[p.category]||'#1A7B6E';
    gcMake('gc-consumo',{type:'bar',
      data:{labels:mLabels,datasets:[{label:p.unit+'/mes',data,
        backgroundColor:col+'88',borderColor:col,borderWidth:1.5,borderRadius:6}]},
      options:{responsive:true,plugins:{legend:{display:false}},
        scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:'#E2DDD5'},
          title:{display:true,text:p.unit+' / mes'}}}}
    });
  }
  if(!GC['gc-rate-solid']){
    const withRate=DATA.products.filter(p=>recalcRate(p)!==null);
    function rateChart(id,prods,lbl){
      if(!prods.length) return;
      gcMake(id,{type:'bar',
        data:{labels:prods.map(p=>p.name),datasets:[{label:lbl,
          data:prods.map(p=>+recalcRate(p).toFixed(1)),
          backgroundColor:prods.map(p=>CAT_COLOR[p.category]+'BB'),
          borderColor:prods.map(p=>CAT_COLOR[p.category]),borderWidth:1.5,borderRadius:5}]},
        options:{indexAxis:'y',responsive:true,plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>' '+ctx.parsed.x+' '+prods[ctx.dataIndex].unit+'/d�a'}}},
          scales:{x:{beginAtZero:true,grid:{color:'#E2DDD5'},title:{display:true,text:lbl}},
            y:{grid:{display:false},ticks:{font:{size:11}}}}}
      });
    }
    rateChart('gc-rate-solid',withRate.filter(p=>UNIT_TYPE[p.unit]==='solid').sort((a,b)=>recalcRate(b)-recalcRate(a)).slice(0,10),'g/d�a');
    rateChart('gc-rate-liquid',withRate.filter(p=>UNIT_TYPE[p.unit]==='liquid').sort((a,b)=>recalcRate(b)-recalcRate(a)).slice(0,10),'ml/d�a');
    CATEGORIES.forEach(cat=>{
      const id='gc-dur-'+cat;
      const prods=DATA.products.filter(p=>p.category===cat&&p.entries.some(e=>e.opened&&e.closed));
      if(!prods.length) return;
      const data=prods.map(p=>{
        const done=p.entries.filter(e=>e.opened&&e.closed);
        const avg=done.reduce((s,e)=>{const d=(new Date(e.closed)-new Date(e.opened))/86400000; return s+(d>0?d:0);},0)/done.length;
        return {name:p.name,avg:Math.round(avg),n:done.length};
      }).filter(d=>d.avg>0).sort((a,b)=>b.avg-a.avg);
      if(!data.length) return;
      gcMake(id,{type:'bar',
        data:{labels:data.map(d=>d.name),datasets:[{label:'d�as',data:data.map(d=>d.avg),
          backgroundColor:CAT_COLOR[cat]+'BB',borderColor:CAT_COLOR[cat],borderWidth:1.5,borderRadius:5}]},
        options:{indexAxis:'y',responsive:true,plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>' '+ctx.parsed.x+' d�as ('+data[ctx.dataIndex].n+' entradas)'}}},
          scales:{x:{beginAtZero:true,grid:{color:'#E2DDD5'},title:{display:true,text:'d�as'}},
            y:{grid:{display:false},ticks:{font:{size:11}}}}}
      });
    });
  }
}

// ??????????????????????????????????????????????
// DETAIL MODAL
// ??????????????????????????????????????????????
let detailTab='info';
function openDetail(pid){ detailTab='info'; showModal('detail',pid); }

function renderDetailModal(pid){
  const p=DATA.products.find(x=>x.id===pid); if(!p) return;
  const rate=recalcRate(p), d=getDaysLeft(p), s=getStatus(d);
  const pillCls={critical:'pill-critical',warning:'pill-warning',ok:'pill-ok',unknown:'pill-unknown'}[s];
  document.getElementById('modal-title').textContent=p.name;
  document.getElementById('modal-body').innerHTML=`
    <div style="display:flex;gap:8px;align-items:center;margin-bottom:14px">
      <span style="background:var(--surface2);padding:3px 10px;border-radius:20px;font-size:11.5px;color:var(--text-muted)">${p.category}</span>
      <span class="status-pill ${pillCls}">${statusLabel(s,d)}</span>
    </div>
    <div class="detail-tabs">
      <button class="detail-tab ${detailTab==='info'?'active':''}" onclick="switchTab('${pid}','info')">Info</button>
      <button class="detail-tab ${detailTab==='historial'?'active':''}" onclick="switchTab('${pid}','historial')">Historial</button>
      <button class="detail-tab ${detailTab==='graficos'?'active':''}" onclick="switchTab('${pid}','graficos')">Gr�ficos</button>
    </div>
    ${detailTab==='info'?detailInfo(p,rate,d):''}
    ${detailTab==='historial'?detailHistorial(p):''}
    ${detailTab==='graficos'?detailGraficos(p):''}
  `;
  if(detailTab==='graficos') setTimeout(()=>drawProductCharts(p),60);
}

function detailInfo(p,rate,d){
  return `
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:18px">
      <div style="background:var(--bg);border-radius:10px;padding:12px;text-align:center">
        <div style="font-family:'DM Serif Display',serif;font-size:26px">${rate?fmtN(rate,p.unit):'�'}</div>
        <div style="font-size:10.5px;color:var(--text-muted);margin-top:2px">${p.unit}/d�a</div>
      </div>
      <div style="background:var(--bg);border-radius:10px;padding:12px;text-align:center">
        <div style="font-family:'DM Serif Display',serif;font-size:26px;color:${d!==null?(d<=3?'var(--red)':d<=7?'var(--amber)':'var(--teal)'):'var(--gray)'}">${d!==null?Math.round(d):'�'}</div>
        <div style="font-size:10.5px;color:var(--text-muted);margin-top:2px">d�as restantes</div>
      </div>
      <div style="background:var(--bg);border-radius:10px;padding:12px;text-align:center">
        <div style="font-family:'DM Serif Display',serif;font-size:26px">${p.entries.length}</div>
        <div style="font-size:10.5px;color:var(--text-muted);margin-top:2px">entradas</div>
      </div>
    </div>
    ${p.price!==null?`<div style="background:var(--teal-light);border-radius:10px;padding:11px 14px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between">
      <span style="font-size:12.5px;color:var(--teal-dark);font-weight:500">Precio registrado</span>
      <span style="font-family:'DM Serif Display',serif;font-size:18px;color:var(--teal-dark)">$${p.price.toLocaleString('es-CO')}</span>
    </div>`:''}
    <div style="display:flex;gap:7px;flex-wrap:wrap">
      <button class="btn btn-primary btn-sm" onclick="openAddEntry('${p.id}')">+ Nueva entrada</button>
      <button class="btn btn-secondary btn-sm" onclick="openEditProduct('${p.id}')">Editar</button>
      <button class="btn btn-danger btn-sm" onclick="confirmDelete('${p.id}')">Eliminar</button>
    </div>`;
}

function detailHistorial(p){
  const sorted=[...p.entries].sort((a,b)=>new Date(b.opened||0)-new Date(a.opened||0));
  if(!sorted.length) return '<div style="text-align:center;padding:30px;color:var(--text-muted);font-size:13px">Sin entradas todav�a.<br><br><button class="btn btn-primary btn-sm" onclick="openAddEntry(\''+p.id+'\')">+ Agregar primera entrada</button></div>';
  return `<div style="overflow-x:auto"><table class="history-table"><thead><tr>
    <th>Cantidad</th><th>Abierto</th><th>Cerrado</th><th>D�as</th><th>Tasa</th><th>Precio</th><th></th>
  </tr></thead><tbody>
    ${sorted.map(e=>{
      const days=e.opened&&e.closed?Math.round((new Date(e.closed)-new Date(e.opened))/86400000):'�';
      const tasa=(e.opened&&e.closed&&days>0)?fmtN(e.qty/days,p.unit):'�';
      return `<tr><td><strong>${fmtN(e.qty,p.unit)} ${p.unit}</strong></td><td>${fmtDate(e.opened)}</td><td>${fmtDate(e.closed)}</td><td>${days}</td><td>${tasa!=='�'?tasa+' '+p.unit+'/d':'�'}</td><td>${e.price?'$'+e.price.toLocaleString('es-CO'):'�'}</td><td><button class="remove-btn" style="width:22px;height:22px;font-size:11px" onclick="deleteEntry('${p.id}','${e.id}')">�</button></td></tr>`;
    }).join('')}
  </tbody></table></div>
  <div style="margin-top:10px"><button class="btn btn-primary btn-sm" onclick="openAddEntry('${p.id}')">+ Nueva entrada</button></div>`;
}

function detailGraficos(p){
  return `
    <div class="chart-wrap"><div class="chart-title">TASA DE CONSUMO POR ENTRADA (${p.unit}/d�a)</div><canvas id="chart-rate" height="150"></canvas></div>
    <div class="chart-wrap"><div class="chart-title">D�AS QUE DUR� CADA PRESENTACI�N</div><canvas id="chart-days" height="150"></canvas></div>`;
}

function drawProductCharts(p){
  const done=p.entries.filter(e=>e.opened&&e.closed).sort((a,b)=>new Date(a.opened)-new Date(b.opened));
  if(!done.length) return;
  const labels=done.map((e,i)=>`#${i+1} ${fmtDate(e.opened).slice(0,6)}`);
  const rates=done.map(e=>{const d=(new Date(e.closed)-new Date(e.opened))/86400000;return d>0?+(e.qty/d).toFixed(2):0;});
  const days=done.map(e=>Math.round((new Date(e.closed)-new Date(e.opened))/86400000));
  const cfg=(data,lbl,color)=>({type:'bar',data:{labels,datasets:[{label:lbl,data,backgroundColor:color+'BB',borderColor:color,borderWidth:1.5,borderRadius:5}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'#E2DDD5'}},x:{grid:{display:false}}}}});
  const rc=document.getElementById('chart-rate'); if(rc) new Chart(rc,cfg(rates,p.unit+'/d�a','#1A7B6E'));
  const dc=document.getElementById('chart-days'); if(dc) new Chart(dc,cfg(days,'D�as','#D97706'));
}

function switchTab(pid,tab){ detailTab=tab; renderDetailModal(pid); }

// ??????????????????????????????????????????????
// ADD ENTRY
// ??????????????????????????????????????????????
function openAddEntry(pid){
  const p=DATA.products.find(x=>x.id===pid);
  document.getElementById('modal-title').textContent=`Nueva entrada � ${p.name}`;
  const today=new Date().toISOString().split('T')[0];
  document.getElementById('modal-body').innerHTML=`
    <p style="font-size:12.5px;color:var(--text-muted);margin-bottom:18px">Registra una compra de <strong>${p.name}</strong>. La tasa de consumo se recalcula autom�ticamente.</p>
    <div class="form-grid">
      <div class="form-group"><label class="form-label">CANTIDAD (${p.unit})</label><input class="form-input" type="number" id="e-qty" placeholder="ej. 1000" step="any" min="0"></div>
      <div class="form-group"><label class="form-label">PRECIO (opcional)</label><input class="form-input" type="number" id="e-price" placeholder="ej. 3200" step="any" min="0"></div>
      <div class="form-group"><label class="form-label">FECHA APERTURA</label><input class="form-input" type="date" id="e-opened" value="${today}"></div>
      <div class="form-group"><label class="form-label">FECHA CIERRE (si ya termin�)</label><input class="form-input" type="date" id="e-closed"></div>
    </div>
    <div class="form-actions">
      <button class="btn btn-secondary" onclick="openDetail('${pid}')">Cancelar</button>
      <button class="btn btn-primary" onclick="saveEntry('${pid}')">Guardar</button>
    </div>`;
}

function saveEntry(pid){
  const qty=parseFloat(document.getElementById('e-qty').value);
  const opened=document.getElementById('e-opened').value;
  const closed=document.getElementById('e-closed').value||null;
  const price=parseFloat(document.getElementById('e-price').value)||null;
  if(!qty||!opened){showToast('Completa cantidad y fecha de apertura');return;}
  const p=DATA.products.find(x=>x.id===pid);
  p.entries.push({id:uid(),qty,opened,closed,price});
  if(price) p.price=price;
  saveData(DATA); closeModal(); render(); showToast(`Entrada guardada para ${p.name} ?`);
}

function deleteEntry(pid,eid){
  const p=DATA.products.find(x=>x.id===pid);
  p.entries=p.entries.filter(e=>e.id!==eid);
  saveData(DATA); renderDetailModal(pid); showToast('Entrada eliminada');
}

// ??????????????????????????????????????????????
// NEW / EDIT PRODUCT
// ??????????????????????????????????????????????
function openNewProduct(defaultCat){
  document.getElementById('modal-title').textContent='Nuevo producto';
  document.getElementById('modal-body').innerHTML=productForm(null,defaultCat);
  showModal('form');
}
function openEditProduct(pid){
  const p=DATA.products.find(x=>x.id===pid);
  document.getElementById('modal-title').textContent=`Editar � ${p.name}`;
  document.getElementById('modal-body').innerHTML=productForm(p);
  showModal('form');
}
function productForm(p,defCat){
  const cats=CATEGORIES.map(c=>`<option value="${c}" ${(p?.category||defCat)===c?'selected':''}>${c}</option>`).join('');
  const units=['g','ml','und','pastillas','kg','l'].map(u=>`<option value="${u}" ${p?.unit===u?'selected':''}>${u}</option>`).join('');
  return `<div class="form-grid">
    <div class="form-group full"><label class="form-label">NOMBRE</label><input class="form-input" id="np-name" placeholder="ej. Aceite de cocina" value="${p?.name||''}"></div>
    <div class="form-group"><label class="form-label">CATEGOR�A</label><select class="form-select" id="np-cat">${cats}</select></div>
    <div class="form-group"><label class="form-label">UNIDAD</label><select class="form-select" id="np-unit">${units}</select></div>
    <div class="form-group"><label class="form-label">TASA DIARIA ESTIMADA</label><input class="form-input" type="number" id="np-rate" placeholder="opcional" value="${p?.dailyRate||''}" step="any" min="0"></div>
    <div class="form-group"><label class="form-label">PRECIO REFERENCIA</label><input class="form-input" type="number" id="np-price" placeholder="opcional" value="${p?.price||''}" step="any" min="0"></div>
  </div>
  <div class="form-actions">
    <button class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
    <button class="btn btn-primary" onclick="saveProduct(${p?`'${p.id}'`:'null'})">${p?'Guardar':'Crear'}</button>
  </div>`;
}
function saveProduct(pid){
  const name=document.getElementById('np-name').value.trim();
  const cat=document.getElementById('np-cat').value;
  const unit=document.getElementById('np-unit').value;
  const rate=parseFloat(document.getElementById('np-rate').value)||null;
  const price=parseFloat(document.getElementById('np-price').value)||null;
  if(!name){showToast('El nombre es obligatorio');return;}
  if(pid){const p=DATA.products.find(x=>x.id===pid);Object.assign(p,{name,category:cat,unit,dailyRate:rate,price});}
  else DATA.products.push({id:uid(),name,category:cat,unit,dailyRate:rate,entries:[],price});
  saveData(DATA); closeModal(); render(); showToast(`${name} ${pid?'actualizado':'creado'} ?`);
}
function confirmDelete(pid){
  const p=DATA.products.find(x=>x.id===pid);
  if(!confirm(`�Eliminar "${p.name}"? Se borrar� su historial.`))return;
  DATA.products=DATA.products.filter(x=>x.id!==pid);
  saveData(DATA); closeModal(); render(); showToast(`${p.name} eliminado`);
}

function quickClose(pid){
  const p=DATA.products.find(x=>x.id===pid);
  const last=getLastOpen(p); if(!last) return;
  const today=new Date().toISOString().split('T')[0];
  document.getElementById('modal-title').textContent='�Cu�ndo se termin�?';
  document.getElementById('modal-body').innerHTML=`
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:18px">
      Registra la fecha en que se acab� <strong>${p.name}</strong>.
    </p>
    <div class="form-group">
      <label class="form-label">FECHA DE CIERRE</label>
      <input class="form-input" type="date" id="qc-date" value="${today}" style="max-width:220px">
    </div>
    <div class="form-actions" style="margin-top:20px">
      <button class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
      <button class="btn btn-primary" onclick="confirmQuickClose('${pid}')">Confirmar</button>
    </div>`;
  showModal('form');
}
function confirmQuickClose(pid){
  const d=document.getElementById('qc-date').value;
  if(!d){showToast('Selecciona una fecha');return;}
  const p=DATA.products.find(x=>x.id===pid);
  const last=getLastOpen(p); if(!last) return;
  last.closed=d;
  saveData(DATA); closeModal(); render(); showToast(`${p.name} marcado como terminado ?`);
}

// ??????????????????????????????????????????????
// MERCADO
// ??????????????????????????????????????????????
let mercadoItems=[];
let mercadoResults=null;

function renderMercado(){
  const today=new Date().toISOString().split('T')[0];
  const rowsHTML=mercadoItems.map((item,i)=>{
    const p=item.pid?DATA.products.find(x=>x.id===item.pid):null;
    return `<div class="mercado-row" id="mrow-${i}">
      <button class="product-pill-btn ${p?'filled':''}" onclick="openPicker(${i})">
        <span class="product-pill-text">${p?p.name:'Toca para elegir...'}</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="flex-shrink:0"><path d="m6 9 6 6 6-6"/></svg>
      </button>
      <input class="form-input price-col" type="number" placeholder="Precio $" step="any" min="0"
        value="${item.price||''}" onchange="mercadoItems[${i}].price=parseFloat(this.value)||null">
      <input class="form-input" type="number" placeholder="Cant." step="any" min="0"
        value="${item.qty||''}" onchange="mercadoItems[${i}].qty=parseFloat(this.value)||0">
      <button class="remove-btn" onclick="removeMercadoItem(${i})">�</button>
    </div>`;
  }).join('');
  return `
    <div class="topbar">
      <div class="topbar-title"><h2>Registrar Mercado</h2><p>�Qu� compraste hoy? Ingresa los productos y calculo cu�ndo se acaba cada uno.</p></div>
    </div>
    <div class="mercado-hero">
      <h3>?? Nuevo mercado</h3>
      <p>Selecciona cada producto, su cantidad y precio. Puedes crear productos nuevos desde el selector.</p>
    </div>
    <div class="mercado-form">
      <div style="margin-bottom:14px">
        <label class="form-label">FECHA DE COMPRA</label>
        <input class="form-input" type="date" id="mercado-date" value="${today}" style="max-width:190px;margin-top:5px">
      </div>
      <div class="mercado-row-head">
        <span>Producto</span>
        <span class="price-head">Precio ($)</span>
        <span>Cantidad</span>
        <span></span>
      </div>
      <div class="mercado-list" id="mercado-list">${rowsHTML}</div>
      <button class="add-item-btn" onclick="addMercadoItem()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
        Agregar producto
      </button>
      <div class="form-actions" style="margin-top:16px">
        <button class="btn btn-secondary" onclick="mercadoItems=[];mercadoResults=null;render()">Limpiar</button>
        <button class="btn btn-primary" onclick="procesarMercado()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
          Registrar y calcular
        </button>
      </div>
    </div>
    ${mercadoResults?renderMercadoResults():''}`;
}

function addMercadoItem(){ mercadoItems.push({pid:'',qty:0,price:null}); render(); setTimeout(()=>document.getElementById('mercado-list')?.lastElementChild?.scrollIntoView({behavior:'smooth'}),60); }
function removeMercadoItem(i){ mercadoItems.splice(i,1); render(); }

function procesarMercado(){
  const date=document.getElementById('mercado-date').value;
  const valid=mercadoItems.filter(it=>it.pid&&it.qty>0);
  if(!valid.length){showToast('Agrega al menos un producto con cantidad');return;}
  valid.forEach(it=>{
    const p=DATA.products.find(x=>x.id===it.pid); if(!p) return;
    const prev=p.entries.find(e=>e.opened&&!e.closed); if(prev) prev.closed=date;
    p.entries.push({id:uid(),qty:it.qty,opened:date,closed:null,price:it.price});
    if(it.price) p.price=it.price;
  });
  DATA.mercadoHistory.push({date,items:valid.map(it=>({...it}))});
  saveData(DATA); mercadoResults=valid; updateBadges(); render();
  showToast(`�Mercado registrado! ${valid.length} productos actualizados ?`);
}

function renderMercadoResults(){
  const next=14;
  const needRestock=mercadoResults.filter(it=>{
    const p=DATA.products.find(x=>x.id===it.pid); if(!p) return false;
    const d=getDaysLeft(p); return d!==null&&d<next;
  });
  return `
    <div class="prediction-card">
      <h4>?? Proyecci�n � pr�ximos ${next} d�as</h4>
      ${mercadoResults.map(it=>{
        const p=DATA.products.find(x=>x.id===it.pid); if(!p) return '';
        const rate=recalcRate(p),d=getDaysLeft(p),s=getStatus(d);
        return `<div class="pred-item">
          <div><div class="pred-name">${p.name}</div><div class="pred-detail">${rate?fmtN(rate,p.unit)+' '+p.unit+'/d�a � ':''}${fmtN(it.qty,p.unit)} ${p.unit} comprados</div></div>
          <div class="pred-days"><strong style="color:${s==='critical'?'var(--red)':s==='warning'?'var(--amber)':'var(--teal)'}">${d!==null?Math.round(d):'?'}</strong><span>d�as est.</span></div>
          <span class="status-pill ${d!==null&&d<next?'pill-warning':'pill-ok'}">${d!==null&&d<next?'Pedir pronto':'OK'}</span>
        </div>`;
      }).join('')}
    </div>
    <div style="background:var(--teal-light);border-radius:var(--radius);padding:14px 18px;border:1.5px solid var(--teal)">
      <div style="font-weight:600;color:var(--teal-dark);margin-bottom:8px">??? Comprar en pr�ximo mercado</div>
      <div style="display:flex;flex-wrap:wrap;gap:7px">
        ${needRestock.length?needRestock.map(it=>{const p=DATA.products.find(x=>x.id===it.pid);return `<span style="background:var(--teal);color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500">${p.name}</span>`;}).join(''):'<span style="color:var(--teal-dark);font-size:13px">�Todo alcanza para el pr�ximo mercado! ??</span>'}
      </div>
    </div>`;
}

// ??????????????????????????????????????????????
// PRODUCT PICKER BOTTOM SHEET
// ??????????????????????????????????????????????
let pickerItemIndex=-1;

function openPicker(idx){
  pickerItemIndex=idx;
  document.getElementById('picker-search').value='';
  renderPickerBody('');
  document.getElementById('picker-overlay').classList.add('open');
  setTimeout(()=>document.getElementById('picker-search').focus(),200);
}
function closePicker(){ document.getElementById('picker-overlay').classList.remove('open'); }
function closePickerOutside(e){ if(e.target===document.getElementById('picker-overlay')) closePicker(); }
function filterPicker(){ renderPickerBody(document.getElementById('picker-search').value.toLowerCase()); }

function renderPickerBody(q){
  const body=document.getElementById('picker-body'); if(!body) return;
  const curPid=mercadoItems[pickerItemIndex]?.pid;
  let html='';
  CATEGORIES.forEach(cat=>{
    const ps=DATA.products.filter(p=>p.category===cat&&(!q||p.name.toLowerCase().includes(q)));
    if(!ps.length) return;
    html+=`<div class="picker-cat-label">${cat}</div>`;
    ps.forEach(p=>{
      const rate=recalcRate(p);
      const sel=p.id===curPid;
      html+=`<button class="picker-product-btn ${sel?'selected':''}" onclick="selectPickerProduct('${p.id}')">
        <div>
          <div style="font-weight:${sel?600:400}">${p.name} ${sel?'?':''}</div>
          <div class="picker-product-meta">${rate?fmtN(rate,p.unit)+' '+p.unit+'/d�a':''}</div>
        </div>
        ${p.price?`<span style="font-size:11.5px;color:var(--text-muted)">$${p.price.toLocaleString('es-CO')}</span>`:''}
      </button>`;
    });
  });
  if(!html) html=`<div style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px">No se encontr� "${q}"</div>`;
  html+=`<button class="picker-new-btn" onclick="openNewFromPicker()">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
    Crear nuevo producto
  </button>`;
  body.innerHTML=html;
}

function selectPickerProduct(pid){
  if(pickerItemIndex>=0) mercadoItems[pickerItemIndex].pid=pid;
  closePicker(); render();
}

function openNewFromPicker(){
  closePicker();
  document.getElementById('modal-title').textContent='Nuevo producto';
  document.getElementById('modal-body').innerHTML=productFormForMercado();
  showModal('form');
}

function productFormForMercado(){
  const cats=CATEGORIES.map(c=>`<option value="${c}">${c}</option>`).join('');
  const units=['g','ml','und','pastillas','kg','l'].map(u=>`<option value="${u}">${u}</option>`).join('');
  return `<p style="font-size:12.5px;color:var(--text-muted);margin-bottom:16px">Crea el producto y luego selecci�nalo en el mercado.</p>
  <div class="form-grid">
    <div class="form-group full"><label class="form-label">NOMBRE</label><input class="form-input" id="np-name" placeholder="ej. Aceite de cocina"></div>
    <div class="form-group"><label class="form-label">CATEGOR�A</label><select class="form-select" id="np-cat">${cats}</select></div>
    <div class="form-group"><label class="form-label">UNIDAD</label><select class="form-select" id="np-unit">${units}</select></div>
    <div class="form-group"><label class="form-label">TASA DIARIA EST.</label><input class="form-input" type="number" id="np-rate" placeholder="opcional" step="any" min="0"></div>
    <div class="form-group"><label class="form-label">PRECIO</label><input class="form-input" type="number" id="np-price" placeholder="opcional" step="any" min="0"></div>
  </div>
  <div class="form-actions">
    <button class="btn btn-secondary" onclick="closeModal();setTimeout(()=>openPicker(${pickerItemIndex}),100)">Cancelar</button>
    <button class="btn btn-primary" onclick="saveProductAndPick()">Crear y seleccionar</button>
  </div>`;
}

function saveProductAndPick(){
  const name=document.getElementById('np-name').value.trim();
  const cat=document.getElementById('np-cat').value;
  const unit=document.getElementById('np-unit').value;
  const rate=parseFloat(document.getElementById('np-rate').value)||null;
  const price=parseFloat(document.getElementById('np-price').value)||null;
  if(!name){showToast('El nombre es obligatorio');return;}
  const newId=uid();
  DATA.products.push({id:newId,name,category:cat,unit,dailyRate:rate,entries:[],price});
  saveData(DATA);
  mercadoItems[pickerItemIndex].pid=newId;
  closeModal(); render(); showToast(`${name} creado y seleccionado ?`);
}

// ??????????????????????????????????????????????
// MODAL CONTROL
// ??????????????????????????????????????????????
function showModal(type,pid){
  document.getElementById('modal-overlay').classList.add('open');
  if(type==='detail') renderDetailModal(pid);
}
function closeModal(){ document.getElementById('modal-overlay').classList.remove('open'); }
function closeModalOutside(e){ if(e.target===document.getElementById('modal-overlay')) closeModal(); }

// ??????????????????????????????????????????????
// TOAST
// ??????????????????????????????????????????????
function showToast(msg){ const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),2800); }

// ??????????????????????????????????????????????
// INIT
// ??????????????????????????????????????????????
render();
</script>
</body>
</html>"""


# ?? Flask routes ??????????????????????????????????????????????????????????????

@app.route("/")
def index():
    data = load_data()
    data_json = json.dumps(data, ensure_ascii=False)
    # Reemplazamos el placeholder seguro en la plantilla raw
    html = HTML_TEMPLATE.replace("FLASK_DATA_PLACEHOLDER", data_json)
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/api/save", methods=["POST"])
def api_save():
    """Recibe el estado completo del inventario y lo persiste."""
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"ok": False, "error": "Payload vac�o o JSON inv�lido"}), 400
        save_data(data)
        return jsonify({"ok": True})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/api/data", methods=["GET"])
def api_data():
    """Devuelve el JSON completo (�til para depuraci�n o integraciones)."""
    return jsonify(load_data())


# ?? Punto de entrada ??????????????????????????????????????????????????????????

if __name__ == "__main__":
    print()
    print("=" * 42)
    print("  HomeStock AI - servidor Python")
    print("=" * 42)
    print("  Abre en:  http://localhost:5000")
    print("  Datos en: homestockai_data.json")
    print("=" * 42)
    print()
    app.run(debug=True, port=5000, host="0.0.0.0")
