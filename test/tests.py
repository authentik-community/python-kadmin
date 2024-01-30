#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
import copy
import gc
import os
import subprocess
import unittest
from pprint import pprint
from types import ModuleType

import k5test

import kadmin
import kadmin_local

TEST_ACCOUNTS = [f"test{i:02d}@KRBTEST.COM" for i in range(100)]


def create_test_accounts():
    with subprocess.Popen(
        ["kadmin.local"],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as k:
        command = ""
        for account in TEST_ACCOUNTS:
            command += f"ank -randkey {account}\n"
        k.communicate(command.encode())
        k.wait()


def delete_test_accounts():
    with subprocess.Popen(
        ["kadmin.local"],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as k:
        command = ""
        for account in TEST_ACCOUNTS:
            command += f"delprinc -force {account}\n"
        k.communicate(command.encode())
        k.wait()


def database_size() -> int:
    with subprocess.Popen(
        ["kadmin.local"],
        shell=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as k:
        stdoutdata, _ = k.communicate("listprincs\n".encode())
        k.wait()
    # We subtract two because the pipe contains the following in addition to the principals
    #
    # kadmin.local:  listprincs
    # kadmin.local:
    #
    return stdoutdata.decode().count("\n") - 2


class KerberosTestCase(k5test.unit.KerberosTestCase):
    @classmethod
    def setUpClass(cls):
        cls.realm = k5test.realm.K5Realm(
            start_kadmind=True,
        )
        cls._saved_env = copy.deepcopy(os.environ)
        for k, v in cls.realm.env.items():
            os.environ[k] = v
        cls.realm.prep_kadmin()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        for k in copy.deepcopy(os.environ):
            if k in cls._saved_env:
                os.environ[k] = cls._saved_env[k]
            else:
                del os.environ[k]
        cls._saved_env = None


class KAdminTests(KerberosTestCase):
    mod: ModuleType = kadmin

    def setUp(self):
        self.kadm = self.mod.init_with_ccache(
            self.realm.admin_princ, self.realm.kadmin_ccache
        )
        if self.kadm is None:
            self.stop()

    def test_init_with_keytab(self):
        keytab = os.path.join(self.realm.tmpdir, "admin_keytab")
        self.realm.extract_keytab(self.realm.admin_princ, keytab)
        kadm = self.mod.init_with_keytab(self.realm.admin_princ, keytab)
        self.assertIsNotNone(kadm)

    def test_init_with_ccache(self):
        kadm = self.mod.init_with_ccache(
            self.realm.admin_princ, self.realm.kadmin_ccache
        )
        self.assertIsNotNone(kadm)

    def test_init_with_ccache_no_name(self):
        kadm = self.mod.init_with_ccache(None, self.realm.kadmin_ccache)
        self.assertIsNotNone(kadm)

    def test_init_with_password(self):
        kadm = self.mod.init_with_password(
            self.realm.admin_princ, self.realm.password("admin")
        )
        self.assertIsNotNone(kadm)

    def test_create(self):
        pre_size = database_size()
        for account in TEST_ACCOUNTS:
            self.kadm.ank(account)
        post_size = database_size()
        self.assertEqual(pre_size + len(TEST_ACCOUNTS), post_size)
        delete_test_accounts()

    def test_delete(self):
        create_test_accounts()
        pre_size = database_size()
        for account in TEST_ACCOUNTS:
            self.kadm.delprinc(account)
        post_size = database_size()
        self.assertEqual(pre_size, len(TEST_ACCOUNTS) + post_size)
        delete_test_accounts()

    def test_double_create(self):
        delete_test_accounts()
        account = TEST_ACCOUNTS[0]
        self.kadm.ank(account)
        with self.assertRaises(self.mod.KAdminError):
            self.kadm.ank(account)

    def test_double_delete(self):
        delete_test_accounts()
        account = TEST_ACCOUNTS[0]
        with self.assertRaises(self.mod.KAdminError):
            self.kadm.delprinc(account)

    def test_iteration(self):
        count = 0
        size = database_size()
        for _ in self.kadm.principals():
            count += 1
        self.assertEqual(count, size)

    def test_not_exists(self):
        delete_test_accounts()
        account = TEST_ACCOUNTS[0]
        princ = self.kadm.getprinc(account)
        self.assertIsNone(princ)

    def test_princ_compare_eq(self):
        create_test_accounts()
        account = TEST_ACCOUNTS[0]
        a = self.kadm.getprinc(account)
        b = self.kadm.getprinc(account)
        self.assertEqual(a, b)

    def test_princ_compare_ne(self):
        create_test_accounts()
        account = TEST_ACCOUNTS[0]
        a = self.kadm.getprinc(account)
        account = TEST_ACCOUNTS[1]
        b = self.kadm.getprinc(account)
        self.assertNotEqual(a, b)


class KAdminLocalTests(KAdminTests):
    mod = kadmin_local


def main():
    kadmin_tests = unittest.TestLoader().loadTestsFromTestCase(KAdminTests)
    kadmin_local_tests = unittest.TestLoader().loadTestsFromTestCase(KAdminLocalTests)

    unittest.TextTestRunner(verbosity=2).run(kadmin_tests)
    unittest.TextTestRunner(verbosity=2).run(kadmin_local_tests)


if __name__ == "__main__":
    main()

# delete global constants
del TEST_ACCOUNTS

# collect memory so our valgrind reports clear up any still reachable which shouldnt be
gc.collect()

pprint(locals())
pprint(globals())
