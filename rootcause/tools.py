"""Deterministic, read-only investigation tools. No shell execution or network scanning."""
import re
from datetime import datetime

PATTERNS = {
    "tls_certificate": [r"PKIX path building failed", r"certificate verify failed", r"CERTIFICATE_VERIFY_FAILED", r"unknown ca"],
    "authentication": [r"401 unauthorized", r"invalid credentials", r"authentication failed", r"access denied"],
    "network_dns": [r"Name or service not known", r"NXDOMAIN", r"temporary failure in name resolution", r"getaddrinfo failed"],
    "dependency": [r"ModuleNotFoundError", r"No module named", r"dependency resolution failed"],
    "resource_exhaustion": [r"outofmemory", r"out of memory", r"no space left on device", r"OOMKilled"],
}

def number_lines(log: str):
    return [{"line": i, "text": line[:600]} for i, line in enumerate(log.splitlines(), 1)]

def search_logs(log: str, query: str, limit: int = 15):
    if not query or len(query) > 150:
        return {"error": "query required (1-150 chars)"}
    hits = [x for x in number_lines(log) if query.lower() in x["text"].lower()]
    return {"query": query, "hits": hits[:limit], "total": len(hits)}

def detect_patterns(log: str):
    results = []
    for kind, patterns in PATTERNS.items():
        hits = [x for x in number_lines(log) if any(re.search(p, x["text"], re.I) for p in patterns)]
        if hits:
            results.append({"pattern": kind, "hits": hits[:10], "total": len(hits)})
    return {"patterns": results}

def extract_timeline(log: str, limit: int = 35):
    # Not all logs have timestamps; preserve original order.
    stamp = re.compile(r"(?:20\d\d-\d\d-\d\d[ T]\d\d:\d\d:\d\d(?:[.,]\d+)?)")
    events = []
    for row in number_lines(log):
        m = stamp.search(row["text"])
        if m:
            events.append({**row, "timestamp": m.group(0)})
    return {"events": events[:limit], "total": len(events), "note": "Source order, not clock-synchronized."}

def validate_evidence(log: str, lines: list[int]):
    numbered = number_lines(log)
    valid = {x["line"]: x["text"] for x in numbered}
    found = [{"line": n, "text": valid[n]} for n in lines if isinstance(n,int) and n in valid]
    missing = [n for n in lines if not isinstance(n,int) or n not in valid]
    return {"supported_lines": found, "invalid_lines": missing}

TOOL_HANDLERS = {
    "search_logs": search_logs,
    "detect_patterns": detect_patterns,
    "extract_timeline": extract_timeline,
    "validate_evidence": validate_evidence,
}

def run_tool(name: str, log: str, arguments: dict):
    if name not in TOOL_HANDLERS:
        return {"error": f"Unknown tool: {name}"}
    if name == "search_logs":
        return search_logs(log, str(arguments.get("query", "")))
    if name == "validate_evidence":
        return validate_evidence(log, arguments.get("lines", []))
    return TOOL_HANDLERS[name](log)
