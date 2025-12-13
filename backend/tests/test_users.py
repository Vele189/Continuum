#
def test_users_route(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert "message" in response.json()