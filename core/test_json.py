from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import SimpleTestCase

from .json_storage import create_item, delete_item, get_item, load_json, update_item


class JsonStorageTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.data_dir = patch("core.json_storage.DATA_DIR", self.temp_dir.name)
        self.data_dir.start()
        self.file_name = "events.json"

    def tearDown(self):
        self.data_dir.stop()
        self.temp_dir.cleanup()

    def test_create_read_update_and_delete_item(self):
        event = create_item(
            self.file_name,
            {
                "title": "Generative AI Workshop",
                "description": "Introduction to Generative AI",
                "category": "AI",
                "date": "2026-09-10",
                "venue": "Seminar Hall",
            },
        )

        self.assertEqual(event["id"], 1)
        self.assertEqual(load_json(self.file_name), [event])
        self.assertEqual(get_item(self.file_name, 1), event)

        updated_event = update_item(
            self.file_name,
            1,
            {
                "title": "Advanced Generative AI Workshop",
                "description": "Learn advanced GenAI concepts",
                "category": "Generative AI",
                "date": "2026-09-15",
                "venue": "AI Lab",
            },
        )

        self.assertEqual(updated_event["id"], 1)
        self.assertEqual(get_item(self.file_name, 1), updated_event)
        self.assertTrue(delete_item(self.file_name, 1))
        self.assertEqual(load_json(self.file_name), [])