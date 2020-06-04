#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import Extension

def build(setup_kwargs):
    setup_kwargs.setdefault('ext_modules', []).extend([
        Extension(
            "kadmin",
            libraries=["krb5", "kadm5clnt", "kdb5"],
            include_dirs=["/usr/include/", "/usr/include/et/"],
            sources=[
                "python_kadmin_epita/kadmin.c",
                "python_kadmin_epita/PyKAdminErrors.c",
                "python_kadmin_epita/PyKAdminObject.c",
                "python_kadmin_epita/PyKAdminIterator.c",
                "python_kadmin_epita/PyKAdminPrincipalObject.c",
                "python_kadmin_epita/PyKAdminPolicyObject.c",
                "python_kadmin_epita/PyKAdminCommon.c",
                "python_kadmin_epita/PyKAdminXDR.c",
                "python_kadmin_epita/getdate.c",
            ],
        ),
        Extension(
            "kadmin_local",
            libraries=["krb5", "kadm5srv", "kdb5"],
            include_dirs=["/usr/include/", "/usr/include/et/"],
            sources=[
                "python_kadmin_epita/kadmin.c",
                "python_kadmin_epita/PyKAdminErrors.c",
                "python_kadmin_epita/PyKAdminObject.c",
                "python_kadmin_epita/PyKAdminIterator.c",
                "python_kadmin_epita/PyKAdminPrincipalObject.c",
                "python_kadmin_epita/PyKAdminPolicyObject.c",
                "python_kadmin_epita/PyKAdminCommon.c",
                "python_kadmin_epita/PyKAdminXDR.c",
                "python_kadmin_epita/getdate.c",
            ],
            define_macros=[("KADMIN_LOCAL", "")],
        ),
    ])
