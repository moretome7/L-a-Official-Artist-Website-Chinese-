import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render


def _vite_assets():
    """Read the Vite production manifest and return its entry assets."""
    manifest_path = (
        Path(settings.BASE_DIR)
        / "website"
        / "static"
        / "frontend"
        / ".vite"
        / "manifest.json"
    )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"vite_js": "frontend/.vite/manifest.json", "vite_css": []}

    entry = next(
        (asset for asset in manifest.values() if asset.get("isEntry")),
        None,
    )
    if entry is None:
        return {"vite_js": "frontend/.vite/manifest.json", "vite_css": []}

    return {
        "vite_js": f"frontend/{entry['file']}",
        "vite_css": [f"frontend/{path}" for path in entry.get("css", [])],
    }


def home(request):
    """Display the Vue-powered personal website."""
    return render(request, "website/home.html", _vite_assets())
