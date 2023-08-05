# coding: utf-8

"""
    CLOUD API

    An enterprise-grade Infrastructure is provided as a Service (IaaS) solution that can be managed through a browser-based \"Data Center Designer\" (DCD) tool or via an easy to use API.   The API allows you to perform a variety of management tasks such as spinning up additional servers, adding volumes, adjusting networking, and so forth. It is designed to allow users to leverage the same power and flexibility found within the DCD visual tool. Both tools are consistent with their concepts and lend well to making the experience smooth and intuitive.  # noqa: E501

    The version of the OpenAPI document: 5.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import ionoscloud
from ionoscloud.api.ip_blocks_api import IPBlocksApi  # noqa: E501
from ionoscloud.rest import ApiException


class TestIPBlocksApi(unittest.TestCase):
    """IPBlocksApi unit test stubs"""

    def setUp(self):
        self.api = ionoscloud.api.ip_blocks_api.IPBlocksApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_ipblocks_delete(self):
        """Test case for ipblocks_delete

        Delete IP Block  # noqa: E501
        """
        pass

    def test_ipblocks_find_by_id(self):
        """Test case for ipblocks_find_by_id

        Retrieve an IP Block  # noqa: E501
        """
        pass

    def test_ipblocks_get(self):
        """Test case for ipblocks_get

        List IP Blocks   # noqa: E501
        """
        pass

    def test_ipblocks_patch(self):
        """Test case for ipblocks_patch

        Partially modify IP Block  # noqa: E501
        """
        pass

    def test_ipblocks_post(self):
        """Test case for ipblocks_post

        Reserve IP Block  # noqa: E501
        """
        pass

    def test_ipblocks_put(self):
        """Test case for ipblocks_put

        Modify IP Block  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
