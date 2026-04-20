import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server.models.product_create import ProductCreate  # noqa: E501
from swagger_server.models.product_update import ProductUpdate  # noqa: E501
from swagger_server import util


def app_health_check():  # noqa: E501
    """Health check

     # noqa: E501


    :rtype: InlineResponse200
    """
    return 'do some magic!'


def controllers_product_controller_create_product(body):  # noqa: E501
    """Create a new product

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Product
    """
    if connexion.request.is_json:
        body = ProductCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def controllers_product_controller_delete_product(product_id):  # noqa: E501
    """Delete a product

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: None
    """
    return 'do some magic!'


def controllers_product_controller_get_product_by_id(product_id):  # noqa: E501
    """Get a product by id

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: Product
    """
    return 'do some magic!'


def controllers_product_controller_get_products():  # noqa: E501
    """Get all products

     # noqa: E501


    :rtype: List[Product]
    """
    return 'do some magic!'


def controllers_product_controller_update_product(body, product_id):  # noqa: E501
    """Update a product

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param product_id: 
    :type product_id: str

    :rtype: Product
    """
    if connexion.request.is_json:
        body = ProductUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
