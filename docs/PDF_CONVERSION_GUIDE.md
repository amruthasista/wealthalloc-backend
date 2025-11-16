# Converting Architecture Document to PDF

## Quick Start

Your comprehensive WealthAlloc Architecture Document is ready! Here's how to convert it to a professional PDF for your team.

---

## Method 1: Using Pandoc (Recommended)

**Pandoc** is the best tool for converting Markdown to professional PDFs.

### Installation

**macOS:**
```bash
brew install pandoc
brew install basictex  # LaTeX for PDF generation
```

**Ubuntu/Debian:**
```bash
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**Windows:**
Download from: https://pandoc.org/installing.html

### Basic Conversion

```bash
pandoc ARCHITECTURE.md -o WealthAlloc_Architecture.pdf
```

### Professional PDF with Styling

```bash
pandoc ARCHITECTURE.md \
  -o WealthAlloc_Architecture.pdf \
  --from markdown \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=report \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --highlight-style=tango
```

**Options Explained:**
- `--toc`: Generate table of contents
- `--toc-depth=3`: TOC includes 3 heading levels
- `--number-sections`: Add section numbers
- `-V geometry:margin=1in`: Set 1-inch margins
- `-V fontsize=11pt`: Use 11-point font
- `--highlight-style=tango`: Syntax highlighting for code

### With Custom Title Page

Create `title.yaml`:
```yaml
---
title: "WealthAlloc Architecture Document"
subtitle: "Comprehensive System Architecture"
author:
  - "WealthAlloc Engineering Team"
date: "November 2024"
version: "1.0.0"
keywords: [architecture, fintech, AI, trading]
abstract: |
  This document describes the complete architecture of the WealthAlloc
  platform, including system design, scalability strategies, security
  architecture, and deployment infrastructure.
---
```

Then convert:
```bash
pandoc title.yaml ARCHITECTURE.md \
  -o WealthAlloc_Architecture.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=11pt
```

---

## Method 2: Using Markdown PDF (VS Code Extension)

### Installation

1. Open VS Code
2. Install "Markdown PDF" extension
3. Open `ARCHITECTURE.md`
4. Right-click → "Markdown PDF: Export (pdf)"

### Configuration

Create `.vscode/settings.json`:
```json
{
  "markdown-pdf.format": "A4",
  "markdown-pdf.displayHeaderFooter": true,
  "markdown-pdf.headerTemplate": "<div style='font-size:9px; text-align:center; width:100%;'>WealthAlloc Architecture</div>",
  "markdown-pdf.footerTemplate": "<div style='font-size:9px; text-align:center; width:100%;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
  "markdown-pdf.margin": {
    "top": "1cm",
    "bottom": "1cm",
    "left": "1cm",
    "right": "1cm"
  }
}
```

---

## Method 3: Using grip (GitHub-style Preview)

**grip** renders Markdown exactly as it appears on GitHub.

### Installation

```bash
pip install grip
```

### Generate PDF

```bash
# Start grip server
grip ARCHITECTURE.md

# Open in browser: http://localhost:6419
# Print to PDF using browser (Cmd/Ctrl + P)
```

---

## Method 4: Using Typora (GUI App)

**Typora** is a beautiful Markdown editor with built-in PDF export.

1. Download: https://typora.io/
2. Open `ARCHITECTURE.md`
3. File → Export → PDF

**Pros:**
- WYSIWYG editor
- Beautiful default styling
- Simple one-click export

---

## Method 5: Online Converters

### Markdown to PDF (https://www.markdowntopdf.com/)
1. Upload `ARCHITECTURE.md`
2. Click "Convert"
3. Download PDF

### Dillinger (https://dillinger.io/)
1. Paste Markdown content
2. Click "Export as" → "Styled HTML"
3. Print to PDF from browser

---

## Method 6: Using Python Script

Create `convert_to_pdf.py`:
```python
#!/usr/bin/env python3
"""
Convert Markdown to PDF using markdown2 and weasyprint
"""

from markdown2 import markdown
from weasyprint import HTML
from datetime import datetime

# Read markdown
with open('ARCHITECTURE.md', 'r') as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown(md_content, extras=['tables', 'fenced-code-blocks', 'header-ids'])

# Add CSS styling
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        @page {{
            size: A4;
            margin: 2cm;
            @top-center {{
                content: "WealthAlloc Architecture";
            }}
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
            }}
        }}
    </style>
</head>
<body>
    <div style="text-align: center; margin-bottom: 50px;">
        <h1>WealthAlloc</h1>
        <h2>Architecture Document</h2>
        <p>Version 1.0.0 | {datetime.now().strftime('%B %Y')}</p>
    </div>
    {html_content}
</body>
</html>
"""

# Generate PDF
HTML(string=styled_html).write_pdf('WealthAlloc_Architecture.pdf')
print("✓ PDF generated: WealthAlloc_Architecture.pdf")
```

**Install dependencies:**
```bash
pip install markdown2 weasyprint
```

**Run:**
```bash
python convert_to_pdf.py
```

---

## Styling Tips

### Add Cover Page

Create `cover.md`:
```markdown
---
title: ""
---

<div style="text-align: center; margin-top: 200px;">
  <h1 style="font-size: 48px; color: #2c3e50;">WealthAlloc</h1>
  <h2 style="font-size: 32px; color: #3498db;">System Architecture</h2>
  
  <p style="margin-top: 50px; font-size: 18px;">
    Version 1.0.0<br>
    November 2024
  </p>
  
  <p style="margin-top: 100px;">
    <strong>Prepared by:</strong><br>
    WealthAlloc Engineering Team
  </p>
  
  <p style="margin-top: 150px; color: #7f8c8d;">
    Confidential - Internal Use Only
  </p>
</div>

<div style="page-break-after: always;"></div>
```

**Combine with architecture doc:**
```bash
pandoc cover.md ARCHITECTURE.md -o WealthAlloc_Architecture.pdf --pdf-engine=xelatex
```

### Custom CSS for HTML

Create `styles.css`:
```css
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #2c3e50;
    border-bottom: 4px solid #3498db;
    padding-bottom: 10px;
    margin-top: 40px;
}

h2 {
    color: #34495e;
    border-bottom: 2px solid #95a5a6;
    padding-bottom: 5px;
    margin-top: 30px;
}

code {
    background-color: #f8f9fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', Consolas, monospace;
    font-size: 90%;
}

pre {
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    padding: 15px;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

th {
    background-color: #3498db;
    color: white;
    padding: 12px;
}

td {
    border: 1px solid #ddd;
    padding: 10px;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}
```

**Use with pandoc:**
```bash
pandoc ARCHITECTURE.md -o WealthAlloc_Architecture.pdf --css=styles.css
```

---

## Best Practices

### 1. **Check Before Converting**

```bash
# Validate Markdown syntax
markdownlint ARCHITECTURE.md

# Check for broken links
markdown-link-check ARCHITECTURE.md
```

### 2. **Optimize for Print**

- Use page breaks: `<div style="page-break-after: always;"></div>`
- Avoid very wide code blocks
- Use appropriate font sizes (10-12pt)
- Include page numbers

### 3. **Add Metadata**

```bash
pandoc ARCHITECTURE.md -o output.pdf \
  --metadata title="WealthAlloc Architecture" \
  --metadata author="Engineering Team" \
  --metadata date="November 2024"
```

### 4. **Version Control**

```bash
# Add version to filename
pandoc ARCHITECTURE.md -o WealthAlloc_Architecture_v1.0.0.pdf
```

### 5. **Compress PDF**

```bash
# Reduce file size
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=compressed.pdf WealthAlloc_Architecture.pdf
```

---

## Sharing Options

### 1. **Email**

```
Subject: WealthAlloc Architecture Document v1.0.0

Hi Team,

Please find attached the complete architecture document for the WealthAlloc platform.

Key sections:
- System Overview (p. 3)
- Core Components (p. 12)
- Security Architecture (p. 28)
- Deployment Strategy (p. 35)

Please review by [date] and send feedback to architecture@wealthalloc.com

Best regards,
Architecture Team
```

### 2. **Confluence / Wiki**

- Upload PDF as attachment
- Create page with embedded PDF viewer
- Add table of contents with links

### 3. **Google Drive / SharePoint**

```
Folder Structure:
/WealthAlloc Documentation
  /Architecture
    - WealthAlloc_Architecture_v1.0.0.pdf
    - Diagrams/
    - Supplementary_Docs/
```

### 4. **GitHub Wiki**

- Upload to wiki repository
- Link from main README
- Use GitHub Pages for hosting

### 5. **Presentation Mode**

Create a summary presentation:
```bash
# Convert to HTML slides
pandoc ARCHITECTURE.md -o presentation.html -t revealjs -s
```

---

## Troubleshooting

### Issue: LaTeX errors during conversion

**Solution:**
```bash
# Install full LaTeX distribution
sudo apt-get install texlive-full  # Ubuntu
brew install --cask mactex  # macOS
```

### Issue: Missing fonts

**Solution:**
```bash
# Install additional fonts
sudo apt-get install fonts-liberation
```

### Issue: Large file size

**Solution:**
```bash
# Use compressed settings
pandoc ARCHITECTURE.md -o output.pdf --pdf-engine=xelatex -V geometry:margin=0.75in
```

### Issue: Code blocks cut off

**Solution:**
```bash
# Adjust margins
pandoc ARCHITECTURE.md -o output.pdf -V geometry:margin=0.5in
```

---

## Quick Reference

**Best Method for Professional PDF:**
```bash
pandoc ARCHITECTURE.md -o WealthAlloc_Architecture.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V geometry:margin=1in
```

**Fastest Method:**
```bash
# Using VS Code Markdown PDF extension
Right-click in editor → "Markdown PDF: Export (pdf)"
```

**Most Beautiful Output:**
```bash
# Using Typora
File → Export → PDF
```

---

## Additional Resources

- **Pandoc Manual:** https://pandoc.org/MANUAL.html
- **Markdown Guide:** https://www.markdownguide.org/
- **LaTeX Documentation:** https://www.latex-project.org/
- **WeasyPrint Docs:** https://weasyprint.org/

---

**Your architecture document is ready to share! 🎉**

Choose any method above to generate a professional PDF for your team.
