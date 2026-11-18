#!/usr/bin/env python3
"""Front page: 18 November 2026, with three drawn scenes, eight briefs, the rest of the day and a dot map."""
import subprocess
import sys

W = H = 1024
PAPER = "#f6f1e6"
INK = "#141414"
NAVY = "#101a2b"
GREY = "#6a6f78"
RULE = "#1c1c1c"
THIN = "#c9c1b1"

CAT = {
    "MIDDLE EAST": "#b3341f", "EUROPE": "#4a2f7a", "ASIA-PACIFIC": "#1d6b4a",
    "BUSINESS": "#1f4e79", "HEALTH": "#8a1f4a", "CYBER": "#2b2f6b",
    "AMERICAS": "#5a6b1f", "AFRICA": "#7a4a12", "SPORT": "#146b6b",
}

LEADS = [
    ("1", "MIDDLE EAST", "US strikes Iran's Qeshm Island", "Third attack on US sites in five days; tankers hit mines in Hormuz."),
    ("2", "EUROPE", "Crimea Bridge road arch destroyed", "Kyiv presses deep strikes; Moscow promises a response."),
    ("3", "ASIA-PACIFIC", "Quad leaders vow maritime and cyber pact", "Manila summit: Trump, Modi, Albanese and Takaichi."),
]

GRID = [
    ("4", "BUSINESS", "Huang seeks Nvidia job back", "Revenue $115.8bn as he asks to return."),
    ("5", "HEALTH", "US loses measles elimination status", "First loss in 26 years, PAHO says."),
    ("6", "MIDDLE EAST", "Gaza truce warned it may collapse", "Board of Peace urges action as strikes resume."),
    ("7", "CYBER", "Outages and hacks hit major sites", "Microsoft 365 down; BBC, IKEA, Air France hit."),
    ("8", "AMERICAS", "Peltola wins Alaska Senate race", "Democrat holds the seat in a tight count."),
    ("9", "AMERICAS", "Salvadoran troops battle Haiti gangs", "Haitians rally behind Bukele as deployment widens."),
    ("10", "MIDDLE EAST", "Knesset elects speaker opposed to Netanyahu", "Eisenkot loses the vote 66-52 to Kahana."),
    ("11", "AFRICA", "South Africa summons Nigeria's envoy", "Diplomatic demarche over social media remarks."),
]

ALSO = [
    "Japan PM Takaichi meets Trump before China-Russia summit",
    "Seoul's Lee says he is invited to Tokyo in January",
    "Bahraini rights activist Nabeel Rajab dies at 62",
    "Ecuador fishermen sue Washington over drone strike",
    "Rare contact with isolated Awa people in Brazil",
    "Pakistani man sentenced to 27 years over murder plot",
    "Kuwait intercepts hostile drones near the Gulf",
    "Rubio says no imminent threat to the US from Iran",
    "Qaani arrives in Iraq to ease militia tensions",
    "Japan lose 2-1 to Paraguay in Moriyasu's farewell",
    "Met museum opens first show on postwar Okinawa",
    "Tokyo drafts dual bus pricing for visitors",
    "Mongolia's president says he will step down over bribery claims",
    "APEC leaders gather in Shenzhen for their summit",
    "US and Mexico agree to reopen Texas crossings",
    "Bangladesh says India cannot dictate Hasina's return",
    "Waterspouts recorded over San Francisco Bay",
]

DOTS = {"1": (56, 26.5), "2": (34.5, 45), "3": (121, 14.6), "4": (-122, 37.4), "5": (-77, 38.9),
        "6": (34.3, 31.4), "7": (-0.1, 51.5), "8": (-149, 61.2), "9": (-72.3, 18.5),
        "10": (106.9, 47.9), "11": (28.2, -25.7)}


def wrap(text, limit):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= limit:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def scene(kind, x, y, w, h):
    s = [f'<g clip-path="url(#c{kind}{x})">']
    s.append(f'<defs><clipPath id="c{kind}{x}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>')
    if kind == "port":
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#101a24"/>')
        s.append(f'<rect x="{x}" y="{y+h*0.68}" width="{w}" height="{h*0.32}" fill="#0a121a"/>')
        # dock crane
        s.append(f'<path d="M{x+w*0.06} {y+h*0.68} l0 -{h*0.42}" stroke="#8795a1" stroke-width="5"/>')
        s.append(f'<path d="M{x+w*0.06} {y+h*0.30} l{w*0.20} 0" stroke="#8795a1" stroke-width="5"/>')
        s.append(f'<path d="M{x+w*0.26} {y+h*0.30} l-{w*0.08} {h*0.12} l0 {h*0.18}" fill="none" stroke="#8795a1" stroke-width="3"/>')
        # ship
        s.append(f'<path d="M{x+w*0.40} {y+h*0.74} l{w*0.30} 0 l-{w*0.04} {h*0.12} l-{w*0.22} 0 z" fill="#2b3540"/>')
        s.append(f'<rect x="{x+w*0.50}" y="{y+h*0.62}" width="{w*0.08}" height="{h*0.12}" fill="#4a545f"/>')
        # explosion at the ship
        s.append(f'<circle cx="{x+w*0.55}" cy="{y+h*0.52}" r="{h*0.20}" fill="#f2a33a" opacity="0.95"/>')
        s.append(f'<circle cx="{x+w*0.55}" cy="{y+h*0.52}" r="{h*0.34}" fill="#e4572e" opacity="0.45"/>')
        for i in range(9):
            ang = -80 + i * 20
            s.append(f'<path d="M{x+w*0.55} {y+h*0.52} l{28} 0" stroke="#f6c76a" stroke-width="5" transform="rotate({ang} {x+w*0.55} {y+h*0.52})"/>')
        # smoke
        for i, (dx, ry) in enumerate(((0.40, 0.10), (0.30, 0.13), (0.22, 0.09))):
            s.append(f'<ellipse cx="{x+w*dx}" cy="{y+h*(0.18+i*0.05)}" rx="{w*0.10}" ry="{h*ry}" fill="#39424e" opacity="0.9"/>')
    elif kind == "bridge":
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#5d7f95"/>')
        s.append(f'<rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" fill="#2f4d60"/>')
        # abutments
        s.append(f'<rect x="{x}" y="{y+h*0.34}" width="{w*0.16}" height="{h*0.34}" fill="#3b4650"/>')
        s.append(f'<rect x="{x+w*0.84}" y="{y+h*0.34}" width="{w*0.16}" height="{h*0.34}" fill="#3b4650"/>')
        # intact span left, broken edge
        s.append(f'<rect x="{x}" y="{y+h*0.34}" width="{w*0.34}" height="{h*0.08}" fill="#8f9aa5"/>')
        s.append(f'<path d="M{x+w*0.34} {y+h*0.34} l{w*0.06} {h*0.20} l-{w*0.06} 0 z" fill="#8f9aa5"/>')
        s.append(f'<rect x="{x+w*0.70}" y="{y+h*0.34}" width="{w*0.14}" height="{h*0.08}" fill="#8f9aa5"/>')
        # falling pieces
        s.append(f'<rect x="{x+w*0.44}" y="{y+h*0.62}" width="{w*0.10}" height="{h*0.05}" fill="#8f9aa5" transform="rotate(-18 {x+w*0.49} {y+h*0.64})"/>')
        s.append(f'<rect x="{x+w*0.56}" y="{y+h*0.72}" width="{w*0.07}" height="{h*0.04}" fill="#8f9aa5" transform="rotate(12 {x+w*0.59} {y+h*0.74})"/>')
        # splash
        for i in range(5):
            s.append(f'<path d="M{x+w*(0.40+i*0.06)} {y+h*0.74} l0 -{h*(0.08+0.02*i)}" stroke="#cfe3ee" stroke-width="3" opacity="0.8"/>')
    else:  # summit
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8e0d0"/>')
        s.append(f'<rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" fill="#cfc6b3"/>')
        # flags
        for i, col in enumerate(("#1f4e79", "#b3341f", "#1d6b4a", "#4a2f7a")):
            fx = x + w * (0.12 + i * 0.20)
            s.append(f'<path d="M{fx} {y+h*0.42} l0 -{h*0.30}" stroke="#3a3a3a" stroke-width="3"/>')
            s.append(f'<rect x="{fx}" y="{y+h*0.42-h*0.30}" width="{w*0.10}" height="{h*0.10}" fill="{col}"/>')
        # table
        s.append(f'<ellipse cx="{x+w*0.5}" cy="{y+h*0.72}" rx="{w*0.34}" ry="{h*0.12}" fill="#8a7f6a"/>')
        for i in range(4):
            cx = x + w * (0.30 + i * 0.13)
            s.append(f'<circle cx="{cx}" cy="{y+h*0.58}" r="{h*0.05}" fill="#3a3a3a"/>')
            s.append(f'<path d="M{cx-h*0.06} {y+h*0.68} q{h*0.06} -{h*0.08} {h*0.12} 0" fill="#3a3a3a"/>')
    s.append('</g>')
    return "".join(s)


def render(path, mask_text):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    p.append(f'<text x="44" y="40" font-family="DejaVu Sans" font-size="15" letter-spacing="3" fill="{INK}">THE DAY IN WORLD NEWS</text>')
    p.append(f'<text x="980" y="40" text-anchor="end" font-family="DejaVu Sans" font-size="13" letter-spacing="1.6" fill="{GREY}">28 STORIES · WEDNESDAY 18 NOVEMBER 2026</text>')
    dstr = "Wednesday 18 November 2026"
    p.append(f'<text x="44" y="126" font-family="DejaVu Serif" font-size="54" font-weight="bold" fill="{INK}">{dstr}</text>')
    p.append(f'<line x1="44" y1="146" x2="980" y2="146" stroke="{RULE}" stroke-width="3"/>')

    # three scenes
    sw, sh, gap = 300, 150, 18
    for i, kind in enumerate(("port", "bridge", "summit")):
        p.append(scene(kind, 44 + i * (sw + gap), 162, sw, sh))

    # three leads
    y = 330
    for i, (num, cat, head, sub) in enumerate(LEADS):
        x = 44 + i * (sw + gap)
        col = CAT.get(cat, "#b3341f")
        p.append(f'<circle cx="{x+9}" cy="{y+8}" r="9" fill="{col}"/>')
        p.append(f'<text x="{x+9}" y="{y+11.5}" text-anchor="middle" font-family="DejaVu Sans" font-size="10" font-weight="bold" fill="#fff">{num}</text>')
        p.append(f'<text x="{x+24}" y="{y+12}" font-family="DejaVu Sans" font-size="11" font-weight="bold" letter-spacing="1.4" fill="{col}">{cat}</text>')
        lines = wrap(head, 26)
        for j, line in enumerate(lines[:3]):
            p.append(f'<text x="{x}" y="{y+36+j*20}" font-family="DejaVu Serif" font-size="18" font-weight="bold" fill="{INK}">{line}</text>')
        sl = wrap(sub, 46)
        for j, line in enumerate(sl[:3]):
            p.append(f'<text x="{x}" y="{y+100+j*15}" font-family="DejaVu Sans" font-size="11.5" fill="{GREY}">{line}</text>')

    p.append(f'<line x1="44" y1="462" x2="980" y2="462" stroke="{RULE}" stroke-width="2"/>')

    # grid 4-11, two rows of four
    gw, gh = 224, 102
    for i, (num, cat, head, sub) in enumerate(GRID):
        r, c = divmod(i, 4)
        x = 44 + c * (gw + 12)
        yy = 474 + r * (gh + 8)
        col = CAT.get(cat, "#b3341f")
        p.append(f'<rect x="{x}" y="{yy}" width="{gw}" height="{gh}" fill="#fffdf7" stroke="{THIN}"/>')
        p.append(f'<line x1="{x}" y1="{yy}" x2="{x}" y2="{yy+gh}" stroke="{col}" stroke-width="4"/>')
        p.append(f'<text x="{x+12}" y="{yy+18}" font-family="DejaVu Sans" font-size="10" font-weight="bold" letter-spacing="1.2" fill="{col}">{num} · {cat}</text>')
        lines = wrap(head, 26 if num == "10" else 30)
        for j, line in enumerate(lines[:2]):
            p.append(f'<text x="{x+12}" y="{yy+36+j*15}" font-family="DejaVu Serif" font-size="13.5" font-weight="bold" fill="{INK}">{line}</text>')
        sl = wrap(sub, 40)
        for j, line in enumerate(sl[:2]):
            p.append(f'<text x="{x+12}" y="{yy+76+j*12}" font-family="DejaVu Sans" font-size="9.5" fill="{GREY}">{line}</text>')

    # bottom: also list left, map right
    by = 704
    p.append(f'<line x1="44" y1="{by-8}" x2="980" y2="{by-8}" stroke="{RULE}" stroke-width="2"/>')
    p.append(f'<text x="44" y="{by+14}" font-family="DejaVu Sans" font-size="12" font-weight="bold" letter-spacing="1.4" fill="{INK}">ALSO ON WEDNESDAY 18 NOVEMBER</text>')
    yy = by + 34
    for i, item in enumerate(ALSO):
        col_i = 0 if i < 9 else 1
        if i == 9:
            yy = by + 34
        x = 44 + col_i * 232
        p.append(f'<text x="{x}" y="{yy}" font-family="DejaVu Sans" font-size="10.5" font-weight="bold" fill="{GREY}">{12+i}</text>')
        for j, line in enumerate(wrap(item, 29)[:2]):
            p.append(f'<text x="{x+18}" y="{yy+j*12}" font-family="DejaVu Sans" font-size="10.5" font-weight="bold" fill="{INK}">{line}</text>')
        yy += 24

    # map
    mx, my, mw = 520, by + 4, 460
    p.append(f'<text x="{mx}" y="{by+14}" font-family="DejaVu Sans" font-size="12" font-weight="bold" letter-spacing="1.4" fill="{INK}">WHERE IT HAPPENED</text>')
    cell = mw / 90.0
    for r, row in enumerate(mask_text.strip().split("\n")):
        for c, ch in enumerate(row):
            if ch == "#":
                p.append(f'<circle cx="{mx + c*cell + cell/2:.1f}" cy="{my + 24 + r*cell + cell/2:.1f}" r="1.7" fill="#b9b2a2"/>')
    for num, (lon, lat) in DOTS.items():
        cx = mx + (lon + 180) / 360 * mw
        cy = my + 24 + (90 - lat) / 180 * (cell * 45)
        col = "#b3341f"
        for k, (n2, cat, _, _) in enumerate(LEADS + [(g[0], g[1], g[2], g[3]) for g in GRID]):
            if n2 == num:
                col = CAT.get(cat, "#b3341f")
        p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{col}"/>')
        p.append(f'<text x="{cx:.1f}" y="{cy+3.4:.1f}" text-anchor="middle" font-family="DejaVu Sans" font-size="9" font-weight="bold" fill="#fff">{num}</text>')

    p.append(f'<line x1="44" y1="{H-34}" x2="980" y2="{H-34}" stroke="{THIN}"/>')
    p.append(f'<text x="44" y="{H-14}" font-family="DejaVu Sans" font-size="9.5" fill="{GREY}">Sources: AP, Reuters, Xinhua, Kyodo, The Straits Times, The Hindu, BBC. Scenes drawn for this page.</text>')
    p.append('</svg>')
    svg = path.replace('.png', '.svg')
    open(svg, 'w').write("\n".join(p))
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", path, svg], check=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    import os
    default_mask = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mask.txt")
    mask = open(sys.argv[2] if len(sys.argv) > 2 else default_mask).read()
    render(out, mask)
    print(out, os.path.getsize(out), "bytes")
