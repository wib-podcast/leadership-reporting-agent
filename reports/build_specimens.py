#!/usr/bin/env python3
"""Build four five-page WIB leadership-report specimens from fictional data."""

from __future__ import annotations

import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / "specimens"
BRAND_PATH = HERE / "brand.json"
BRAND = json.loads(BRAND_PATH.read_text())
INK = colors.HexColor(BRAND["colors"]["ink"])
PAPER = colors.HexColor(BRAND["colors"]["paper"])
VOLT = colors.HexColor(BRAND["colors"]["volt"])
SIGNAL = colors.HexColor(BRAND["colors"]["signal"])
MUTED = colors.Color(0.38, 0.40, 0.39)
RULE = colors.Color(0.82, 0.82, 0.78)
CARD = colors.Color(0.97, 0.96, 0.93)
PALE = colors.Color(0.92, 0.92, 0.87)
WATCH = colors.Color(0.89, 0.67, 0.22)
WHITE = colors.white
W, H = landscape(A4)
M = 42
MONTHS = ["MAY", "JUN", "JUL", "AUG", "SEP", "OCT* "]

# All records in this file are invented for a podcast screen demo.
CLIENTS = [
    {"name": "Alpha", "program": "Core launch", "health": "ON TRACK", "progress": 88,
     "owner": "Iris Lee", "signal": "API contract signed; pilot scope locked.",
     "blocker": "Partner certification window is not confirmed.", "ticket": "WIB-ALP-214",
     "next": "Confirm pilot acceptance criteria and book certification slot.",
     "trend": [20, 34, 47, 61, 75, 88]},
    {"name": "Lotus", "program": "Payments refresh", "health": "AT RISK", "progress": 76,
     "owner": "Victor Chen", "signal": "Webhook contract tests are ready for sandbox.",
     "blocker": "Gateway sandbox access remains with partner team.", "ticket": "WIB-LOT-087",
     "next": "Escalate sandbox access; run first end-to-end payment test.",
     "trend": [15, 27, 40, 54, 67, 76]},
    {"name": "Pearl", "program": "Member portal", "health": "ON TRACK", "progress": 93,
     "owner": "Priya Shah", "signal": "Core flows passed; release candidate is stable.",
     "blocker": "Accessibility sign-off is pending on the revised focus order.", "ticket": "WIB-PEA-153",
     "next": "Close accessibility review and confirm release checklist.",
     "trend": [23, 37, 52, 66, 81, 93]},
    {"name": "Cedar", "program": "Analytics migration", "health": "WATCH", "progress": 82,
     "owner": "Omar Reed", "signal": "Parity checks pass on 94% of sampled rows.",
     "blocker": "Legacy export exceptions need a signed acceptance threshold.", "ticket": "WIB-CED-066",
     "next": "Review exception sample and sign off the parity threshold.",
     "trend": [18, 31, 45, 59, 72, 82]},
    {"name": "Nova", "program": "Mobile onboarding", "health": "ON TRACK", "progress": 94,
     "owner": "Ella Park", "signal": "Demo experiment shows an 8-point completion lift.",
     "blocker": "Rollout guardrails need Product and Sales agreement.", "ticket": "WIB-NOV-072",
     "next": "Approve rollout guardrails and stage the first 50% cohort.",
     "trend": [21, 36, 52, 68, 83, 94]},
    {"name": "Ember", "program": "CRM consolidation", "health": "AT RISK", "progress": 73,
     "owner": "Jamie Fox", "signal": "Target CRM field map is drafted.",
     "blocker": "Two source systems have no named data owner.", "ticket": "WIB-EMB-033",
     "next": "Name source owners and confirm a migration rehearsal date.",
     "trend": [12, 24, 38, 51, 64, 73]},
]

MONTHLY_HEALTH = [
    ("MAY", 5, 1, 0), ("JUN", 4, 2, 0), ("JUL", 3, 2, 1),
    ("AUG", 3, 1, 2), ("SEP", 3, 1, 2), ("OCT*", 3, 1, 2),
]

ACTION_ITEMS = [
    ("WIB-LOT-087", "Secure gateway sandbox access", "Victor Chen", "26 Oct", "BLOCKED"),
    ("WIB-EMB-033", "Name two CRM source owners", "Jamie Fox", "26 Oct", "OPEN"),
    ("WIB-NOV-072", "Approve 50% rollout guardrails", "Ella Park", "27 Oct", "DECISION"),
    ("WIB-CED-066", "Sign data-parity threshold", "Omar Reed", "28 Oct", "OPEN"),
    ("WIB-PEA-153", "Close accessibility sign-off", "Priya Shah", "29 Oct", "IN REVIEW"),
    ("WIB-ALP-214", "Book partner certification slot", "Iris Lee", "30 Oct", "OPEN"),
]


def mix(a, b, amount):
    return colors.Color(a.red * (1 - amount) + b.red * amount,
                        a.green * (1 - amount) + b.green * amount,
                        a.blue * (1 - amount) + b.blue * amount)


def rect(c, x, top, width, height, fill=None, stroke=None, radius=0):
    c.setFillColor(fill or PAPER)
    c.setStrokeColor(stroke or fill or PAPER)
    c.setLineWidth(0.7)
    y = H - top - height
    if radius:
        c.roundRect(x, y, width, height, radius, fill=1, stroke=bool(stroke))
    else:
        c.rect(x, y, width, height, fill=1, stroke=bool(stroke))


def line(c, x1, top1, x2, top2, color=RULE, width=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, H - top1, x2, H - top2)


def text(c, value, x, top, size=10, color=INK, font="Helvetica", align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    y = H - top - size
    if align == "right":
        c.drawRightString(x, y, str(value))
    elif align == "center":
        c.drawCentredString(x, y, str(value))
    else:
        c.drawString(x, y, str(value))


def wrap_lines(value, width, font, size):
    words = str(value).split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(c, value, x, top, width, size=9.5, leading=13, color=MUTED, font="Helvetica", max_lines=None):
    lines = wrap_lines(value, width, font, size)
    if max_lines:
        lines = lines[:max_lines]
    for i, row in enumerate(lines):
        text(c, row, x, top + i * leading, size, color, font)
    return top + len(lines) * leading


def header(c, report, page, total=5):
    rect(c, 0, 0, W, H, PAPER)
    rect(c, 0, 0, 10, H, INK)
    rect(c, M, 22, 47, 19, VOLT)
    text(c, "WIB *", M + 7, 26, 9, INK, "Helvetica-Bold")
    text(c, "WHAT I BUILT / LEADERSHIP REPORTING", M + 58, 26, 8, INK, "Helvetica-Bold")
    text(c, "SPECIMEN / SYNTHETIC DATA / 20 OCT 2026", W - M, 27, 7.2, MUTED, "Courier", "right")
    line(c, M, 51, W - M, 51, INK, 0.8)
    line(c, M, H - 34, W - M, H - 34, RULE, 0.65)
    text(c, f"{report.upper()}   /   NOT CLIENT REPORTING", M, H - 25, 7.1, MUTED, "Courier")
    text(c, f"{page:02d} / {total:02d}", W - M, H - 25, 7.2, MUTED, "Courier", "right")


def section(c, title, top, subtitle=None, x=M, width=W - 2 * M):
    text(c, title, x, top, 17, INK, "Helvetica-Bold")
    if subtitle:
        text(c, subtitle, x, top + 24, 8.1, MUTED, "Helvetica")
    line(c, x, top + 43, x + width, top + 43, INK, 0.75)
    return top + 54


def tag(c, value, x, top, kind="neutral"):
    fill = PALE
    foreground = INK
    if kind == "risk":
        fill, foreground = mix(PAPER, SIGNAL, 0.20), SIGNAL
    elif kind == "watch":
        fill, foreground = mix(PAPER, WATCH, 0.24), INK
    elif kind == "good":
        fill, foreground = mix(PAPER, VOLT, 0.48), INK
    width = stringWidth(value.upper(), "Courier-Bold", 7) + 14
    rect(c, x, top, width, 16, fill, None, 2)
    text(c, value.upper(), x + 7, top + 4, 7, foreground, "Courier-Bold")
    return width


def status_kind(value):
    return "risk" if value == "AT RISK" else "watch" if value == "WATCH" else "good"


def kpi(c, x, top, width, number, label):
    rect(c, x, top, width, 54, CARD, RULE, 3)
    text(c, number, x + 12, top + 7, 20, INK, "Helvetica-Bold")
    text(c, label.upper(), x + 12, top + 34, 7.2, MUTED, "Courier")


def bullet(c, value, x, top, width, color=INK, size=9):
    rect(c, x, top + 4, 6, 6, VOLT)
    end = paragraph(c, value, x + 14, top, width - 14, size, size + 3, color)
    return end + 5


def draw_donut(c, cx, top_center, radius, parts, labels):
    cy = H - top_center
    start = 90
    for value, color in parts:
        extent = 360 * value / sum(v for v, _ in parts)
        c.setFillColor(color)
        c.setStrokeColor(PAPER)
        c.setLineWidth(1.5)
        c.wedge(cx - radius, cy - radius, cx + radius, cy + radius, startAng=start, extent=extent, fill=1, stroke=1)
        start += extent
    c.setFillColor(PAPER)
    c.circle(cx, cy, radius * 0.56, fill=1, stroke=0)
    text(c, str(sum(v for v, _ in parts)), cx, top_center - 10, 19, INK, "Helvetica-Bold", "center")
    text(c, "CLIENTS", cx, top_center + 10, 6.8, MUTED, "Courier", "center")
    for i, (label, value, color) in enumerate(labels):
        yy = top_center - 24 + i * 19
        rect(c, cx + radius + 18, yy + 2, 8, 8, color)
        text(c, f"{label}  {value}", cx + radius + 32, yy, 8, INK, "Helvetica")


def draw_stacked_monthly(c, x, top, width, height, rows=MONTHLY_HEALTH):
    colors_by = [INK, WATCH, SIGNAL]
    names = ["On track", "Watch", "At risk"]
    left = x + 54
    chartw = width - 70
    rowh = height / len(rows)
    for j, name in enumerate(names):
        xx = x + j * 95
        rect(c, xx, top - 17, 7, 7, colors_by[j])
        text(c, name, xx + 12, top - 20, 7, MUTED)
    for i, (month, good, watch, risk) in enumerate(rows):
        yy = top + i * rowh
        text(c, month, x, yy + 3, 7.2, MUTED, "Courier-Bold")
        vals = [good, watch, risk]
        xx = left
        for value, color in zip(vals, colors_by):
            cellw = chartw * value / 6
            if cellw:
                rect(c, xx, yy, cellw, rowh - 4, color)
                if cellw > 24:
                    text(c, str(value), xx + cellw / 2, yy + 4, 7, PAPER, "Helvetica-Bold", "center")
            xx += cellw
        line(c, left, yy + rowh - 1, left + chartw, yy + rowh - 1, RULE, 0.45)
    for tick in range(7):
        xx = left + chartw * tick / 6
        line(c, xx, top - 2, xx, top + height, mix(PAPER, INK, 0.10), 0.4)
        if tick < 6:
            text(c, MONTHS[tick], left + chartw * (tick + 0.5) / 6, top + height + 4, 6.6, MUTED, "Courier", "center")


def draw_progress_bars(c, x, top, width, clients=CLIENTS, rowh=43):
    for i, cl in enumerate(clients):
        yy = top + i * rowh
        text(c, cl["name"], x, yy, 8.5, INK, "Helvetica-Bold")
        text(c, cl["program"], x + 52, yy, 7.7, MUTED)
        tag(c, cl["health"], x + width - 122, yy - 1, status_kind(cl["health"]))
        bx, by, bw = x + 52, yy + 16, width - 194
        rect(c, bx, by, bw, 8, PALE)
        rect(c, bx, by, bw * cl["progress"] / 100, 8,
             SIGNAL if cl["health"] == "AT RISK" else VOLT if cl["health"] == "WATCH" else INK)
        text(c, f"{cl['progress']}%", x + width - 48, yy + 13, 8, INK, "Helvetica-Bold", "right")


def table(c, x, top, widths, headers, rows, row_height=35, font_size=8):
    total = sum(widths)
    rect(c, x, top, total, 24, INK)
    xx = x
    for col, width in zip(headers, widths):
        text(c, col.upper(), xx + 7, top + 8, 6.7, PAPER, "Courier-Bold")
        xx += width
    yy = top + 24
    for idx, row in enumerate(rows):
        bg = CARD if idx % 2 == 0 else PAPER
        rect(c, x, yy, total, row_height, bg, RULE)
        xx = x
        for i, (value, width) in enumerate(zip(row, widths)):
            cell_text = str(value)
            color = INK
            font = "Helvetica"
            if i == 0:
                font = "Courier-Bold"
                color = INK
            lines = wrap_lines(cell_text, width - 14, font, font_size)
            for j, val in enumerate(lines[:3]):
                text(c, val, xx + 7, yy + 6 + j * (font_size + 2), font_size, color, font)
            xx += width
        yy += row_height
    return yy


def panel(c, x, top, width, height, title, accent=VOLT):
    rect(c, x, top, width, height, CARD, RULE, 3)
    rect(c, x, top, 4, height, accent)
    text(c, title, x + 14, top + 11, 10, INK, "Helvetica-Bold")


def gantt(c, x, top, width, rows):
    labelw = 154
    gridw = width - labelw
    colw = gridw / 6
    for i, month in enumerate(MONTHS):
        rect(c, x + labelw + i * colw, top, colw, 21, INK)
        text(c, month.strip(), x + labelw + (i + 0.5) * colw, top + 6, 6.8, PAPER, "Courier-Bold", "center")
    yy = top + 21
    rh = 18
    for idx, (name, start, end, progress, kind) in enumerate(rows):
        bg = CARD if idx % 2 == 0 else PAPER
        rect(c, x, yy, width, rh, bg, RULE)
        text(c, name, x + 5, yy + 5, 7.1, INK, "Helvetica")
        for i in range(6):
            line(c, x + labelw + i * colw, yy, x + labelw + i * colw, yy + rh, RULE, 0.4)
        totalw = (end - start) * colw
        bx = x + labelw + start * colw + 3
        rect(c, bx, yy + 5, max(totalw - 6, 8), 8, PALE, None, 2)
        fill = SIGNAL if kind == "risk" else WATCH if kind == "watch" else INK if progress >= 100 else VOLT
        rect(c, bx, yy + 5, max((totalw - 6) * min(progress, 100) / 100, 5), 8, fill, None, 2)
        if end < 6:
            px = x + labelw + end * colw
            c.setFillColor(SIGNAL if kind == "risk" else INK)
            p = c.beginPath()
            p.moveTo(px, H - (yy + 4))
            p.lineTo(px + 4, H - (yy + 9))
            p.lineTo(px, H - (yy + 14))
            p.lineTo(px - 4, H - (yy + 9))
            p.close()
            c.drawPath(p, fill=1, stroke=0)
        yy += rh
    for i in range(7):
        xx = x + labelw + i * colw
        line(c, xx, top, xx, yy, RULE, 0.45)
    return yy


def page_cover(c, report, code, title, subtitle, metrics, story, insight_title, insight_lines):
    header(c, report, 1)
    text(c, "SPECIMEN REPORT / 6-MONTH PORTFOLIO VIEW", M, 83, 8, MUTED, "Courier-Bold")
    text(c, title, M, 106, 28, INK, "Helvetica-Bold")
    paragraph(c, subtitle, M, 145, 470, 10.3, 15, MUTED)
    rect(c, W - 250, 82, 208, 105, INK, None, 4)
    text(c, "BUILD TICKET", W - 232, 96, 7, PAPER, "Courier-Bold")
    text(c, code, W - 232, 116, 16, VOLT, "Courier-Bold")
    text(c, "IN DEMO / SYNTHETIC", W - 232, 151, 7, PAPER, "Courier")
    gap = 10
    kw = (W - 2 * M - gap * 3) / 4
    for i, (number, label) in enumerate(metrics):
        kpi(c, M + i * (kw + gap), 204, kw, number, label)
    panel(c, M, 278, 380, 119, "What this report tells you", VOLT)
    paragraph(c, story, M + 15, 308, 350, 9.2, 13, INK)
    panel(c, M + 399, 278, W - 2 * M - 399, 119, insight_title, SIGNAL)
    yy = 307
    for item in insight_lines:
        yy = bullet(c, item, M + 414, yy, W - 2 * M - 429, size=8.5)
    text(c, "REPORTING BASIS", M, 425, 7, MUTED, "Courier-Bold")
    line(c, M, 440, W - M, 440, RULE)
    paragraph(c, "Synthetic-only sample using placeholder clients Alpha, Lotus, Pearl, Cedar, Nova and Ember. Six-month trend is May-October 2026; October values are month-to-date through 20 October. Action dates are illustrative planning dates for 26-30 October.", M, 453, W - 2 * M, 8.5, 12, MUTED)
    c.showPage()


def client_report(path):
    c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
    report = "Client status"
    page_cover(c, report, "WIB-101", "Client-wise status", "Portfolio health, delivery signals, open risks and next-week actions by placeholder client.",
               [("06", "Clients"), ("03", "On track"), ("01", "Watch"), ("02", "At risk")],
               "A relationship-level view for account leads and delivery owners. It answers where each client stands, what changed over the six-month window, and which owner action will move the work next.",
               "Leadership readout", ["Four of six programs have no red status.", "Lotus and Ember need named owners or external dates.", "No actual customer records or messages are used."])

    header(c, report, 2)
    y = section(c, "Portfolio health and movement", 72, "Current status mix and six-month progress trend; October is month-to-date.")
    panel(c, M, y, 286, 230, "Status distribution", VOLT)
    draw_donut(c, M + 83, y + 133, 54, [(3, INK), (1, WATCH), (2, SIGNAL)],
               [("On track", 3, INK), ("Watch", 1, WATCH), ("At risk", 2, SIGNAL)])
    paragraph(c, "Status is an editorial summary of delivery evidence, dependency timing and ownership clarity. It is not a probability score.", M + 17, y + 196, 250, 8.2, 11, MUTED)
    panel(c, M + 301, y, W - 2 * M - 301, 230, "Progress by client", SIGNAL)
    draw_progress_bars(c, M + 316, y + 36, W - 2 * M - 331, rowh=28)
    text(c, "Six-month progress is directional and synthetic; it does not represent earned value.", M + 316, y + 207, 7.4, MUTED)
    text(c, "HOW TO READ IT", M, y + 252, 7, MUTED, "Courier-Bold")
    paragraph(c, "The portfolio is late-stage overall. Progress percentages summarize modeled work completion; health tags show current delivery attention. A high completion percentage does not cancel a blocked external dependency.", M, y + 268, W - 2 * M, 9, 13, INK)
    c.showPage()

    header(c, report, 3)
    y = section(c, "Client-by-client snapshot", 72, "Evidence, delivery position and what the status means for the relationship.")
    cardw = (W - 2 * M - 18) / 2
    cardh = 133
    for idx, cl in enumerate(CLIENTS):
        col, row = idx % 2, idx // 2
        x = M + col * (cardw + 18)
        top = y + row * (cardh + 13)
        panel(c, x, top, cardw, cardh, f"{cl['name']} / {cl['program']}", SIGNAL if cl["health"] == "AT RISK" else VOLT)
        tag(c, cl["health"], x + cardw - 112, top + 9, status_kind(cl["health"]))
        text(c, f"{cl['progress']}% complete", x + 14, top + 35, 8.2, INK, "Helvetica-Bold")
        text(c, f"Relationship owner: {cl['owner']}", x + 14, top + 52, 7.6, MUTED)
        paragraph(c, cl["signal"], x + 14, top + 69, cardw - 28, 8.3, 11, INK)
        text(c, f"NEXT: {cl['next']}", x + 14, top + 108, 7.3, MUTED, "Helvetica-Bold")
    c.showPage()

    header(c, report, 4)
    y = section(c, "Risks, dependencies and decisions", 72, "Open items that can change client confidence or delivery dates.")
    rows = []
    for cl in CLIENTS:
        if cl["health"] != "ON TRACK":
            rows.append((cl["ticket"], cl["name"] + " / " + cl["blocker"], cl["owner"], "26-28 Oct", cl["health"]))
    table(c, M, y, [84, 302, 105, 78, 89], ["Ticket", "Risk or dependency", "Owner", "Target", "Health"], rows, 42, 7.7)
    panel(c, M, y + 243, 330, 134, "Decision requests", SIGNAL)
    yy = y + 272
    for item in ["Lotus: partner lead confirms sandbox access date.", "Cedar: sponsor accepts the 6% exception sample or requests remediation.", "Ember: Sales Ops names owners for both source systems."]:
        yy = bullet(c, item, M + 14, yy, 300, size=8.2)
    panel(c, M + 346, y + 243, W - 2 * M - 346, 134, "Client communication watch", VOLT)
    paragraph(c, "Keep client updates evidence-led: state the owner, next checkpoint and what would move the date. Avoid calling a dependency resolved until the named partner or client owner confirms it.", M + 361, y + 274, W - 2 * M - 376, 8.7, 12, INK)
    c.showPage()

    header(c, report, 5)
    y = section(c, "Next week / client action plan", 72, "Planning window: 26-30 October 2026. Dates are illustrative demo commitments.")
    rows = [(a[0], a[1], a[2], a[3], a[4]) for a in ACTION_ITEMS]
    table(c, M, y, [88, 285, 112, 78, 86], ["Ticket", "Action", "Owner", "Due", "State"], rows, 39, 7.6)
    panel(c, M, y + 286, W - 2 * M, 94, "What should be true by Friday", VOLT)
    xx = M + 16
    for i, item in enumerate(["Lotus has a dated sandbox path.", "Ember has two named data owners.", "Nova guardrails are recorded.", "Pearl has a closed accessibility checklist."]):
        col = i % 2
        row = i // 2
        bullet(c, item, xx + col * 345, y + 316 + row * 25, 320, size=8.2)
    paragraph(c, "Source note: all clients, signals, percentages, owners, ticket IDs and dates are invented. This report is a presentation specimen, not a client communication.", M, y + 399, W - 2 * M, 7.8, 11, MUTED)
    c.showPage()
    c.save()


def timeline_report(path):
    c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
    report = "Timeline review"
    page_cover(c, report, "WIB-102", "Timeline-wise delivery", "A cross-client schedule view that exposes milestone dates, dependency paths, and forecast confidence.",
               [("18", "Milestone lanes"), ("06", "Programs"), ("04", "Next-week gates"), ("02", "Critical risks")],
               "This report tells a program lead where the work sits on the calendar, which gates are complete, and which dependencies can move a launch date. It separates completed historical phases from the forward plan.",
               "Schedule signal", ["Lotus sandbox access is on the critical path.", "Ember ownership must precede migration rehearsal.", "Dates are planning examples, not client commitments."])

    header(c, report, 2)
    y = section(c, "Six-month program Gantt", 72, "May-October 2026 / October is month-to-date; bars show phase completion at a glance.")
    tasks = []
    phase_map = {
        "Alpha": [("Design", 0, 1.2, 100, "good"), ("Build + API", 1.1, 3.8, 100, "good"), ("Pilot + cert", 3.8, 6, 70, "watch")],
        "Lotus": [("Design", 0, 1.1, 100, "good"), ("Payment build", 1.1, 3.5, 90, "good"), ("Sandbox + SIT", 3.5, 6, 45, "risk")],
        "Pearl": [("Discovery", 0, 1, 100, "good"), ("Portal build", 1, 3.7, 100, "good"), ("A11y + release", 3.7, 6, 85, "good")],
        "Cedar": [("Data mapping", 0, 1.3, 100, "good"), ("Migration + QA", 1.3, 4.1, 90, "good"), ("Parity sign-off", 4.1, 6, 60, "watch")],
        "Nova": [("Research", 0, 1.1, 100, "good"), ("Build + experiment", 1.1, 4, 100, "good"), ("Rollout", 4, 6, 76, "good")],
        "Ember": [("Field inventory", 0, 1.4, 100, "good"), ("CRM mapping", 1.4, 4, 80, "good"), ("Owners + rehearsal", 4, 6, 42, "risk")],
    }
    for cl in CLIENTS:
        for phase, start, end, progress, kind in phase_map[cl["name"]]:
            tasks.append((f"{cl['name']} / {phase}", start, end, progress, kind))
    end = gantt(c, M, y, W - 2 * M, tasks)
    text(c, "COMPLETED", M, end + 13, 7, MUTED, "Courier-Bold")
    rect(c, M + 74, end + 15, 8, 8, INK)
    text(c, "IN PROGRESS", M + 91, end + 13, 7, MUTED, "Courier-Bold")
    rect(c, M + 177, end + 15, 8, 8, VOLT)
    text(c, "DEPENDENCY RISK", M + 194, end + 13, 7, MUTED, "Courier-Bold")
    rect(c, M + 296, end + 15, 8, 8, SIGNAL)
    panel(c, M, end + 36, W - 2 * M, 46, "Reading the schedule", VOLT)
    paragraph(c, "The final bar in each client lane is the nearest release gate. A red segment marks a dependency with an unconfirmed owner/date; it does not mean the whole program has stopped.", M + 14, end + 57, W - 2 * M - 28, 8.1, 10, INK)
    c.showPage()

    header(c, report, 3)
    y = section(c, "Milestone ledger", 72, "Date, confidence, predecessor and ticket for the next meaningful delivery gate.")
    milestone_rows = [
        ("Alpha", "Partner certification slot", "30 Oct", "Medium", "Pilot scope", "WIB-ALP-214"),
        ("Lotus", "Sandbox credentials + first SIT", "26-30 Oct", "Low", "Partner access", "WIB-LOT-087"),
        ("Pearl", "Accessibility sign-off", "29 Oct", "High", "Focus-order review", "WIB-PEA-153"),
        ("Cedar", "Parity threshold accepted", "28 Oct", "Medium", "Exception sample", "WIB-CED-066"),
        ("Nova", "50% cohort approval", "27 Oct", "Medium", "Rollout guardrails", "WIB-NOV-072"),
        ("Ember", "Source owners assigned", "26 Oct", "Low", "Data stewardship", "WIB-EMB-033"),
    ]
    table(c, M, y, [62, 206, 82, 76, 146, 94], ["Client", "Milestone", "Target", "Confidence", "Predecessor", "Ticket"], milestone_rows, 43, 7.3)
    panel(c, M, y + 315, 334, 88, "Confidence guide", VOLT)
    paragraph(c, "High: owner and predecessor are confirmed. Medium: one review or slot remains. Low: external access or ownership is still open.", M + 14, y + 344, 304, 8.5, 12, INK)
    panel(c, M + 350, y + 315, W - 2 * M - 350, 88, "Date discipline", SIGNAL)
    paragraph(c, "Carry forecast changes with a reason, source and new owner date. Do not move a milestone silently when a dependency slips.", M + 364, y + 344, W - 2 * M - 378, 8.5, 12, INK)
    c.showPage()

    header(c, report, 4)
    y = section(c, "Critical path and schedule exposure", 72, "Two dependency chains have the highest likelihood of moving downstream dates.")
    chain_rows = [
        ("LOTUS", "Partner sandbox access", "Webhook SIT", "Payment UAT", "Cutover rehearsal", "HIGH"),
        ("EMBER", "Name data owners", "Approve field map", "Migration rehearsal", "Parity sign-off", "HIGH"),
        ("CEDAR", "Review exception rows", "Accept threshold", "Backfill run", "Data cutover", "MED"),
        ("PEARL", "Close focus-order review", "A11y sign-off", "Release checklist", "Release", "LOW"),
    ]
    table(c, M, y, [62, 145, 133, 132, 131, 63], ["Path", "Gate 1", "Gate 2", "Gate 3", "Gate 4", "Exposure"], chain_rows, 48, 7.1)
    panel(c, M, y + 241, 353, 136, "Schedule recovery options", SIGNAL)
    yy = y + 270
    for item in ["Lotus: set a partner escalation time; use a stubbed sandbox only for internal contract checks.", "Ember: assign interim data stewards so mapping review can start while ownership is formalized.", "Cedar: time-box the exception review and record accept/remediate criteria."]:
        yy = bullet(c, item, M + 14, yy, 325, size=8.1)
    panel(c, M + 369, y + 241, W - 2 * M - 369, 136, "Forecast summary", VOLT)
    paragraph(c, "The portfolio schedule is recoverable if the two HIGH exposure gates receive owner/date decisions early in the planning week. Pearl and Nova have nearer-term approval gates that can close without new build work.", M + 384, y + 271, W - 2 * M - 399, 8.6, 12, INK)
    c.showPage()

    header(c, report, 5)
    y = section(c, "Next-week schedule / 26-30 October", 72, "Sequence the decisions first, then protect test and release windows.")
    rows = [
        ("Mon 26", "Lotus sandbox access; Ember data owners", "Partner lead / Jamie Fox", "WIB-LOT-087 / EMB-033"),
        ("Tue 27", "Nova rollout guardrails; start 50% cohort prep", "Product + Sales / Ella Park", "WIB-NOV-072"),
        ("Wed 28", "Cedar parity threshold; Alpha certification slot", "Omar Reed / Iris Lee", "WIB-CED-066 / ALP-214"),
        ("Thu 29", "Pearl accessibility sign-off and release check", "Priya Shah", "WIB-PEA-153"),
        ("Fri 30", "Review forecast changes; publish next gate list", "Program lead", "WSR-2026-43"),
    ]
    table(c, M, y, [73, 293, 204, 148], ["Day", "Planned gate", "Suggested owner", "Ticket(s)"], rows, 44, 7.7)
    panel(c, M, y + 270, W - 2 * M, 104, "Pending next week", SIGNAL)
    yy = y + 300
    for item in ["Partner access date for Lotus.", "Formal stewardship names for Ember source data.", "Written go/no-go guardrails for Nova rollout."]:
        yy = bullet(c, item, M + 16 + (0 if yy < y + 350 else 360), yy if yy < y + 350 else y + 300, 325, size=8.2)
    paragraph(c, "Synthetic schedule only. Reconcile target dates with Jira and owner confirmations before using this layout with live program data.", M, y + 392, W - 2 * M, 7.8, 11, MUTED)
    c.showPage()
    c.save()


def wsr_report(path):
    c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
    report = "Weekly status report"
    page_cover(c, report, "WIB-103", "Weekly status report", "A leadership-ready weekly readout: health, movement, risks, decisions and the work planned next week.",
               [("06", "Programs"), ("03", "On track"), ("03", "Need attention"), ("06", "Open actions")],
               "The WSR distinguishes trend from current state. It surfaces what changed, where leadership attention is needed, which decisions unblock delivery, and who owns the next checkpoint.",
               "Executive signal", ["Progress is late-stage, but two critical paths remain exposed.", "The most useful asks are owners and dates, not broad escalation.", "Numbers and narrative are fictional demo content."])

    header(c, report, 2)
    y = section(c, "Portfolio health trend", 72, "Program counts by status across the six-month window; each month totals six clients.")
    panel(c, M, y, W - 2 * M, 259, "Monthly health distribution", VOLT)
    draw_stacked_monthly(c, M + 20, y + 49, W - 2 * M - 40, 166)
    paragraph(c, "The status mix shifted from mostly on-track in May to three programs requiring watch or risk attention by July. The mix has held steady since August; the work now is dependency closure and decision follow-through.", M + 18, y + 229, W - 2 * M - 36, 8.5, 12, INK)
    panel(c, M, y + 279, 355, 103, "What moved this week", SIGNAL)
    yy = y + 307
    for item in ["Pearl reached 93%; accessibility sign-off is the last release gate.", "Lotus integration tests remain blocked by partner sandbox access.", "Nova experiment result is ready for a rollout decision."]:
        yy = bullet(c, item, M + 15, yy, 325, size=8)
    panel(c, M + 371, y + 279, W - 2 * M - 371, 103, "What did not change", VOLT)
    paragraph(c, "Cedar still needs a signed parity threshold. Ember still needs two source owners. Keep both on the leadership action list until evidence changes.", M + 386, y + 308, W - 2 * M - 401, 8.4, 12, INK)
    c.showPage()

    header(c, report, 3)
    y = section(c, "Workstream and client scorecard", 72, "Separate delivery progress from the decision or dependency that needs help.")
    draw_progress_bars(c, M, y + 8, W - 2 * M)
    panel(c, M, y + 286, 355, 96, "Delivery pulse", VOLT)
    paragraph(c, "Four programs are on track or watch with a near-term closure path. Lotus and Ember carry the most material schedule exposure. Pearl and Nova have decision gates that can close with clear review ownership.", M + 15, y + 316, 325, 8.7, 12, INK)
    panel(c, M + 371, y + 286, W - 2 * M - 371, 96, "Leadership attention", SIGNAL)
    paragraph(c, "Ask each accountable lead for one owner, one date and one evidence checkpoint. Keep status green only when the next gate is supported by a named owner and a dated dependency.", M + 386, y + 316, W - 2 * M - 401, 8.7, 12, INK)
    c.showPage()

    header(c, report, 4)
    y = section(c, "Risks and decisions for the connect", 72, "A short decision log that can be read aloud in a leadership meeting.")
    risk_rows = [
        ("R1 / Lotus", "Sandbox access no date", "Partner lead", "Name escalation owner + date", "HIGH"),
        ("R2 / Ember", "Two source owners missing", "Sales Ops", "Appoint interim stewards", "HIGH"),
        ("D1 / Nova", "Rollout guardrails open", "Product + Sales", "Approve 50% cohort criteria", "DECIDE"),
        ("D2 / Cedar", "6% export exceptions", "Client sponsor", "Accept or remediate threshold", "DECIDE"),
        ("R3 / Pearl", "Focus-order sign-off pending", "Design QA", "Close accessibility checklist", "MED"),
    ]
    table(c, M, y, [94, 185, 112, 222, 105], ["Ref", "Evidence / gap", "Owner", "Leadership ask", "Priority"], risk_rows, 42, 7.4)
    panel(c, M, y + 250, W - 2 * M, 94, "Suggested WSR talk track", VOLT)
    paragraph(c, "Three programs are on track, one is on watch and two are at risk. The two risks are actionable: Lotus needs a dated partner sandbox path; Ember needs data owners. Today we need two named owners, two dates and a recorded Nova rollout decision.", M + 16, y + 279, W - 2 * M - 32, 9, 13, INK)
    c.showPage()

    header(c, report, 5)
    y = section(c, "Next-week commitments and deck outline", 72, "Use the same five-part structure in the weekly leadership connect deck.")
    rows = [(a[0], a[1], a[2], a[3], a[4]) for a in ACTION_ITEMS]
    table(c, M, y, [87, 283, 105, 77, 88], ["Ticket", "Commitment", "Owner", "Due", "State"], rows, 37, 7.4)
    panel(c, M, y + 274, 335, 111, "WSR deck / 5 slides", VOLT)
    yy = y + 301
    for item in ["Portfolio snapshot and trend", "What changed since last connect", "Top risks and dependency paths", "Decisions required today", "Owners, due dates and next checkpoint"]:
        yy = bullet(c, item, M + 14, yy, 305, size=7.8)
    panel(c, M + 351, y + 274, W - 2 * M - 351, 111, "Definition of done", SIGNAL)
    paragraph(c, "Every action has a ticket or traceable reference, one owner, a date and an evidence checkpoint. Leave unknown values explicitly marked as pending instead of filling them with a guess.", M + 366, y + 305, W - 2 * M - 381, 8.4, 12, INK)
    c.showPage()
    c.save()


def product_sales_report(path):
    c = canvas.Canvas(str(path), pagesize=(W, H), pageCompression=1)
    report = "Product x Sales"
    page_cover(c, report, "WIB-104", "Product x Sales connect", "A recurring standup brief that connects customer demand, product readiness, commercial motion and decisions.",
               [("12", "Demo requests"), ("06", "Qualified"), ("03", "Pilot-ready"), ("02", "Decisions")],
               "This report gives Product and Sales a shared view of which customer problems are repeatable, which features are ready to show, what proof is missing, and what follow-up belongs to each team.",
               "Connect focus", ["Nova onboarding lift is a demo signal, not a validated claim.", "Lotus and Ember need data/partner prerequisites.", "Keep customer language and product evidence linked."])

    header(c, report, 2)
    y = section(c, "Demand-to-delivery funnel", 72, "Illustrative requests across six placeholder accounts; stage counts are synthetic.")
    panel(c, M, y, 365, 255, "Opportunity funnel", VOLT)
    stages = [("Requests", 12), ("Qualified", 6), ("Solution fit", 4), ("Pilot-ready", 3), ("Shipped", 2)]
    maxv = 12
    for i, (name, value) in enumerate(stages):
        yy = y + 41 + i * 38
        text(c, name, M + 17, yy + 3, 8.2, INK)
        bw = 214 * value / maxv
        fill = [INK, INK, WATCH, VOLT, SIGNAL][i]
        rect(c, M + 111, yy, bw, 20, fill, None, 2)
        text(c, str(value), M + 111 + bw + 10, yy + 5, 8, INK, "Helvetica-Bold")
        text(c, f"{value / maxv:.0%}", M + 337, yy + 5, 7.4, MUTED, "Courier", "right")
    panel(c, M + 382, y, W - 2 * M - 382, 255, "Interpretation", SIGNAL)
    yy = y + 39
    for item in ["Half of the modeled requests qualify for discovery.", "Three use cases are ready for a structured pilot conversation.", "Two shipped capabilities have a demo proof point.", "Do not treat funnel counts as bookings or revenue."]:
        yy = bullet(c, item, M + 398, yy, W - 2 * M - 414, size=8.6)
    text(c, "DEMO PROOF POINT", M + 398, y + 194, 7, MUTED, "Courier-Bold")
    paragraph(c, "Nova: onboarding completion increased by 8 percentage points in a fictional experiment. Confirm cohort size, guardrails and measurement window before using externally.", M + 398, y + 211, W - 2 * M - 414, 8, 11, INK)
    panel(c, M, y + 275, W - 2 * M, 90, "Shared qualification questions", VOLT)
    paragraph(c, "Who experiences the problem? What evidence shows frequency or impact? Which product capability addresses it? What is the smallest safe pilot? Who owns the next customer follow-up?", M + 16, y + 307, W - 2 * M - 32, 9, 13, INK)
    c.showPage()

    header(c, report, 3)
    y = section(c, "Feature readiness and account fit", 72, "A simple readiness matrix prevents promising features before evidence and owners are in place.")
    fit_rows = [
        ("Nova", "Guided onboarding", "94%", "8-point demo lift", "Guardrails review", "READY FOR PILOT"),
        ("Pearl", "Accessible portal", "93%", "Core flow pass", "A11y sign-off", "CONDITIONAL"),
        ("Alpha", "Launch API", "88%", "Contract signed", "Cert slot", "CONDITIONAL"),
        ("Lotus", "Payment refresh", "76%", "Webhook tests ready", "Sandbox access", "BLOCKED"),
        ("Cedar", "Analytics export", "82%", "94% sampled parity", "Threshold sign-off", "CONDITIONAL"),
        ("Ember", "CRM consolidation", "73%", "Field map drafted", "Source owners", "BLOCKED"),
    ]
    table(c, M, y, [60, 125, 58, 160, 145, 115], ["Account", "Use case", "Done", "Evidence", "Missing proof", "Sales motion"], fit_rows, 42, 7.1)
    panel(c, M, y + 300, 355, 99, "Safe language", VOLT)
    paragraph(c, "Say 'pilot-ready pending guardrails' when the experiment is promising but thresholds are not signed. Say 'blocked on partner access' when the customer cannot test yet.", M + 14, y + 330, 326, 8.5, 12, INK)
    panel(c, M + 371, y + 300, W - 2 * M - 371, 99, "Evidence rule", SIGNAL)
    paragraph(c, "Link each commercial claim to a dated product artifact, experiment result or owner-confirmed customer note. Label unsupported items as hypotheses.", M + 386, y + 330, W - 2 * M - 401, 8.5, 12, INK)
    c.showPage()

    header(c, report, 4)
    y = section(c, "Meeting notes, decisions and follow-ups", 72, "Convert recurring standup discussion into owners, dates and proof points.")
    note_rows = [
        ("Product", "Nova rollout guardrails", "Decision", "Ella Park", "27 Oct", "WIB-NOV-072"),
        ("Sales", "Lotus sandbox escalation path", "Dependency", "Victor Chen", "26 Oct", "WIB-LOT-087"),
        ("Product", "Pearl accessibility release gate", "Review", "Priya Shah", "29 Oct", "WIB-PEA-153"),
        ("Sales Ops", "Ember source-data ownership", "Decision", "Jamie Fox", "26 Oct", "WIB-EMB-033"),
        ("Product", "Cedar parity threshold", "Decision", "Omar Reed", "28 Oct", "WIB-CED-066"),
    ]
    table(c, M, y, [78, 182, 76, 100, 69, 108], ["Team", "Topic", "Type", "Owner", "Due", "Ticket"], note_rows, 43, 7.2)
    panel(c, M, y + 253, W - 2 * M, 124, "Decisions to make in the room", SIGNAL)
    yy = y + 283
    for item in ["Nova: approve or revise the first 50% rollout cohort and stop conditions.", "Cedar: accept the remaining exception sample or fund targeted remediation.", "Ember: name interim data stewards to unblock field mapping."]:
        yy = bullet(c, item, M + 15, yy, W - 2 * M - 30, size=8.4)
    c.showPage()

    header(c, report, 5)
    y = section(c, "Next-week standup / 26-30 October", 72, "A 30-minute agenda and handoff-ready action list for Product and Sales.")
    agenda = [
        ("00-05", "Customer evidence since last connect", "Sales", "One customer quote or linked note per signal"),
        ("05-12", "Pilot and release readiness", "Product", "Show readiness matrix; call out missing proof"),
        ("12-20", "Decisions: Nova / Cedar / Ember", "Both", "Record decision, owner and revisit date"),
        ("20-26", "Blocked customer paths: Lotus / Alpha", "Sales", "Name partner owner and escalation checkpoint"),
        ("26-30", "Read back actions", "Facilitator", "Confirm tickets, dates and next meeting"),
    ]
    table(c, M, y, [65, 204, 82, 262], ["Time", "Agenda", "Lead", "Meeting output"], agenda, 43, 7.5)
    panel(c, M, y + 260, 355, 116, "Expected outputs", VOLT)
    yy = y + 289
    for item in ["Updated feature-readiness matrix", "Two explicit commercial/product decisions", "Owner and date for every blocked path", "Customer-safe demo claims"]:
        yy = bullet(c, item, M + 14, yy, 325, size=7.8)
    panel(c, M + 371, y + 260, W - 2 * M - 371, 116, "Data note", SIGNAL)
    paragraph(c, "All account names, metrics, requests, meeting notes and ticket IDs are fabricated. No transcript, inbox or CRM was read for this specimen.", M + 386, y + 293, W - 2 * M - 401, 8.6, 12, INK)
    c.showPage()
    c.save()


def write_specimen_data():
    data = {
        "metadata": {
            "synthetic": True,
            "period": "May-October 2026 (October month-to-date through 2026-10-20)",
            "report_date": "2026-10-20",
            "planning_week": {"start": "2026-10-26", "end": "2026-10-30"},
            "warning": "Every client, owner, ticket, metric, signal and date is invented for a podcast showcase. Never treat as actual client status.",
        },
        "clients": CLIENTS,
        "monthly_health_counts": [
            {"month": month, "on_track": good, "watch": watch, "at_risk": risk}
            for month, good, watch, risk in MONTHLY_HEALTH
        ],
        "actions": [
            {"ticket": ticket, "action": action, "owner": owner, "due": due, "state": state}
            for ticket, action, owner, due, state in ACTION_ITEMS
        ],
        "product_sales_funnel": [
            {"stage": name, "count": count}
            for name, count in [("Requests", 12), ("Qualified", 6), ("Solution fit", 4), ("Pilot-ready", 3), ("Shipped", 2)]
        ],
    }
    (HERE / "specimen-data.json").write_text(json.dumps(data, indent=2) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_specimen_data()
    client_report(OUT / "wib-client-status-specimen.pdf")
    timeline_report(OUT / "wib-timeline-delivery-specimen.pdf")
    wsr_report(OUT / "wib-weekly-status-report-specimen.pdf")
    product_sales_report(OUT / "wib-product-sales-connect-specimen.pdf")
    print("Created four synthetic five-page reports in", OUT)


if __name__ == "__main__":
    main()
