from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, Boolean, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# --- Association Tables ---
ProductTagsMap = Table(
    "product_tags_map",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("product_tags.id", ondelete="CASCADE"), primary_key=True),
)

# --- Category Model ---
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    products = relationship("Product", back_populates="category")


# --- Product Tag Model ---
class ProductTag(Base):
    __tablename__ = "product_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    products = relationship("Product", secondary=ProductTagsMap, back_populates="tags")


# --- Product Model ---
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    gst_percentage = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))

    category = relationship("Category", back_populates="products")
    tags = relationship("ProductTag", secondary=ProductTagsMap, back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete")


# --- Product Image Model ---
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    product = relationship("Product", back_populates="images")
