import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        print("All tests passed.")
    else:
        raise SystemExit(1)
