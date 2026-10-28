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
    "dark": dict(bg="#0F172A", panel="#111B2E", line="#1E293B", grid="#1E293B",
                 text="#F1F5F9", muted="#94A3B8", accent="#14B8A6", accent2="#22D3EE"),
    "light": dict(bg="#F8FAFC", panel="#FFFFFF", line="#E2E8F0", grid="#E2E8F0",
                  text="#0F172A", muted="#475569", accent="#0D9488", accent2="#0891B2"),
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


def card(p, t):
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


SOCIAL_REPOS = {"arbiter": "paukennick/arbiter", "ascendra": "paukennick/Ascendra", "omni": "paukennick/OmniEngineering"}


def main():
    (ASSETS / "social").mkdir(parents=True, exist_ok=True)
    out = {}
    for name, t in THEMES.items():
        out[f"banner-{name}.svg"] = banner(t)
        for key, p in PROJECTS.items():
            out[f"card-{key}-{name}.svg"] = card(p, t)
    for key, p in PROJECTS.items():
        out[f"social/{key}.svg"] = social(key, p, THEMES["dark"], SOCIAL_REPOS[key])
    for rel, svg in out.items():
        (ASSETS / rel).write_text(svg, encoding="utf-8", newline="\n")
    print(f"wrote {len(out)} files under {ASSETS}")


if __name__ == "__main__":
    main()
