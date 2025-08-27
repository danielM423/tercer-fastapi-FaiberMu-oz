from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from datetime import datetime

class Book(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., min_length=2)
    isbn: str = Field(..., regex=r"^97[89]-\d{10}$")
    year: int = Field(..., ge=1800, le=datetime.now().year)
    rating: float = Field(..., ge=0, le=5)
    tags: List[str] = []
    price: float = Field(..., gt=0)
    is_available: bool = Field(True)
    is_bestseller: bool = Field(False)

    # --- VALIDADORES CUSTOM ---
    @validator("title")
    def capitalize_title(cls, v):
        return v.title()

    @validator("author")
    def author_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El autor no puede ser solo números")
        return v

    @validator("tags")
    def unique_tags(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("No se permiten tags duplicados")
        return v

    @root_validator
    def cross_field_validations(cls, values):
        # 1. Bestseller requiere rating >= 4.0
        if values.get("is_bestseller") and values.get("rating", 0) < 4.0:
            raise ValueError("Los libros bestseller deben tener rating >= 4.0")

        # 2. Libros antiguos (<1900) deben tener precio especial
        if values.get("year") < 1900 and values.get("price", 0) < 5:
            raise ValueError("Los libros antiguos deben tener precio >= 5")
        return values
