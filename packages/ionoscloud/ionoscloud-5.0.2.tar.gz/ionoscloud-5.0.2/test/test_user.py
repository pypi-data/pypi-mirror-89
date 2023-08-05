# coding: utf-8

"""
    CLOUD API

    An enterprise-grade Infrastructure is provided as a Service (IaaS) solution that can be managed through a browser-based \"Data Center Designer\" (DCD) tool or via an easy to use API.   The API allows you to perform a variety of management tasks such as spinning up additional servers, adding volumes, adjusting networking, and so forth. It is designed to allow users to leverage the same power and flexibility found within the DCD visual tool. Both tools are consistent with their concepts and lend well to making the experience smooth and intuitive.  # noqa: E501

    The version of the OpenAPI document: 5.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import ionoscloud
from ionoscloud.models.user import User  # noqa: E501
from ionoscloud.rest import ApiException

class TestUser(unittest.TestCase):
    """User unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test User
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = ionoscloud.models.user.User()  # noqa: E501
        if include_optional :
            return User(
                id = '15f67991-0f51-4efc-a8ad-ef1fb31a480c',
                type = "user",
                href = '<RESOURCE-URI>',
                metadata = ionoscloud.models.user_metadata.UserMetadata(
                    etag = '45480eb3fbfc31f1d916c1eaa4abdcc3', 
                    created_date = '2015-12-04T14:34:09.809Z', 
                    last_login = '2015-12-04T14:34:09.809Z', ),
                properties = ionoscloud.models.user_properties.UserProperties(
                    firstname = '', 
                    lastname = '', 
                    email = '', 
                    administrator = True, 
                    force_sec_auth = True, 
                    sec_auth_active = True, 
                    s3_canonical_user_id = '', 
                    password = '', 
                    active = True, ),
                entities = ionoscloud.models.users_entities.UsersEntities(
                    owns = ionoscloud.models.resources_users.ResourcesUsers(
                        id = '15f67991-0f51-4efc-a8ad-ef1fb31a480c', 
                        type = "collection", 
                        href = 'https://<API_HOST>/cloudapi/v5/um/users/9b1b4c62-1466-11e7-87d3-d7bb7dac0087/owns', 
                        items = [
                            ionoscloud.models.resource.Resource(
                                id = '15f67991-0f51-4efc-a8ad-ef1fb31a480c', 
                                type = "group", 
                                href = 'https://<API_HOST>/cloudapi/v5/um/resources/datacenter/15f67991-0f51-4efc-a8ad-ef1fb31a480c', 
                                metadata = ionoscloud.models.datacenter_element_metadata.DatacenterElementMetadata(
                                    etag = '45480eb3fbfc31f1d916c1eaa4abdcc3', 
                                    created_date = '2015-12-04T14:34:09.809Z', 
                                    created_by = 'user@example.com', 
                                    created_by_user_id = 'user@example.com', 
                                    last_modified_date = '2015-12-04T14:34:09.809Z', 
                                    last_modified_by = 'user@example.com', 
                                    last_modified_by_user_id = '63cef532-26fe-4a64-a4e0-de7c8a506c90', 
                                    state = 'AVAILABLE', ), 
                                properties = ionoscloud.models.resource_properties.ResourceProperties(
                                    name = '', 
                                    sec_auth_protection = True, ), )
                            ], ), 
                    groups = ionoscloud.models.group_users.GroupUsers(
                        id = '15f67991-0f51-4efc-a8ad-ef1fb31a480c', 
                        type = "groups", 
                        href = 'https://<API_HOST>/cloudapi/v5/um/users/9b1b4c62-1466-11e7-87d3-d7bb7dac0087/groups', ), )
            )
        else :
            return User(
                properties = ionoscloud.models.user_properties.UserProperties(
                    firstname = '', 
                    lastname = '', 
                    email = '', 
                    administrator = True, 
                    force_sec_auth = True, 
                    sec_auth_active = True, 
                    s3_canonical_user_id = '', 
                    password = '', 
                    active = True, ),
        )

    def testUser(self):
        """Test User"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
