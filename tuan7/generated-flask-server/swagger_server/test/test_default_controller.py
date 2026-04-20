# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server.models.product_create import ProductCreate  # noqa: E501
from swagger_server.models.product_update import ProductUpdate  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_app_health_check(self):
        """Test case for app_health_check

        Health check
        """
        response = self.client.open(
            '/health',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controllers_product_controller_create_product(self):
        """Test case for controllers_product_controller_create_product

        Create a new product
        """
        body = ProductCreate()
        response = self.client.open(
            '/products',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controllers_product_controller_delete_product(self):
        """Test case for controllers_product_controller_delete_product

        Delete a product
        """
        response = self.client.open(
            '/products/{product_id}'.format(product_id='product_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controllers_product_controller_get_product_by_id(self):
        """Test case for controllers_product_controller_get_product_by_id

        Get a product by id
        """
        response = self.client.open(
            '/products/{product_id}'.format(product_id='product_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controllers_product_controller_get_products(self):
        """Test case for controllers_product_controller_get_products

        Get all products
        """
        response = self.client.open(
            '/products',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controllers_product_controller_update_product(self):
        """Test case for controllers_product_controller_update_product

        Update a product
        """
        body = ProductUpdate()
        response = self.client.open(
            '/products/{product_id}'.format(product_id='product_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
