import os
import logging
from dada_test import BaseTest

import dada_settings
from dada_utils import path

import dada_http

TEST_LOGGER = logging.getLogger()


class UtilTests(BaseTest):
    def test_http_download_file(self):
        local_path = dada_http.download_file("http://example.com/")
        assert path.exists(local_path)
        path.remove(local_path)


if __name__ == "__main__":
    unittest.main()
