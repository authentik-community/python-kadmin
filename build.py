#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import Extension

extensions = [
    Extension(
        "kadmin",
        libraries=["krb5", "kadm5clnt", "kdb5"],
        include_dirs=["/usr/include/", "/usr/include/et/"],
        sources=[
            "src/kadmin.c",
            "src/PyKAdminErrors.c",
            "src/PyKAdminObject.c",
            "src/PyKAdminIterator.c",
            "src/PyKAdminPrincipalObject.c",
            "src/PyKAdminPolicyObject.c",
            "src/PyKAdminCommon.c",
            "src/PyKAdminXDR.c",
            "src/getdate.c",
        ],
    ),
    Extension(
        "kadmin_local",
        libraries=["krb5", "kadm5srv", "kdb5"],
        include_dirs=["/usr/include/", "/usr/include/et/"],
        sources=[
            "src/kadmin.c",
            "src/PyKAdminErrors.c",
            "src/PyKAdminObject.c",
            "src/PyKAdminIterator.c",
            "src/PyKAdminPrincipalObject.c",
            "src/PyKAdminPolicyObject.c",
            "src/PyKAdminCommon.c",
            "src/PyKAdminXDR.c",
            "src/getdate.c",
        ],
        define_macros=[("KADMIN_LOCAL", "")],
    ),
]


def build(setup_kwargs):
    setup_kwargs.update({
        "ext_modules": extensions,
    })
