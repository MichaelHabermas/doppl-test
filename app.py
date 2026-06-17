"""Root deploy shim for the Render ``doppl-fusion-demo`` web service.

The live service runs ``pip install -r requirements.txt`` and
``uvicorn app:app`` from the repo root, but the actual Fusion demo app lives in
``spikes/agenotype/``. This shim makes ``app:app`` resolve from the root: it puts
the spike directory on ``sys.path`` (so the app's sibling imports such as
``fusion_demo`` and ``html_trace`` resolve) and loads the real module under a
distinct name to avoid colliding with this file.
"""

from __future__ import annotations

import importlib.util
import os
import sys

_AGENO_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "spikes", "agenotype"
)
if _AGENO_DIR not in sys.path:
    sys.path.insert(0, _AGENO_DIR)

_spec = importlib.util.spec_from_file_location(
    "agenotype_app", os.path.join(_AGENO_DIR, "app.py")
)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load Fusion demo app from {_AGENO_DIR}")

_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

app = _module.app
