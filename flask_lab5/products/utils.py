import os
import uuid
from werkzeug.utils import secure_filename


def save_product_image(file_storage, blueprint_static_folder):
    if not file_storage or not file_storage.filename:
        return None
    upload_dir = os.path.join(blueprint_static_folder, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(secure_filename(file_storage.filename))[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_filename)
    file_storage.save(file_path)

    # Відносний шлях усередині static блюпринта
    return f"uploads/{unique_filename}"
