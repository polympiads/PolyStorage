
import os

from django.test import TestCase
import importlib.util

class TestImport(TestCase):
    def test_import_all (self):
        f = []
        for (dirpath, dirnames, filenames) in os.walk("./polystorage"):
            f.extend(list(map(lambda filename: os.path.join(dirpath, filename), filenames)))
        
        def import_module (path: str):
            if not path.endswith(".py") or "migrations" in path: return

            try:
                spec = importlib.util.spec_from_file_location( "<imported>", path )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as exception:
                print("Exception while loading", path, ":", exception)
        
        for path in f:
            import_module(path)