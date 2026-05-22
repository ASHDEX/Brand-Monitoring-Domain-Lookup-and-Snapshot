# Brand & Domain Monitoring Toolkit

A Python toolkit for brand protection and domain intelligence — performing bulk domain lookups, reachability checks, visual screenshot capture, and HTML report generation.

## Scripts

| Script | Description |
|--------|-------------|
| `bulk-domain-reachability-check.py` | Checks reachability of bulk domain lists and flags unreachable or suspicious domains |
| `domain_visual_report_generator` | Captures full-page screenshots of domains and compiles them into a visual HTML report |
| `screenshot_collector.py` | Standalone screenshot collector for domain archival and forensic documentation |

## Use Cases

- Detect typosquatting and brand impersonation domains
- Monitor domain infrastructure changes over time
- Generate visual evidence reports for incident response
- Perform bulk reachability assessments on suspected phishing domains

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run bulk reachability check
python bulk-domain-reachability-check.py

# Generate visual domain report
python screenshot_collector.py
```

## Author

**ASHDEX** — Security Researcher & Architect  
[ashdex.com](https://ashdex.com)
