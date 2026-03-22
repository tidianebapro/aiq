#!/usr/bin/env python3
"""
ArchIntel — AI-Augmented Enterprise Architecture Platform
Demo Backend — Flask API on port 5003
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# ─── Mock Data ─────────────────────────────────────────────────────────────

SYSTEMS = [
    # ERP & Core
    {"id": "sap-erp",       "name": "SAP ERP S/4HANA",        "type": "ERP",           "domain": "Finance",        "risk": 7.5, "criticality": "CRITICAL", "vendor": "SAP",         "tech": "Java/ABAP",   "eol": False, "cloud": False, "validated": True,  "deps_up": 23, "deps_down": 64, "color": "#981E13"},
    {"id": "oracle-ebs",    "name": "Oracle EBS Financials",   "type": "ERP/Finance",   "domain": "Finance",        "risk": 6.8, "criticality": "CRITICAL", "vendor": "Oracle",      "tech": "Java",        "eol": False, "cloud": False, "validated": True,  "deps_up": 18, "deps_down": 41, "color": "#C42B1C"},
    {"id": "hyperion",      "name": "Hyperion Planning",       "type": "Finance",       "domain": "Finance",        "risk": 4.2, "criticality": "HIGH",     "vendor": "Oracle",      "tech": "Java",        "eol": True,  "cloud": False, "validated": True,  "deps_up": 4,  "deps_down": 12, "color": "#DC2626"},
    # Integration
    {"id": "api-gateway",   "name": "API Gateway (Kong)",      "type": "Integration",   "domain": "Integration",   "risk": 3.1, "criticality": "HIGH",     "vendor": "Kong",        "tech": "Nginx/Lua",   "eol": False, "cloud": True,  "validated": False, "deps_up": 41, "deps_down": 89, "color": "#2563EB"},
    {"id": "mulesoft",      "name": "MuleSoft ESB",            "type": "Integration",   "domain": "Integration",   "risk": 4.8, "criticality": "HIGH",     "vendor": "Salesforce",  "tech": "Java",        "eol": False, "cloud": False, "validated": False, "deps_up": 28, "deps_down": 55, "color": "#1D4ED8"},
    {"id": "kafka",         "name": "Apache Kafka",            "type": "Messaging",     "domain": "Integration",   "risk": 3.4, "criticality": "HIGH",     "vendor": "OSS",         "tech": "Scala/Java",  "eol": False, "cloud": False, "validated": False, "deps_up": 12, "deps_down": 34, "color": "#3B82F6"},
    # Operations
    {"id": "mes",           "name": "MES Manufacturing",       "type": "Operations",    "domain": "Operations",    "risk": 5.4, "criticality": "HIGH",     "vendor": "Siemens",     "tech": ".NET",        "eol": False, "cloud": False, "validated": True,  "deps_up": 8,  "deps_down": 29, "color": "#16A34A"},
    {"id": "scada",         "name": "SCADA Control System",    "type": "OT/IoT",        "domain": "Operations",    "risk": 6.1, "criticality": "CRITICAL", "vendor": "ABB",         "tech": "Proprietary", "eol": False, "cloud": False, "validated": True,  "deps_up": 3,  "deps_down": 14, "color": "#15803D"},
    {"id": "lims",          "name": "LIMS Laboratory",         "type": "Lab/QA",        "domain": "Operations",    "risk": 4.6, "criticality": "HIGH",     "vendor": "LabWare",     "tech": "Java",        "eol": False, "cloud": False, "validated": True,  "deps_up": 6,  "deps_down": 18, "color": "#166534"},
    # SaaS
    {"id": "salesforce",    "name": "Salesforce CRM",          "type": "CRM",           "domain": "SaaS",          "risk": 2.1, "criticality": "MEDIUM",   "vendor": "Salesforce",  "tech": "Cloud",       "eol": False, "cloud": True,  "validated": False, "deps_up": 15, "deps_down": 22, "color": "#7C3AED"},
    {"id": "workday",       "name": "Workday HCM",             "type": "HR",            "domain": "SaaS",          "risk": 2.8, "criticality": "MEDIUM",   "vendor": "Workday",     "tech": "Cloud",       "eol": False, "cloud": True,  "validated": False, "deps_up": 9,  "deps_down": 16, "color": "#6D28D9"},
    {"id": "servicenow",    "name": "ServiceNow ITSM",         "type": "ITSM",          "domain": "SaaS",          "risk": 1.9, "criticality": "LOW",      "vendor": "ServiceNow",  "tech": "Cloud",       "eol": False, "cloud": True,  "validated": False, "deps_up": 44, "deps_down": 8,  "color": "#5B21B6"},
    # Data & Analytics
    {"id": "oracle-db",     "name": "Oracle Database 19c",     "type": "Database",      "domain": "Data",          "risk": 5.9, "criticality": "CRITICAL", "vendor": "Oracle",      "tech": "Oracle DB",   "eol": False, "cloud": False, "validated": True,  "deps_up": 34, "deps_down": 2,  "color": "#0891B2"},
    {"id": "dw-teradata",   "name": "Teradata Data Warehouse",  "type": "Database",     "domain": "Data",          "risk": 4.3, "criticality": "HIGH",     "vendor": "Teradata",    "tech": "Teradata",    "eol": True,  "cloud": False, "validated": False, "deps_up": 18, "deps_down": 4,  "color": "#0E7490"},
    {"id": "tableau",       "name": "Tableau Analytics",        "type": "BI/Analytics", "domain": "Data",          "risk": 1.4, "criticality": "LOW",      "vendor": "Salesforce",  "tech": "Cloud",       "eol": False, "cloud": True,  "validated": False, "deps_up": 6,  "deps_down": 0,  "color": "#155E75"},
    # Infrastructure
    {"id": "active-dir",    "name": "Active Directory",         "type": "IAM",          "domain": "Infrastructure","risk": 5.0, "criticality": "CRITICAL", "vendor": "Microsoft",   "tech": "Windows",     "eol": False, "cloud": False, "validated": False, "deps_up": 117,"deps_down": 2,  "color": "#EA580C"},
    {"id": "vmware",        "name": "VMware vSphere",           "type": "Virtualisation","domain": "Infrastructure","risk": 4.1, "criticality": "HIGH",     "vendor": "Broadcom",    "tech": "ESXi",        "eol": False, "cloud": False, "validated": False, "deps_up": 89, "deps_down": 4,  "color": "#C2410C"},
    {"id": "netapp",        "name": "NetApp Storage",           "type": "Storage",       "domain": "Infrastructure","risk": 3.7, "criticality": "HIGH",     "vendor": "NetApp",      "tech": "ONTAP",       "eol": False, "cloud": False, "validated": False, "deps_up": 67, "deps_down": 0,  "color": "#D97706"},
    # Legacy / High Risk
    {"id": "cobol-batch",   "name": "COBOL Batch Processing",   "type": "Legacy",       "domain": "Legacy",        "risk": 5.8, "criticality": "HIGH",     "vendor": "Internal",    "tech": "COBOL",       "eol": True,  "cloud": False, "validated": True,  "deps_up": 8,  "deps_down": 18, "color": "#7F1D1D"},
    {"id": "mainframe",     "name": "IBM Mainframe z/OS",       "type": "Legacy",       "domain": "Legacy",        "risk": 6.4, "criticality": "CRITICAL", "vendor": "IBM",         "tech": "z/OS",        "eol": False, "cloud": False, "validated": True,  "deps_up": 6,  "deps_down": 22, "color": "#991B1B"},
    # Compliance
    {"id": "veeva-vault",   "name": "Veeva Vault RIM",          "type": "Compliance",   "domain": "Compliance",    "risk": 2.3, "criticality": "MEDIUM",   "vendor": "Veeva",       "tech": "Cloud",       "eol": False, "cloud": True,  "validated": True,  "deps_up": 12, "deps_down": 3,  "color": "#DC2626"},
    {"id": "trackwise",     "name": "TrackWise Quality",         "type": "QMS",         "domain": "Compliance",    "risk": 3.1, "criticality": "MEDIUM",   "vendor": "Sparta",      "tech": "Java",        "eol": False, "cloud": False, "validated": True,  "deps_up": 8,  "deps_down": 6,  "color": "#B91C1C"},
    # Web / Customer
    {"id": "cust-portal",   "name": "Customer Portal (Web)",    "type": "Web",          "domain": "Customer",      "risk": 3.8, "criticality": "HIGH",     "vendor": "Internal",    "tech": "React/Node",  "eol": False, "cloud": True,  "validated": False, "deps_up": 14, "deps_down": 4,  "color": "#0891B2"},
    {"id": "hr-payroll",    "name": "HR Payroll System",         "type": "HR",          "domain": "HR",            "risk": 4.4, "criticality": "HIGH",     "vendor": "SAP",         "tech": "ABAP",        "eol": False, "cloud": False, "validated": False, "deps_up": 18, "deps_down": 6,  "color": "#7C3AED"},
]

# Dependency edges: [source_id, target_id, type, label]
DEPENDENCIES = [
    ["sap-erp",    "oracle-db",   "data",    "Financial data"],
    ["sap-erp",    "api-gateway", "api",     "REST API"],
    ["sap-erp",    "mulesoft",    "message", "Event stream"],
    ["sap-erp",    "active-dir",  "auth",    "SSO/LDAP"],
    ["sap-erp",    "hr-payroll",  "data",    "Employee data"],
    ["oracle-ebs", "oracle-db",   "data",    "Direct DB"],
    ["oracle-ebs", "sap-erp",     "api",     "Finance sync"],
    ["oracle-ebs", "active-dir",  "auth",    "SSO"],
    ["api-gateway","salesforce",  "api",     "CRM sync"],
    ["api-gateway","cust-portal", "api",     "Public API"],
    ["api-gateway","kafka",       "message", "Event routing"],
    ["mulesoft",   "oracle-db",   "data",    "Data sync"],
    ["mulesoft",   "cobol-batch", "legacy",  "Batch trigger"],
    ["mulesoft",   "mainframe",   "legacy",  "CICS calls"],
    ["kafka",      "dw-teradata", "stream",  "Event log"],
    ["kafka",      "mes",         "message", "Production events"],
    ["mes",        "oracle-db",   "data",    "Production data"],
    ["mes",        "scada",       "ot",      "Control signals"],
    ["mes",        "lims",        "api",     "Lab requests"],
    ["scada",      "mes",         "ot",      "Sensor data"],
    ["lims",       "veeva-vault", "api",     "Quality data"],
    ["lims",       "trackwise",   "api",     "Deviations"],
    ["oracle-db",  "vmware",      "infra",   "VM host"],
    ["oracle-db",  "netapp",      "infra",   "Storage"],
    ["dw-teradata","tableau",     "data",    "Reports"],
    ["dw-teradata","vmware",      "infra",   "VM host"],
    ["active-dir", "vmware",      "infra",   "AD auth"],
    ["vmware",     "netapp",      "infra",   "NFS storage"],
    ["cobol-batch","mainframe",   "legacy",  "JCL jobs"],
    ["cobol-batch","oracle-db",   "data",    "Batch output"],
    ["mainframe",  "oracle-db",   "data",    "DB2 bridge"],
    ["workday",    "active-dir",  "auth",    "SSO"],
    ["workday",    "hr-payroll",  "data",    "HR master"],
    ["salesforce", "cust-portal", "api",     "Customer data"],
    ["servicenow", "active-dir",  "auth",    "SSO"],
    ["servicenow", "vmware",      "api",     "CMDB sync"],
    ["hyperion",   "oracle-ebs",  "data",    "Financial data"],
    ["hyperion",   "oracle-db",   "data",    "Direct DB"],
    ["veeva-vault","salesforce",  "api",     "CRM sync"],
    ["hr-payroll", "oracle-db",   "data",    "Payroll DB"],
]

SYSTEM_MAP = {s["id"]: s for s in SYSTEMS}

# ─── Helpers ────────────────────────────────────────────────────────────────

def get_system_or_404(system_id):
    s = SYSTEM_MAP.get(system_id)
    if not s:
        return None, jsonify({"error": "System not found"}), 404
    return s, None, None

def get_deps_for(system_id):
    """Return upstream and downstream dependencies for a system."""
    upstream   = []
    downstream = []
    for src, dst, dep_type, label in DEPENDENCIES:
        if dst == system_id:
            s = SYSTEM_MAP.get(src)
            if s:
                upstream.append({**s, "dep_type": dep_type, "dep_label": label})
        if src == system_id:
            s = SYSTEM_MAP.get(dst)
            if s:
                downstream.append({**s, "dep_type": dep_type, "dep_label": label})
    return upstream, downstream

def compute_impacted(system_id, depth=3):
    """BFS downstream impact traversal."""
    visited = set()
    queue   = [(system_id, 0)]
    impacted = []
    while queue:
        nid, d = queue.pop(0)
        if nid in visited or d > depth:
            continue
        visited.add(nid)
        if nid != system_id:
            s = SYSTEM_MAP.get(nid)
            if s:
                impacted.append({**s, "impact_depth": d})
        for src, dst, dep_type, label in DEPENDENCIES:
            if src == nid and dst not in visited:
                queue.append((dst, d + 1))
    return impacted

# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/systems")
def api_systems():
    domain = request.args.get("domain")
    result = SYSTEMS if not domain else [s for s in SYSTEMS if s["domain"].lower() == domain.lower()]
    return jsonify(result)

@app.route("/api/systems/<system_id>")
def api_system_detail(system_id):
    s, err, code = get_system_or_404(system_id)
    if err:
        return err, code
    up, down = get_deps_for(system_id)
    return jsonify({**s, "upstream": up, "downstream": down})

@app.route("/api/graph")
def api_graph():
    """Return D3-compatible node/link graph data."""
    nodes = [
        {
            "id":          s["id"],
            "name":        s["name"],
            "type":        s["type"],
            "domain":      s["domain"],
            "risk":        s["risk"],
            "criticality": s["criticality"],
            "color":       s["color"],
            "cloud":       s["cloud"],
            "eol":         s["eol"],
            "validated":   s["validated"],
        }
        for s in SYSTEMS
    ]
    links = [
        {"source": src, "target": dst, "type": dep_type, "label": label}
        for src, dst, dep_type, label in DEPENDENCIES
    ]
    return jsonify({"nodes": nodes, "links": links})

@app.route("/api/dashboard")
def api_dashboard():
    total     = len(SYSTEMS)
    high_risk = [s for s in SYSTEMS if s["risk"] >= 6.0]
    med_risk  = [s for s in SYSTEMS if 3.5 <= s["risk"] < 6.0]
    low_risk  = [s for s in SYSTEMS if s["risk"] < 3.5]
    eol_count = sum(1 for s in SYSTEMS if s["eol"])
    cloud_pct = round(sum(1 for s in SYSTEMS if s["cloud"]) / total * 100)
    avg_risk  = round(sum(s["risk"] for s in SYSTEMS) / total, 1)
    undoc     = sum(1 for s in SYSTEMS if not s["validated"])

    # Risk by domain
    domains = {}
    for s in SYSTEMS:
        d = s["domain"]
        if d not in domains:
            domains[d] = {"systems": 0, "risk_sum": 0}
        domains[d]["systems"] += 1
        domains[d]["risk_sum"] += s["risk"]
    domain_risk = [
        {"domain": d, "avg_risk": round(v["risk_sum"] / v["systems"], 1), "count": v["systems"]}
        for d, v in domains.items()
    ]
    domain_risk.sort(key=lambda x: -x["avg_risk"])

    # Monthly trend (simulated history, 12 months)
    trend = []
    base  = 8.2
    for i in range(12):
        base = max(base - random.uniform(0.05, 0.2), 6.8)
        trend.append(round(base + random.uniform(-0.1, 0.1), 2))
    trend[-1] = avg_risk

    return jsonify({
        "total_systems":   total,
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(med_risk),
        "low_risk_count":  len(low_risk),
        "eol_count":       eol_count,
        "cloud_percentage": cloud_pct,
        "avg_risk_score":  avg_risk,
        "undocumented":    undoc,
        "domain_risk":     domain_risk,
        "risk_trend":      trend,
        "high_risk_systems": [
            {k: s[k] for k in ["id","name","type","domain","risk","criticality","deps_down","eol"]}
            for s in sorted(high_risk, key=lambda x: -x["risk"])
        ],
    })

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Run change impact simulation for a given system and change type."""
    data      = request.json or {}
    system_id = data.get("system_id", "sap-erp")
    change    = data.get("change_type", "decommission")
    depth     = int(data.get("depth", 3))

    s, err, code = get_system_or_404(system_id)
    if err:
        return err, code

    time.sleep(0.6)  # simulate AI thinking

    impacted  = compute_impacted(system_id, depth)
    up, down  = get_deps_for(system_id)

    # Risk scoring per change type
    risk_mult = {"decommission": 1.0, "migration": 0.7, "upgrade": 0.5, "integration": 0.6}.get(change, 0.8)

    critical = [i for i in impacted if i["risk"] >= 6.0]
    high     = [i for i in impacted if 4.0 <= i["risk"] < 6.0]
    medium   = [i for i in impacted if i["risk"] < 4.0]

    validated_affected = [i for i in impacted if i["validated"]]
    domains_affected   = list(set(i["domain"] for i in impacted))

    base_cost    = int(s["risk"] * 320000 * risk_mult)
    risk_score   = min(round(s["risk"] * risk_mult + len(critical) * 0.1, 1), 10.0)
    confidence   = min(91 + random.randint(-3, 5), 97)
    est_weeks    = len(impacted) // 4 + 8

    # AI recommendations
    recs = []
    if change == "decommission":
        recs = [
            {"priority": 1, "action": f"Establish data migration plan for {len(down)} downstream integrations", "effort": f"{min(len(down) // 3, 12)} weeks", "color": "#16A34A"},
            {"priority": 2, "action": f"Document and replace {len([i for i in down if not i.get('validated')])} undocumented API connections", "effort": "2–4 weeks", "color": "#2563EB"},
            {"priority": 3, "action": f"Engage GxP compliance team — {len(validated_affected)} validated systems affected", "effort": "4–6 weeks", "color": "#EA580C"} if validated_affected else None,
            {"priority": 4, "action": "Create roll-back plan and freeze window for change execution", "effort": "1 week", "color": "#6B7280"},
        ]
    elif change == "migration":
        recs = [
            {"priority": 1, "action": "Assess cloud-readiness of all downstream services", "effort": "3–4 weeks", "color": "#16A34A"},
            {"priority": 2, "action": "Identify data residency constraints (GxP / GDPR)", "effort": "2 weeks", "color": "#2563EB"},
            {"priority": 3, "action": "Design hybrid integration layer for transition period", "effort": "6–8 weeks", "color": "#EA580C"},
            {"priority": 4, "action": "Plan phased migration wave with parallel-run window", "effort": "4 weeks", "color": "#6B7280"},
        ]
    elif change == "upgrade":
        recs = [
            {"priority": 1, "action": "Run regression test suite across all dependent systems", "effort": "3 weeks", "color": "#16A34A"},
            {"priority": 2, "action": "Check API version compatibility for downstream consumers", "effort": "1 week", "color": "#2563EB"},
            {"priority": 3, "action": "Update documentation in LeanIX with new version metadata", "effort": "1 week", "color": "#6B7280"},
        ]
    elif change == "integration":
        recs = [
            {"priority": 1, "action": "Define canonical data model for integration layer", "effort": "2 weeks", "color": "#16A34A"},
            {"priority": 2, "action": "Map authentication and authorisation flows", "effort": "1 week", "color": "#2563EB"},
            {"priority": 3, "action": "Establish error handling and circuit-breaker patterns", "effort": "2 weeks", "color": "#EA580C"},
        ]
    recs = [r for r in recs if r]

    return jsonify({
        "system":              s,
        "change_type":         change,
        "risk_score":          risk_score,
        "confidence":          confidence,
        "total_impacted":      len(impacted),
        "critical_impacted":   len(critical),
        "high_impacted":       len(high),
        "medium_impacted":     len(medium),
        "domains_affected":    domains_affected,
        "validated_affected":  len(validated_affected),
        "estimated_cost_eur":  base_cost,
        "estimated_weeks":     est_weeks,
        "impacted_systems":    impacted[:20],  # top 20
        "recommendations":     recs,
    })

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").lower()
    if not q:
        return jsonify([])
    results = [
        s for s in SYSTEMS
        if q in s["name"].lower() or q in s["type"].lower() or q in s["domain"].lower() or q in s["vendor"].lower()
    ]
    return jsonify(results[:8])

@app.route("/api/domains")
def api_domains():
    domains = list(set(s["domain"] for s in SYSTEMS))
    return jsonify(sorted(domains))

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════╗")
    print("║   ArchIntel — Enterprise Architecture AI     ║")
    print("║   Demo server running on http://localhost:5003 ║")
    print("╚══════════════════════════════════════════════╝\n")
    app.run(host="0.0.0.0", port=5003, debug=True)
