"""Render tests/TEST_REPORT.md to a standalone, print-friendly HTML document.
Run: venv/Scripts/python.exe tests/export_report.py"""
import os
import re

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "TEST_REPORT.md")
OUT = os.path.join(HERE, "reports", "TEST_REPORT.html")

CSS = """
:root{--ink:#1a1a1a;--muted:#5b6072;--line:#c7cbdb;--navy:#0f1e3d;--amber:#f5a623;--ok:#15803d;--tint:#f7f7fa}
*{box-sizing:border-box}
body{font:15px/1.6 -apple-system,'Segoe UI',Calibri,Arial,sans-serif;color:var(--ink);margin:0;background:#fff}
main{max-width:980px;margin:0 auto;padding:40px 24px 64px}
header.banner{background:var(--navy);color:#fff;padding:36px 24px;border-bottom:4px solid var(--amber)}
header.banner div{max-width:980px;margin:0 auto}
header.banner p{margin:6px 0 0;color:#cadcfc}
h1{font-size:28px;margin:0}
main h1{display:none}
h2{font-size:20px;color:var(--navy);margin:34px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px}
th{background:var(--navy);color:#fff;text-align:left;padding:8px 10px}
td{border:1px solid var(--line);padding:8px 10px;vertical-align:top}
tbody tr:nth-child(even){background:var(--tint)}
code{font-family:Consolas,'Courier New',monospace;font-size:13px;background:var(--tint);padding:1px 5px;border-radius:4px}
pre{background:var(--tint);border:1px solid var(--line);border-radius:8px;padding:14px;overflow-x:auto}
pre code{background:none;padding:0}
strong{color:var(--navy)}
a{color:#1d4ed8}
.pass{display:inline-block;background:var(--ok);color:#fff;border-radius:999px;padding:2px 14px;font-weight:700}
nav.links{margin:18px 0 0;font-size:14px}
@media print{header.banner{-webkit-print-color-adjust:exact;print-color-adjust:exact}th{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

with open(SRC, encoding="utf-8") as f:
    body = markdown.markdown(f.read(), extensions=["tables", "fenced_code"])
# the summary table has a blank header row in Markdown; drop the empty navy bar it would render
body = re.sub(r"<thead>\s*<tr>(\s*<th>\s*</th>)+\s*</tr>\s*</thead>", "", body)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CricketIQ - Selenium Test Report</title><style>{CSS}</style></head>
<body>
<header class="banner"><div>
<h1>CricketIQ - Selenium Test Report</h1>
<p><span class="pass">59 / 59 passed</span> &nbsp; Chrome 154 headless &middot; Selenium 4.50 &middot; pytest 9.1</p>
</div></header>
<main>
<nav class="links">Detailed per-test log: <a href="selenium_report.html">selenium_report.html</a> &middot; CI format: <a href="junit.xml">junit.xml</a></nav>
{body}
</main></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", OUT, len(html), "bytes")
