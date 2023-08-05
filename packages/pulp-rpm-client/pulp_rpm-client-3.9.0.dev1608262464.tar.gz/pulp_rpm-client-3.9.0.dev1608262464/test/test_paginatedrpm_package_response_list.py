# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.paginatedrpm_package_response_list import PaginatedrpmPackageResponseList  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestPaginatedrpmPackageResponseList(unittest.TestCase):
    """PaginatedrpmPackageResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedrpmPackageResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.paginatedrpm_package_response_list.PaginatedrpmPackageResponseList()  # noqa: E501
        if include_optional :
            return PaginatedrpmPackageResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_rpm.models.rpm/package_response.rpm.PackageResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        artifact = '0', 
                        name = '0', 
                        epoch = '0', 
                        version = '0', 
                        release = '0', 
                        arch = '0', 
                        pkg_id = '0', 
                        checksum_type = '0', 
                        summary = '0', 
                        description = '0', 
                        url = '0', 
                        changelogs = pulpcore.client.pulp_rpm.models.changelogs.changelogs(), 
                        files = pulpcore.client.pulp_rpm.models.files.files(), 
                        requires = pulpcore.client.pulp_rpm.models.requires.requires(), 
                        provides = pulpcore.client.pulp_rpm.models.provides.provides(), 
                        conflicts = pulpcore.client.pulp_rpm.models.conflicts.conflicts(), 
                        obsoletes = pulpcore.client.pulp_rpm.models.obsoletes.obsoletes(), 
                        suggests = pulpcore.client.pulp_rpm.models.suggests.suggests(), 
                        enhances = pulpcore.client.pulp_rpm.models.enhances.enhances(), 
                        recommends = pulpcore.client.pulp_rpm.models.recommends.recommends(), 
                        sha256 = '0', 
                        supplements = pulpcore.client.pulp_rpm.models.supplements.supplements(), 
                        location_base = '0', 
                        location_href = '0', 
                        rpm_buildhost = '0', 
                        rpm_group = '0', 
                        rpm_license = '0', 
                        rpm_packager = '0', 
                        rpm_sourcerpm = '0', 
                        rpm_vendor = '0', 
                        rpm_header_start = 56, 
                        rpm_header_end = 56, 
                        is_modular = True, 
                        size_archive = 56, 
                        size_installed = 56, 
                        size_package = 56, 
                        time_build = 56, 
                        time_file = 56, )
                    ]
            )
        else :
            return PaginatedrpmPackageResponseList(
        )

    def testPaginatedrpmPackageResponseList(self):
        """Test PaginatedrpmPackageResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
