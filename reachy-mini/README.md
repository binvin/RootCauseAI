---
title: Rootcause Reachy
emoji: 🤖
colorFrom: purple
colorTo: gray
sdk: static
pinned: false
tags:
  - reachy_mini
  - reachy_mini_python_app
---

# Rootcause Reachy

Forked from the Reachy Mini conversation app.

Customize `profiles/_rootcause_reachy_locked_profile/profile.md` to change the assistant instructions and enabled tools.
Add custom tools under `src/rootcause_reachy/tools/` by subclassing `Tool`.

Do not forget to customize:
- this `README.md` file
- the `index.html` file (Hugging Face Spaces landing page)
- the `src/rootcause_reachy/static/index.html` (the web app parameters page)

The original README from the conversation app is available in `README_OLD.md`.