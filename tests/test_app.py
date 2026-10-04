"""Run with:  python -m unittest"""
import os
import tempfile
import unittest

from app import create_app


class PasteTests(unittest.TestCase):
    def setUp(self):
        fd, self.db = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.client = create_app({"DB": self.db, "TESTING": True}).test_client()

    def tearDown(self):
        os.remove(self.db)

    def test_create_view_delete(self):
        r = self.client.post("/", data={"content": "print(1)", "lang": "python"})
        self.assertEqual(r.status_code, 302)
        path = r.headers["Location"]
        page = self.client.get(path)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Delete", page.data)            # creator sees delete
        self.assertEqual(self.client.get(path + "/raw").data, b"print(1)")
        self.client.post(path + "/delete")
        self.assertEqual(self.client.get(path).status_code, 404)

    def test_empty_paste_rejected(self):
        self.assertEqual(self.client.post("/", data={"content": "  "}).status_code, 400)

    def test_api_roundtrip(self):
        r = self.client.post("/api/paste", data="hello", content_type="text/plain")
        self.assertEqual(r.status_code, 201)
        info = r.get_json()
        self.assertEqual(self.client.get("/api/paste/" + info["id"]).get_json()["content"], "hello")
        bad = self.client.delete("/api/paste/" + info["id"], headers={"X-Delete-Token": "x"})
        self.assertEqual(bad.status_code, 403)
        ok = self.client.delete("/api/paste/" + info["id"],
                                headers={"X-Delete-Token": info["delete_token"]})
        self.assertEqual(ok.status_code, 200)


if __name__ == "__main__":
    unittest.main()
