"""Commands init."""

from application.commands.products.create_product_command import CreateProductCommand
from application.commands.products.delete_product_command import DeleteProductCommand
from application.commands.products.update_product_command import UpdateProductCommand
from application.commands.products.update_stock_command import UpdateStockCommand

__all__ = [
    "CreateProductCommand",
    "DeleteProductCommand",
    "UpdateProductCommand",
    "UpdateStockCommand",
]
