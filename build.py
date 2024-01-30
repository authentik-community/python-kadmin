#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import Extension


def build(setup_kwargs):
    setup_kwargs.setdefault("ext_modules", []).extend(
        [
            Extension(
                "kadmin",
                libraries=["krb5", "kadm5clnt", "kdb5"],
                include_dirs=["/usr/include/", "/usr/include/et/"],
                sources=[
                    "kadmin/kadmin.c",
                    "kadmin/PyKAdminErrors.c",
                    "kadmin/PyKAdminObject.c",
                    "kadmin/PyKAdminIterator.c",
                    "kadmin/PyKAdminPrincipalObject.c",
                    "kadmin/PyKAdminPolicyObject.c",
                    "kadmin/PyKAdminCommon.c",
                    "kadmin/PyKAdminXDR.c",
                    "kadmin/getdate.c",
                ],
            ),
            Extension(
                "kadmin_local",
                libraries=["krb5", "kadm5srv", "kdb5"],
                include_dirs=["/usr/include/", "/usr/include/et/"],
                sources=[
                    "kadmin/kadmin.c",
                    "kadmin/PyKAdminErrors.c",
                    "kadmin/PyKAdminObject.c",
                    "kadmin/PyKAdminIterator.c",
                    "kadmin/PyKAdminPrincipalObject.c",
                    "kadmin/PyKAdminPolicyObject.c",
                    "kadmin/PyKAdminCommon.c",
                    "kadmin/PyKAdminXDR.c",
                    "kadmin/getdate.c",
                ],
                define_macros=[("KADMIN_LOCAL", "")],
            ),
        ]
    )
