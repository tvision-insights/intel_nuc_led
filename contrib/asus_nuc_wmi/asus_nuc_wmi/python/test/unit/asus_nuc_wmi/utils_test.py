"""
The `test.unit.asus_nuc_wmi.utils_test` module provides unit tests for the functions in
`asus_nuc_wmi.utils`.

Classes:
    TestUtils: A unit test class for the functions in `asus_nuc_wmi.utils`.
"""

import fcntl
import tempfile
import unittest

from threading import Thread

from asus_nuc_wmi import NucWmiError
from asus_nuc_wmi.utils import acquire_file_lock, defined_indexes


class TestUtils(unittest.TestCase):
    """
    A unit test class for the functions of `asus_nuc_wmi.utils`

    Methods:
        setUp: Unit test initialization.
        test_acquire_file_lock: Tests that `acquire_file_lock` raises the expected exception when it cannot acquire
                                the lock file and that it successfully acquires the lock file otherwise.
        test_defined_indexes: Tests that `defined_indexes` returns the indices of indexes with defined values.
    """

    def setUp(self):
        """
        Initializes the unit tests.
        """

        self.maxDiff = None # pylint: disable=invalid-name


    def test_acquire_file_lock(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that `acquire_file_lock` can successfully acquire a file lock and returns None.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)


    def test_acquire_file_lock2(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that `acquire_file_lock` raises an exception when the file lock is already acquired.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)

            with open(temp_lock_file.name, 'w', encoding='utf8') as temp_lock_file2:
                with self.assertRaises(NucWmiError) as err:
                    acquire_file_lock(temp_lock_file2)

                self.assertEqual(
                    str(err.exception),
                    'Error (ASUS NUC WMI failed to acquire lock file %s: %s)' % \
                    (temp_lock_file2.name, '[Errno 11] Resource temporarily unavailable')
                )


    def test_acquire_file_lock3(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 3: Test that `acquire_file_lock` can successfully acquire a blocking file lock and returns None.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file, blocking_file_lock=True)

            self.assertEqual(returned_acquire_file_lock, None)


    def test_acquire_file_lock4(self):
        """
        Test that `acquire_file_lock` returns the expected exceptions, return values, or outputs.
        """

        # Branch 4: Test that `acquire_file_lock` hangs when acquiring a blocking file lock on file thats already
        #           locked.

        with tempfile.NamedTemporaryFile(delete=True) as temp_lock_file:
            blocking_thread = None
            returned_acquire_file_lock = acquire_file_lock(temp_lock_file)

            self.assertEqual(returned_acquire_file_lock, None)

            with open(temp_lock_file.name, 'w', encoding='utf8') as temp_lock_file2:
                blocking_thread = Thread(
                    target=acquire_file_lock,
                    args=[temp_lock_file2],
                    kwargs={'blocking_file_lock': True}
                )

                blocking_thread.start()
                blocking_thread.join(10.0)

                self.assertEqual(blocking_thread.is_alive(), True)


            fcntl.flock(temp_lock_file.fileno(), fcntl.LOCK_UN)

            blocking_thread.join(2.0)

            self.assertEqual(blocking_thread.is_alive(), False)


    def test_defined_indexes(self):
        """
        Tests that `defined_indexes` returns the expected exceptions, return values, or outputs.
        """

        # Branch 1: Test that a list input returns a list of indexes with non None values.
        defined_list = [None, "some value", "some value 2"]
        expected_defined_indexes = [1, 2]

        returned_defined_indexes = defined_indexes(defined_list)

        self.assertEqual(
            returned_defined_indexes,
            expected_defined_indexes
        )


    def test_defined_indexes2(self):
        """
        Tests that `defined_indexes` returns the expected exceptions, return values, or outputs.
        """

        # Branch 2: Test that a non list input returns an emptylist of indexes.
        defined_list = None
        expected_defined_indexes = []

        returned_defined_indexes = defined_indexes(defined_list)

        self.assertEqual(
            returned_defined_indexes,
            expected_defined_indexes
        )
