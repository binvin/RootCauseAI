import streamlit as st
from rootcause.agent import mock_investigate, neb_investigate, redact_secrets

st.set_page_config(page_title="RootCause AI",page_icon="🔎",layout="wide")
st.title("🔎 RootCause AI")
st.caption("Evidence-first troubleshooting agent • NVIDIA Nemotron via Nebius Token Factory")
st.warning("Development prototype. Do not upload secrets or confidential customer logs. Investigation is read-only; conclusions require human validation.")
mode=st.radio("Investigation mode",["Offline baseline (no AI)","Nebius Nemotron agent"],horizontal=True)
upload=st.file_uploader("Upload a UTF-8 log file",type=["log","txt"])
if upload:
    raw=upload.getvalue().decode("utf-8",errors="replace")
else:
    raw=st.text_area("Or paste logs",height=210,placeholder="2026-10-27 10:00:01 ERROR SSLHandshakeException: PKIX path building failed")
if st.button("Investigate",type="primary",disabled=not bool(raw.strip())):
    text=redact_secrets(raw)[:80000]
    if len(raw)>len(text):st.info("Input may have been truncated for predictable processing.")
    with st.spinner("Investigating read-only log evidence..."):
        try:
            report,trace=(mock_investigate(text) if mode.startswith("Offline") else neb_investigate(text))
        except Exception as exc:
            st.error(f"Investigation failed: {type(exc).__name__}: {exc}")
            st.stop()
    st.subheader("Investigation report")
    st.markdown(report)
    st.download_button("Download report",report,file_name="rootcause_report.md",mime="text/markdown")
    st.subheader("Investigation trace")
    st.caption("Tool results are drawn from the supplied log only. No live systems are accessed.")
    for index,step in enumerate(trace,1):
        with st.expander(f"Step {index}: {step['tool']}"):
            st.json(step)
