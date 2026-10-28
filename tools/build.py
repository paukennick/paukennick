"""Generate the profile banner, project cards and social previews.

usage: python tools/build.py          # writes assets/*.svg and assets/social/*.svg
Edit PROJECTS or THEMES below, rerun, commit. PNG social previews are made by
tools/render_png.ps1 (headless Chrome) from the social SVGs.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#141414", panel="#1C1C1C", line="#2E2E2E", grid="#242424",
                 text="#F5F5F4", muted="#A8A29E", accent="#F59E0B", accent2="#F97316"),
    "light": dict(bg="#FAFAF9", panel="#FFFFFF", line="#E7E5E4", grid="#E7E5E4",
                  text="#1C1917", muted="#57534E", accent="#D97706", accent2="#EA580C"),
}

PROJECTS = {
    "arbiter": dict(
        title="Arbiter", tag="PYTHON · APACHE-2.0",
        pitch=["Static analysis for AI-written code.", "Names every check it didn’t run."],
        stats=[("21", "native probes"), ("280", "rules"), ("10", "control frameworks")],
    ),
    "ascendra": dict(
        title="Ascendra", tag="TYPESCRIPT · iOS · ANDROID · WEB",
        pitch=["Adaptive AI-tutored certification prep.", "Expo · Next.js · Supabase · Claude API"],
        stats=[("90", "courses"), ("3", "platforms"), ("1/7/21", "day spaced review")],
    ),
    "omni": dict(
        title="OmniEngineering", tag="FORK · CONTRIBUTOR",
        pitch=["Repo-local engineering workspace that", "keeps AI assistants on one context."],
        stats=[("5", "AI assistants"), ("3.10+", "Python"), ("0", "MCP servers needed")],
    ),
}

MOTION = """
@keyframes blink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }
@keyframes pulse { 0% { opacity: .55; transform: scale(.82) } 100% { opacity: 0; transform: scale(1.18) } }
.cursor { animation: blink 1.1s steps(1) infinite }
.ring { transform-origin: 1010px 150px; animation: pulse 3.6s ease-out infinite }
.ring.r2 { animation-delay: 1.2s } .ring.r3 { animation-delay: 2.4s }
@media (prefers-reduced-motion: reduce) { .cursor, .ring { animation: none } }
"""


def banner(t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Nick Pauken, SRE and DevSecOps: assurance tooling for AI-written code">
<style>{MOTION}</style>
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['grid']}"/></pattern>
  <radialGradient id="glow" cx="84%" cy="50%" r="45%"><stop offset="0" stop-color="{t['accent']}" stop-opacity=".22"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/></linearGradient>
  <clipPath id="frame"><rect width="1200" height="300" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="1200" height="300" fill="{t['bg']}"/>
  <rect width="1200" height="300" fill="url(#dots)"/>
  <rect width="1200" height="300" fill="url(#glow)"/>
  <rect width="1200" height="4" fill="url(#edge)"/>
</g>
<rect x=".5" y=".5" width="1199" height="299" rx="18" fill="none" stroke="{t['line']}"/>
<text x="64" y="72" font-family="{MONO}" font-size="16" fill="{t['accent']}">~/paukennick</text>
<text x="62" y="136" font-family="{SANS}" font-size="62" font-weight="700" fill="{t['text']}">Nick Pauken</text>
<text x="64" y="178" font-family="{SANS}" font-size="24" font-weight="600" fill="{t['accent']}">SRE · DevSecOps · Greater Seattle Area</text>
<text x="64" y="214" font-family="{SANS}" font-size="20" fill="{t['muted']}">Assurance tooling for AI-written code: measured precision, traceable requirements.</text>
<text x="64" y="260" font-family="{MONO}" font-size="16" fill="{t['muted']}"><tspan fill="{t['accent']}">$</tspan> arbiter scan .  <tspan fill="{t['accent2']}"># every check that didn’t run is named</tspan><tspan class="cursor" fill="{t['accent']}"> ▍</tspan></text>
<circle class="ring" cx="1010" cy="150" r="96" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
<circle class="ring r2" cx="1010" cy="150" r="96" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
<circle class="ring r3" cx="1010" cy="150" r="96" fill="none" stroke="{t['accent']}" stroke-width="1.5"/>
<path d="M1010 78 L1066 100 V148 C1066 186 1042 210 1010 224 C978 210 954 186 954 148 V100 Z" fill="{t['panel']}" stroke="url(#edge)" stroke-width="4" stroke-linejoin="round"/>
<path d="M984 150 L1002 168 L1038 130" fill="none" stroke="{t['accent']}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def icon(key, size=56, x=322, y=18):
    """Inline assets/icons/<key>.svg (GitHub won't load files referenced from an SVG image)."""
    import re
    src = (ASSETS / "icons" / f"{key}.svg").read_text(encoding="utf-8")
    body = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    for old in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{old}"', f'id="{key}-{old}"').replace(f"url(#{old})", f"url(#{key}-{old})")
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256">{body}</svg>'


def card(p, t, key=None):
    stats = "".join(
        f'<text x="{24 + i * 126}" y="188" font-family="{SANS}" font-size="26" font-weight="700" fill="{t["accent"]}">{escape(v)}</text>'
        f'<text x="{24 + i * 126}" y="210" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{escape(k)}</text>'
        for i, (v, k) in enumerate(p["stats"]))
    pitch = "".join(
        f'<text x="24" y="{108 + i * 22}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{escape(s)}</text>'
        for i, s in enumerate(p["pitch"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="236" viewBox="0 0 400 236" role="img" aria-label="{escape(p['title'])}: {escape(' '.join(p['pitch']))}">
<defs>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/></linearGradient>
  <clipPath id="frame"><rect width="400" height="236" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)"><rect width="400" height="236" fill="{t['panel']}"/><rect width="400" height="4" fill="url(#edge)"/></g>
<rect x=".5" y=".5" width="399" height="235" rx="14" fill="none" stroke="{t['line']}"/>
<text x="24" y="38" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t['accent']}">{escape(p['tag'])}</text>
<text x="24" y="76" font-family="{SANS}" font-size="28" font-weight="700" fill="{t['text']}">{escape(p['title'])}</text>
{pitch}
<line x1="24" x2="376" y1="152" y2="152" stroke="{t['line']}"/>
{stats}
{icon(key) if key else ''}
</svg>
"""


def social(key, p, t, repo):
    stats = "".join(
        f'<text x="{96 + i * 300}" y="470" font-family="{SANS}" font-size="64" font-weight="700" fill="{t["accent"]}">{escape(v)}</text>'
        f'<text x="{96 + i * 300}" y="510" font-family="{SANS}" font-size="26" fill="{t["muted"]}">{escape(k)}</text>'
        for i, (v, k) in enumerate(p["stats"]))
    pitch = "".join(
        f'<text x="96" y="{272 + i * 46}" font-family="{SANS}" font-size="36" fill="{t["muted"]}">{escape(s)}</text>'
        for i, s in enumerate(p["pitch"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
<defs>
  <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{t['grid']}"/></pattern>
  <radialGradient id="glow" cx="90%" cy="20%" r="60%"><stop offset="0" stop-color="{t['accent']}" stop-opacity=".2"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/></linearGradient>
</defs>
<rect width="1280" height="640" fill="{t['bg']}"/><rect width="1280" height="640" fill="url(#dots)"/><rect width="1280" height="640" fill="url(#glow)"/>
<rect width="1280" height="10" fill="url(#edge)"/>
<text x="96" y="128" font-family="{MONO}" font-size="24" letter-spacing="2" fill="{t['accent']}">{escape(p['tag'])}</text>
<text x="92" y="214" font-family="{SANS}" font-size="96" font-weight="700" fill="{t['text']}">{escape(p['title'])}</text>
{pitch}
<line x1="96" x2="1184" y1="380" y2="380" stroke="{t['line']}" stroke-width="2"/>
{stats}
<text x="96" y="590" font-family="{MONO}" font-size="24" fill="{t['muted']}">github.com/{escape(repo)}</text>
</svg>
"""


def emblem(key, t):
    a, b, p = t["accent"], t["accent2"], t["panel"]
    if key == "arbiter":  # shield with check inside scan rings
        rings = "".join(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{a}" stroke-opacity="{o}" stroke-width="2"/>'
                        for r, o in ((150, .15), (190, .09), (230, .05)))
        return (rings + f'<path d="M0 -112 L88 -78 V-4 C88 56 50 94 0 116 C-50 94 -88 56 -88 -4 V-78 Z" fill="{p}" '
                f'stroke="url(#edge)" stroke-width="6" stroke-linejoin="round"/>'
                f'<path d="M-40 0 L-12 28 L44 -30" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    if key == "ascendra":  # rising steps = 0-4 mastery levels, with a peak marker
        bars = "".join(f'<rect x="{-150 + i * 64}" y="{90 - h}" width="44" height="{h}" rx="8" fill="{a}" fill-opacity="{.25 + i * .18}"/>'
                       for i, h in enumerate((40, 80, 120, 160, 200)))
        return (bars + f'<path d="M-128 30 C-60 10 0 -40 120 -130" fill="none" stroke="{b}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>'
                f'<circle cx="128" cy="-136" r="12" fill="{b}"/><line x1="-170" x2="170" y1="92" y2="92" stroke="{t["line"]}" stroke-width="3"/>')
    # omni: one shared context hub, five assistants around it
    import math
    pts = [(160 * math.cos(math.radians(-90 + i * 72)), 160 * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
    spokes = "".join(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{a}" stroke-opacity=".5" stroke-width="3"/>' for x, y in pts)
    ring = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    nodes = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="{p}" stroke="{b}" stroke-width="4"/>' for x, y in pts)
    return (f'<polygon points="{ring}" fill="none" stroke="{t["line"]}" stroke-width="3"/>' + spokes + nodes +
            f'<circle cx="0" cy="0" r="54" fill="{p}" stroke="url(#edge)" stroke-width="6"/>'
            f'<text x="0" y="12" text-anchor="middle" font-family="{MONO}" font-size="34" font-weight="700" fill="{a}">.ai</text>')


def social_emblem(key, p, t, repo):
    pitch = "".join(
        f'<text x="96" y="{330 + i * 44}" font-family="{SANS}" font-size="32" fill="{t["muted"]}">{escape(s)}</text>'
        for i, s in enumerate(p["pitch"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
<defs>
  <radialGradient id="glow" cx="78%" cy="50%" r="42%"><stop offset="0" stop-color="{t['accent']}" stop-opacity=".25"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/></linearGradient>
</defs>
<rect width="1280" height="640" fill="{t['bg']}"/><rect width="1280" height="640" fill="url(#glow)"/>
<rect x="0" y="0" width="10" height="640" fill="url(#edge)"/>
<text x="96" y="200" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{t['accent']}">{escape(p['tag'])}</text>
<text x="92" y="282" font-family="{SANS}" font-size="{80 if len(p['title']) > 10 else 92}" font-weight="700" fill="{t['text']}">{escape(p['title'])}</text>
{pitch}
<text x="96" y="560" font-family="{MONO}" font-size="22" fill="{t['muted']}">github.com/{escape(repo)}</text>
<g transform="translate(1000 320)">{emblem(key, t)}</g>
</svg>
"""


SOCIAL_REPOS = {"arbiter": "paukennick/arbiter", "ascendra": "paukennick/Ascendra", "omni": "paukennick/OmniEngineering"}


def main():
    (ASSETS / "social").mkdir(parents=True, exist_ok=True)
    out = {}
    for name, t in THEMES.items():
        out[f"banner-{name}.svg"] = banner(t)
        for key, p in PROJECTS.items():
            out[f"card-{key}-{name}.svg"] = card(p, t, key)
    for key, p in PROJECTS.items():
        repo = SOCIAL_REPOS[key]
        out[f"social/{key}.svg"] = social(key, p, THEMES["dark"], repo)  # option A: stats, dark
        out[f"social/{key}-b.svg"] = social(key, p, THEMES["light"], repo)  # option B: stats, light
        out[f"social/{key}-c.svg"] = social_emblem(key, p, THEMES["dark"], repo)  # option C: emblem
    for rel, svg in out.items():
        (ASSETS / rel).write_text(svg, encoding="utf-8", newline="\n")
    print(f"wrote {len(out)} files under {ASSETS}")


if __name__ == "__main__":
    main()
