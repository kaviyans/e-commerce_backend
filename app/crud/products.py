from sqlalchemy.orm import Session
from app.models.products import Product, Category, ProductTag, ProductImage
from app.schemas.products import ProductCreate, ProductUpdate

# --- Create Product ---
def create_product(db: Session, product_data: ProductCreate):
    db_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        gst_percentage=product_data.gst_percentage,
        category_id=product_data.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Attach tags
    if product_data.tag_ids:
        tags = db.query(ProductTag).filter(ProductTag.id.in_(product_data.tag_ids)).all()
        db_product.tags = tags

    # Attach images
    if product_data.images:
        for img in product_data.images:
            db_image = ProductImage(image_url=img.image_url, is_primary=img.is_primary, product_id=db_product.id)
            db.add(db_image)
        db.commit()

    db.refresh(db_product)
    return db_product


# --- Read ---
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Product).offset(skip).limit(limit).all()


# --- Update ---
def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    for field, value in product_data.dict(exclude_unset=True).items():
        setattr(db_product, field, value)

    if product_data.tag_ids:
        tags = db.query(ProductTag).filter(ProductTag.id.in_(product_data.tag_ids)).all()
        db_product.tags = tags

    db.commit()
    db.refresh(db_product)
    return db_product


# --- Delete ---
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False


# --- Categories ---
def create_category(db: Session, name: str, description: str = None):
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_categories(db: Session):
    return db.query(Category).all()


# --- Tags ---
def create_tag(db: Session, name: str):
    tag = ProductTag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_all_tags(db: Session):
    return db.query(ProductTag).all()
