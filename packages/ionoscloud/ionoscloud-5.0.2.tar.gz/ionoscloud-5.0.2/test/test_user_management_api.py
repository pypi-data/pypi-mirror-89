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
from ionoscloud.api.user_management_api import UserManagementApi  # noqa: E501
from ionoscloud.rest import ApiException


class TestUserManagementApi(unittest.TestCase):
    """UserManagementApi unit test stubs"""

    def setUp(self):
        self.api = ionoscloud.api.user_management_api.UserManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_um_groups_delete(self):
        """Test case for um_groups_delete

        Delete a Group  # noqa: E501
        """
        pass

    def test_um_groups_find_by_id(self):
        """Test case for um_groups_find_by_id

        Retrieve a Group  # noqa: E501
        """
        pass

    def test_um_groups_get(self):
        """Test case for um_groups_get

        List All Groups.  # noqa: E501
        """
        pass

    def test_um_groups_post(self):
        """Test case for um_groups_post

        Create a Group  # noqa: E501
        """
        pass

    def test_um_groups_put(self):
        """Test case for um_groups_put

        Modify a group  # noqa: E501
        """
        pass

    def test_um_groups_resources_get(self):
        """Test case for um_groups_resources_get

        Retrieve resources assigned to a group  # noqa: E501
        """
        pass

    def test_um_groups_shares_delete(self):
        """Test case for um_groups_shares_delete

        Remove a resource from a group  # noqa: E501
        """
        pass

    def test_um_groups_shares_find_by_resource_id(self):
        """Test case for um_groups_shares_find_by_resource_id

        Retrieve a group share  # noqa: E501
        """
        pass

    def test_um_groups_shares_get(self):
        """Test case for um_groups_shares_get

        List Group Shares   # noqa: E501
        """
        pass

    def test_um_groups_shares_post(self):
        """Test case for um_groups_shares_post

        Add a resource to a group  # noqa: E501
        """
        pass

    def test_um_groups_shares_put(self):
        """Test case for um_groups_shares_put

        Modify resource permissions of a group  # noqa: E501
        """
        pass

    def test_um_groups_users_delete(self):
        """Test case for um_groups_users_delete

        Remove a user from a group  # noqa: E501
        """
        pass

    def test_um_groups_users_get(self):
        """Test case for um_groups_users_get

        List Group Members   # noqa: E501
        """
        pass

    def test_um_groups_users_post(self):
        """Test case for um_groups_users_post

        Add a user to a group  # noqa: E501
        """
        pass

    def test_um_resources_find_by_type(self):
        """Test case for um_resources_find_by_type

        Retrieve a list of Resources by type.  # noqa: E501
        """
        pass

    def test_um_resources_find_by_type_and_id(self):
        """Test case for um_resources_find_by_type_and_id

        Retrieve a Resource by type.  # noqa: E501
        """
        pass

    def test_um_resources_get(self):
        """Test case for um_resources_get

        List All Resources.  # noqa: E501
        """
        pass

    def test_um_users_delete(self):
        """Test case for um_users_delete

        Delete a User  # noqa: E501
        """
        pass

    def test_um_users_find_by_id(self):
        """Test case for um_users_find_by_id

        Retrieve a User  # noqa: E501
        """
        pass

    def test_um_users_get(self):
        """Test case for um_users_get

        List all Users   # noqa: E501
        """
        pass

    def test_um_users_groups_get(self):
        """Test case for um_users_groups_get

        Retrieve a User's group resources  # noqa: E501
        """
        pass

    def test_um_users_owns_get(self):
        """Test case for um_users_owns_get

        Retrieve a User's own resources  # noqa: E501
        """
        pass

    def test_um_users_post(self):
        """Test case for um_users_post

        Create a user  # noqa: E501
        """
        pass

    def test_um_users_put(self):
        """Test case for um_users_put

        Modify a user  # noqa: E501
        """
        pass

    def test_um_users_s3keys_delete(self):
        """Test case for um_users_s3keys_delete

        Delete a S3 key  # noqa: E501
        """
        pass

    def test_um_users_s3keys_find_by_key_id(self):
        """Test case for um_users_s3keys_find_by_key_id

        Retrieve given S3 key belonging to the given User  # noqa: E501
        """
        pass

    def test_um_users_s3keys_get(self):
        """Test case for um_users_s3keys_get

        Retrieve a User's S3 keys  # noqa: E501
        """
        pass

    def test_um_users_s3keys_post(self):
        """Test case for um_users_s3keys_post

        Create a S3 key for the given user  # noqa: E501
        """
        pass

    def test_um_users_s3keys_put(self):
        """Test case for um_users_s3keys_put

        Modify a S3 key having the given key id  # noqa: E501
        """
        pass

    def test_um_users_s3ssourl_get(self):
        """Test case for um_users_s3ssourl_get

        Retrieve S3 object storage single signon URL for the given user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
