import os
from tinydb import TinyDB, Query

os.makedirs('data', exist_ok=True)
db = TinyDB('data/products.json', indent=4, ensure_ascii=False)
products_table = db.table('products')
ProductQuery = Query()
