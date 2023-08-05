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

import pulpcore.client.pulp_container
from pulpcore.client.pulp_container.models.container_container_remote import ContainerContainerRemote  # noqa: E501
from pulpcore.client.pulp_container.rest import ApiException

class TestContainerContainerRemote(unittest.TestCase):
    """ContainerContainerRemote unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ContainerContainerRemote
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_container.models.container_container_remote.ContainerContainerRemote()  # noqa: E501
        if include_optional :
            return ContainerContainerRemote(
                name = '0', 
                url = '0', 
                ca_cert = '0', 
                client_cert = '0', 
                client_key = '0', 
                tls_validation = True, 
                proxy_url = '0', 
                username = '0', 
                password = '0', 
                download_concurrency = 1, 
                policy = null, 
                total_timeout = 0.0, 
                connect_timeout = 0.0, 
                sock_connect_timeout = 0.0, 
                sock_read_timeout = 0.0, 
                upstream_name = '0', 
                include_tags = [
                    '0'
                    ], 
                exclude_tags = [
                    '0'
                    ]
            )
        else :
            return ContainerContainerRemote(
                name = '0',
                url = '0',
                upstream_name = '0',
        )

    def testContainerContainerRemote(self):
        """Test ContainerContainerRemote"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
