def test_index_positive(client):
    """Test to check if index route is return OK"""

    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World! MyVideos API" in response.data


def test_route_negative(client):
    """Negative test to check if the non-existent
    route is returning Not Found"""

    response = client.get("/fake_route")
    assert response.status_code == 404


def test_list_videos_positive(client):
    """Test to check if list videos route is return OK"""

    response = client.get("/videos")
    assert response.status_code == 200


def test_one_video_positive_data(engine, client):
    """Test to check if one video route is return OK"""

    with engine.connect() as conn:
        videos = [
            {
                "title": """Engenheiro de software ou Programador?
                com Paulo Silveira""",
                "description": """Engenheiro de software, pessoa que
                programa ou dev, o que você é?""",
                "url": "https://www.youtube.com/watch?v=Gm6U-AxXEQ0",
            },
            {
                "title": "Estrutura de dados com Roberta Arcoverde",
                "description": """O que são estrutura de dados e como
                podem ser aplicadas na programação?""",
                "url": "https://www.youtube.com/watch?v=57VqgNjbzrg",
            },
        ]

        conn.exec_driver_sql(
            """\
                INSERT INTO video(title, description, url)
                VALUES (:title, :description, :url);
                """,
            videos,
        )
        conn.commit()

        result = conn.exec_driver_sql("SELECT * FROM video;").fetchone()

        
        response_1 = client.get("/videos/1")
        response_2 = client.get("/videos/2")

        assert result is not None        
        assert response_1.status_code == 200
        assert response_1.status_code == 200
        assert b"Engenheiro de software" in response_1.data
        assert b"Estrutura de dados" in response_2.data
