import unittest
from cloudr.utils.filetype import check_file_type


class TestFileType(unittest.TestCase):
    OTHER_TYPE = "other"
    IMAGE_TYPE = "image"
    VIDEO_TYPE = "video"
    AUDIO_TYPE = "audio"
    DOCUMENT_TYPE = "document"

    def test_other_type(self):
        self.assertEqual(check_file_type("myfile"), self.OTHER_TYPE)
        self.assertEqual(check_file_type("myfile.123"), self.OTHER_TYPE)
    
    def test_image_type(self):
        self.assertEqual(check_file_type("myfile.jpg"), self.IMAGE_TYPE)
        self.assertEqual(check_file_type("/favoico.ICO"), self.IMAGE_TYPE)
    
    def test_video_type(self):
        self.assertEqual(check_file_type("/foo/bar/myfile.mP4"), self.VIDEO_TYPE)
    
    def test_audio_type(self):
        self.assertEqual(check_file_type("/etc/myfile.mp4.fLaC"), self.AUDIO_TYPE)
    
    def test_document_type(self):
        self.assertEqual(check_file_type("C:\\myfile.pdf"), self.DOCUMENT_TYPE)


if __name__ == "__main__":
    unittest.main()