import pytest
from bs4 import BeautifulSoup
from django_vite.core.asset_loader import DjangoViteAssetLoader

from apps.registration.blocks import VueJsBlock, VueModule


@pytest.fixture
def vite_dev_mode(settings, monkeypatch):
    """Vite dev server mode: no manifest.json needed, as in CI before `npm run build`."""
    settings.DJANGO_VITE = {
        "default": {**settings.DJANGO_VITE["default"], "dev_mode": True}
    }
    # The loader is a singleton that reads the settings once
    monkeypatch.setattr(DjangoViteAssetLoader, "_instance", None)


@pytest.mark.parametrize("module", VueModule.values)
def test_vuejs_block_entrypoint(module):
    block = VueJsBlock()
    context = block.get_context(block.to_python({"vue_module": module}))
    assert context["entrypoint"] == f"entrypoints/{module}.js"


def test_vuejs_block_default_module():
    assert VueJsBlock().get_default()["vue_module"] == VueModule.REGISTRATION


def test_entrypoints_exist(settings):
    """Every Vue module of the block has an entrypoint in uk-aligxilo."""
    entrypoints = settings.BASE_DIR.parent / "uk-aligxilo/entrypoints"
    if not entrypoints.is_dir():
        pytest.skip("uk-aligxilo is not next to the backend (Docker image)")
    assert {f"{m}.js" for m in VueModule.values} <= {
        f.name for f in entrypoints.iterdir()
    }


def test_vuejs_block_renders_mount_point(vite_dev_mode):
    block = VueJsBlock()
    html = block.render(block.to_python({"vue_module": VueModule.PRICE}))
    soup = BeautifulSoup(html, "html.parser")

    assert soup.select_one("div#vue-price.mount-point") is not None
    script = soup.select_one("script[type=module]")
    assert script["src"].endswith("/entrypoints/price.js")
