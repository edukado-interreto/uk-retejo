import pytest

pytestmark = pytest.mark.django_db


def combine(char: str, name: str, actions: list[str]):
    return (char.join([t for t in [name, action] if t]) for action in actions)


# fmt: off
MCP_TOOLS = {
    "whoami": [""],
    "schema": ["list", "detail"],
    "api": ["schema", "call"],
    "pages": ["list", "find", "detail", "create", "update", "delete"],
    "pages_actions": [
        "delete", "publish", "unpublish", "copy", "move", "revert",
        "convert_alias", "create_alias", "copy_for_translation"
    ],
    "pages_revisions": ["list", "detail"],
    "images": ["list", "detail", "create", "update", "delete"],
    "documents": ["list", "detail", "create", "update", "delete"],
    "snippets": ["list", "detail", "create", "update", "delete"],
    "snippets_revisions": ["list", "detail"],
    "snippets_actions": ["delete", "publish", "unpublish", "revert", "copy_for_translation"],
    "redirects": ["list", "find", "detail", "create", "update", "delete"],
    "sites": ["list", "detail", "create", "update", "delete"],
    "locales": ["list", "detail", "create", "update", "delete"],
}
# fmt: on


@pytest.mark.parametrize("url", ["/api/v3/docs/", "/api/v3/openapi.json"])
def test_api_v3_docs_routes_are_available(client, url):
    assert client.get(url).status_code == 200


def test_api_v3_openapi_schema(client):
    schema = client.get("/api/v3/openapi.json").json()
    assert "openapi" in schema
    assert schema["info"]["title"] == "Wagtail API"


def test_mcp_route_is_available(client):
    assert client.get("/mcp/").status_code == 405


def test_mcp_list_capabilities(client, api_token):
    data = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json, text/event-stream",
    }
    response = client.post("/mcp/", data, "application/json", headers=headers)
    assert response.status_code == 200

    result = response.json()["result"]
    assert {tool["name"] for tool in result["tools"]} == {
        item
        for name, actions in MCP_TOOLS.items()
        for item in combine("_", name, actions)
    }
