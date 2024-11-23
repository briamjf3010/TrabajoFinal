import unittest
from app import app

def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Verifica que se devuelve HTML

def test_video_feed_route():
    client = app.test_client()
    response = client.get('/video_feed')
    assert response.status_code == 200
    assert response.content_type.startswith('multipart/x-mixed-replace')  # Verifica que el tipo MIME sea el esperado

if __name__ == "__main__":
    unittest.main()