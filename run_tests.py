import sys
import os
import doctest
import unittest
from splinter.browser import Browser
from maggot import start, stop

def load_tests(loader, tests, ignore):
    global browser
    browser = Browser()
    for test_path in filter(lambda path: path.endswith(".txt"), os.listdir("spec")):
        tests.addTests(doctest.DocFileSuite(os.path.join("spec", test_path),
            globs={
                "browser": browser,
            },
            setUp=start,
            tearDown=stop,
        ))
    return tests

def finish(exit_code):
    browser.quit()

if __name__ == "__main__":
    sys.exit = finish
    unittest.main()
