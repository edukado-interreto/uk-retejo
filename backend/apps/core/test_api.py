import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db
needs_mcp = pytest.mark.skipif(not settings.MCP_ENABLED, reason="MCP_ENABLED is off")

# fmt: off
MCP_TOOLS = {
    "whoami",
    "schema_list", "schema_detail",
    "api_schema", "api_call",
    "pages_list", "pages_find", "pages_detail",
    "pages_create", "pages_update", "pages_delete",
    "pages_actions_delete", "pages_actions_publish", "pages_actions_unpublish",
    "pages_actions_copy", "pages_actions_move", "pages_actions_revert",
    "pages_actions_convert_alias", "pages_actions_create_alias",
    "pages_actions_copy_for_translation",
    "pages_revisions_list", "pages_revisions_detail",
    "images_list", "images_detail", "images_create", "images_update", "images_delete",
    "documents_list", "documents_detail",
    "documents_create", "documents_update", "documents_delete",
    "snippets_list", "snippets_detail",
    "snippets_create", "snippets_update", "snippets_delete",
    "snippets_actions_delete",
    "snippets_revisions_list", "snippets_revisions_detail",
    "snippets_actions_publish", "snippets_actions_unpublish",
    "snippets_actions_revert", "snippets_actions_copy_for_translation",
    "redirects_list", "redirects_find", "redirects_detail",
    "redirects_create", "redirects_update", "redirects_delete",
    "sites_list", "sites_detail", "sites_create", "sites_update", "sites_delete",
    "locales_list", "locales_detail",
    "locales_create", "locales_update", "locales_delete",
    # Evente block tools, from evente.mcp
    "evente_blocks_list", "evente_blocks_detail",
    "evente_blocks_match", "evente_blocks_render",
}
# fmt: on


@pytest.mark.parametrize("url", ["/api/v3/docs/", "/api/v3/openapi.json"])
def test_api_v3_docs_routes_are_available(client, url):
    assert client.get(url).status_code == 200


def test_api_v3_openapi_schema(client):
    schema = client.get("/api/v3/openapi.json").json()
    assert "openapi" in schema
    assert schema["info"]["title"] == "Wagtail API"


@pytest.mark.parametrize(
    "schema_name, fields",
    [
        ("HomePageSchema", {"event", "hero", "body"}),
        ("SimplePageSchema", {"header_image", "body"}),
        ("EventeSiteRootSchema", {"redirect_to_page", "redirect_to_url"}),
    ],
)
def test_api_v3_page_api_fields(client, schema_name, fields):
    schemas = client.get("/api/v3/openapi.json").json()["components"]["schemas"]
    assert fields <= schemas[schema_name]["properties"].keys()


@needs_mcp
def test_mcp_route_is_available(client):
    # GET is not allowed, MCP only accepts POST
    assert client.get("/mcp").status_code == 405


@needs_mcp
def test_mcp_list_capabilities(client, api_token):
    data = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json, text/event-stream",
    }
    response = client.post("/mcp", data, "application/json", headers=headers)
    assert response.status_code == 200

    result = response.json()["result"]
    assert {tool["name"] for tool in result["tools"]} == MCP_TOOLS
