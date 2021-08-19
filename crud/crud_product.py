from crud.base import CRUDBase
from models import Product, ProductType
from schemas import ProductCreate, ProductTypeCreate


class CRUDProduct(CRUDBase[Product, ProductCreate, None]):
    pass


product = CRUDProduct(Product)


class CRUDProductType(CRUDBase[ProductType, ProductTypeCreate, None]):
    pass


product_type = CRUDProductType(ProductType)
