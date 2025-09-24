import unittest

def main():
    # Discover and run all tests in this package
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="src/unit_test", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        exit(1)

if __name__ == "__main__":
    main()
