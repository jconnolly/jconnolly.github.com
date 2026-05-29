#!/usr/bin/env python3
"""
Generate per-post OG images via headless Chromium.
Run: python3 _scripts/og.py "Title here" output.png [--subtitle "..."] [--tag "..."]
1200x630 PNG, branded with the scallop + ollyconn wordmark.
"""
import argparse, asyncio, html, os, sys
from playwright.async_api import async_playwright

SCALLOP = """
<svg viewBox="0 0 100 92" xmlns="http://www.w3.org/2000/svg" style="width:120px;height:auto;fill:#ececef;stroke:#ececef;stroke-width:1.2;stroke-linejoin:miter">
  <g><path d="M 50 78 L 47 8 L 53 8 Z"/><path d="M 50 78 L 56 9 L 62 11 Z"/><path d="M 50 78 L 64 12 L 70 17 Z"/><path d="M 50 78 L 72 19 L 78 26 Z"/><path d="M 50 78 L 79 28 L 84 36 Z"/><path d="M 50 78 L 85 39 L 89 49 Z"/><path d="M 50 78 L 90 52 L 93 64 Z"/><path d="M 50 78 L 44 9 L 38 11 Z"/><path d="M 50 78 L 36 12 L 30 17 Z"/><path d="M 50 78 L 28 19 L 22 26 Z"/><path d="M 50 78 L 21 28 L 16 36 Z"/><path d="M 50 78 L 15 39 L 11 49 Z"/><path d="M 50 78 L 10 52 L 7 64 Z"/></g>
  <path d="M 35 78 L 65 78 L 65 88 L 35 88 Z M 50 78 L 42 82 L 50 86 L 58 82 Z" fill-rule="evenodd" stroke="none"/>
</svg>
"""

def template(title, subtitle, tag):
    t = html.escape(title)
    s = html.escape(subtitle) if subtitle else ""
    g = html.escape(tag).upper() if tag else ""
    # size title font dynamically
    n = len(title)
    title_size = 92 if n <= 30 else (74 if n <= 60 else 58 if n <= 100 else 46)
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ width: 1200px; height: 630px; background: #14141a; color: #ececef;
         font-family: 'Inter', system-ui, sans-serif; position: relative;
         overflow: hidden; }}
  .accent {{ position: absolute; top: 0; left: 0; width: 8px; height: 100%;
             background: #8a99f0; }}
  .brand {{ position: absolute; top: 56px; right: 72px; display: flex;
            flex-direction: column; align-items: center; }}
  .brand .name {{ margin-top: 18px; font-weight: 600; font-size: 26px;
                 color: #ececef; }}
  .brand .url {{ font-size: 14px; color: #93939d; font-style: italic;
                margin-top: 4px; letter-spacing: 0.5px; }}
  .content {{ position: absolute; left: 72px; right: 240px;
              top: 50%; transform: translateY(-50%); }}
  .tag {{ font-family: 'JetBrains Mono', monospace; font-size: 18px;
          color: #8a99f0; letter-spacing: 3px; margin-bottom: 26px;
          text-transform: uppercase; }}
  .title {{ font-family: 'Newsreader', Georgia, serif; font-weight: 700;
            font-size: {title_size}px; line-height: 1.08; color: #ececef;
            letter-spacing: -1.4px; }}
  .subtitle {{ font-family: 'Inter', sans-serif; font-style: italic;
               font-size: 24px; color: #93939d; margin-top: 22px;
               line-height: 1.4; max-width: 720px; }}
  .footer {{ position: absolute; bottom: 38px; left: 72px; right: 240px;
             display: flex; align-items: center; gap: 16px;
             font-family: 'JetBrains Mono', monospace; font-size: 16px;
             color: #93939d; }}
  .footer .rule {{ flex: 1; height: 1px; background: #2a2a32; }}
</style></head>
<body>
  <div class="accent"></div>
  <div class="brand">{SCALLOP}<div class="name">ollyconn</div><div class="url">ollyconn.com</div></div>
  <div class="content">
    {f'<div class="tag">{g}</div>' if g else ''}
    <div class="title">{t}</div>
    {f'<div class="subtitle">{s}</div>' if s else ''}
  </div>
  <div class="footer"><span>john connolly</span><span class="rule"></span></div>
</body></html>"""

async def main(args):
    html_doc = template(args.title, args.subtitle, args.tag)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={'width': 1200, 'height': 630},
                                         device_scale_factor=1)
        page = await ctx.new_page()
        await page.set_content(html_doc, wait_until='networkidle')
        await page.wait_for_timeout(400)
        await page.screenshot(path=args.out, omit_background=False, full_page=False,
                              clip={'x': 0, 'y': 0, 'width': 1200, 'height': 630})
        await browser.close()
    print(f"wrote {args.out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("title")
    ap.add_argument("out")
    ap.add_argument("--subtitle", default=None)
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()
    asyncio.run(main(args))
