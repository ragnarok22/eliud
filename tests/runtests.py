import glob
import inspect
import os
import sys
import unittest

try:
    import eliud  # noqa: F401
except ImportError as e:
    raise RuntimeError(
        "Eliud module not found, reference tests/README.md for instructions."
    ) from e

RUNTESTS_DIR = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":

    def get_name_from_path(path: str) -> str:
        return path.replace(os.path.sep, ".").removesuffix(".py")

    tests_list = glob.glob("test_*")
    print(tests_list)
    suite = []
    for test_target in tests_list:
        if os.path.isdir(test_target):
            for test_file in glob.glob(f"{test_target}/test_*"):
                suite.append(
                    unittest.defaultTestLoader.loadTestsFromName(
                        get_name_from_path(test_file)
                    )
                )
        else:
            suite.append(
                unittest.defaultTestLoader.loadTestsFromName(
                    get_name_from_path(test_target)
                )
            )

    main_suite = unittest.TestSuite(suite)
    unittest.TextTestRunner(verbosity=1).run(main_suite)
