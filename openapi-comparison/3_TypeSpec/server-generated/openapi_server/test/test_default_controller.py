import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_books_create(self):
        """Test case for books_create

        
        """
        book = {"author":"author","id":0,"title":"title"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/books',
            method='POST',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_delete_book(self):
        """Test case for books_delete_book

        
        """
        headers = { 
        }
        response = self.client.open(
            '/api/books/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_get_book(self):
        """Test case for books_get_book

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/books/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_list(self):
        """Test case for books_list

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
