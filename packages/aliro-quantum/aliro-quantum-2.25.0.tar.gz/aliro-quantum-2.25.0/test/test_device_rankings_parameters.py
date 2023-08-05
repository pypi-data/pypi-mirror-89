# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aliro_quantum
from aliro_quantum.models.device_rankings_parameters import DeviceRankingsParameters  # noqa: E501
from aliro_quantum.rest import ApiException

class TestDeviceRankingsParameters(unittest.TestCase):
    """DeviceRankingsParameters unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test DeviceRankingsParameters
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum.models.device_rankings_parameters.DeviceRankingsParameters()  # noqa: E501
        if include_optional :
            return DeviceRankingsParameters(
                body = '0', 
                language = '0'
            )
        else :
            return DeviceRankingsParameters(
                body = '0',
                language = '0',
        )

    def testDeviceRankingsParameters(self):
        """Test DeviceRankingsParameters"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
