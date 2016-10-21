import unittest2

# need to ensure that the package exports the following symbols:
#
# - Modem


class TestImports(unittest2.TestCase):

    def test_import(self):
        # flake8: noqa
        import em73xx
        dir_em73xx = dir(em73xx)
        self.assertIn("Modem", dir_em73xx)
