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
from pulpcore.client.pulp_rpm.models.rpm_rpm_repository_response import RpmRpmRepositoryResponse  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestRpmRpmRepositoryResponse(unittest.TestCase):
    """RpmRpmRepositoryResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RpmRpmRepositoryResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.rpm_rpm_repository_response.RpmRpmRepositoryResponse()  # noqa: E501
        if include_optional :
            return RpmRpmRepositoryResponse(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                versions_href = '0', 
                latest_version_href = '0', 
                name = '0', 
                description = '0', 
                remote = '0', 
                metadata_signing_service = '0', 
                retain_package_versions = 0
            )
        else :
            return RpmRpmRepositoryResponse(
                name = '0',
        )

    def testRpmRpmRepositoryResponse(self):
        """Test RpmRpmRepositoryResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
