from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from .forms import ProductForm, CATEGORY_CHOICES
from . import db as product_db
from .utils import save_product_image

products_bp = Blueprint(
    'products',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/products/static'
)

CATEGORY_MAP = dict(CATEGORY_CHOICES)


def get_next_id():
    all_items = product_db.products_table.all()
    if not all_items:
        return 1
    return max(item['id'] for item in all_items) + 1


@products_bp.route('/product')
def list_products():
    products = product_db.products_table.all()
    return render_template('products/list.html', products=products, category_map=CATEGORY_MAP)


@products_bp.route('/product/<int:id>')
def view_product(id):
    product = product_db.products_table.get(product_db.ProductQuery.id == id)
    if not product:
        abort(404)
    return render_template('products/detail.html', product=product, category_map=CATEGORY_MAP)


@products_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_product_image(form.image.data, products_bp.static_folder)
        new_product = {
            'id': get_next_id(),
            'name': form.name.data,
            'content': form.content.data,
            'price': round(float(form.price.data), 2),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        product_db.products_table.insert(new_product)
        flash('Товар успішно додано до каталогу!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/form.html', form=form, title='Додати новий товар')


@products_bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = product_db.products_table.get(product_db.ProductQuery.id == id)
    if not product:
        abort(404)

    form = ProductForm(data=product)
    if form.validate_on_submit():
        image_path = product.get('image')
        if form.image.data and form.image.data.filename:
            image_path = save_product_image(form.image.data, products_bp.static_folder)

        updated_data = {
            'name': form.name.data,
            'content': form.content.data,
            'price': round(float(form.price.data), 2),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path
            # id та created_at залишаються без змін
        }
        product_db.products_table.update(updated_data, product_db.ProductQuery.id == id)
        flash('Зміни товару успішно збережено!', 'success')
        return redirect(url_for('products.view_product', id=id))

    return render_template('products/form.html', form=form, product=product, title='Редагувати товар')


@products_bp.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = product_db.products_table.get(product_db.ProductQuery.id == id)
    if not product:
        abort(404)
    product_db.products_table.remove(product_db.ProductQuery.id == id)
    flash('Товар успішно видалено.', 'info')
    return redirect(url_for('products.list_products'))
