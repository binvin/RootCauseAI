from rootcause.tools import search_logs,detect_patterns,extract_timeline,validate_evidence
from rootcause.agent import mock_investigate,redact_secrets
LOG="2026-10-27 10:00:01 INFO start\n2026-10-27 10:00:02 ERROR PKIX path building failed\n"
def test_search():
    assert search_logs(LOG,"PKIX")["hits"][0]["line"]==2

def test_patterns():
    assert detect_patterns(LOG)["patterns"][0]["pattern"]=="tls_certificate"

def test_timeline():
    assert extract_timeline(LOG)["total"]==2

def test_evidence():
    r=validate_evidence(LOG,[2,100]); assert len(r["supported_lines"])==1 and r["invalid_lines"]==[100]

def test_mock():
    report, trace=mock_investigate(LOG); assert "tls_certificate" in report and len(trace)==3

def test_redact():
    assert "supersecret" not in redact_secrets("token=supersecret")
