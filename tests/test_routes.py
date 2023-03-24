

def test_index_positive(client):
    assert client.get("/").status_code == 200


def test_route_negative(client):
    assert client.get("/other").status_code == 404
    
