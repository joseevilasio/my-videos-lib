from typing import Dict, Optional

from sqlmodel import Field, Relationship, SQLModel


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    url: str = Field(nullable=False)

    category_id: int = Field(foreign_key="category.id")

    category: "Category" = Relationship(back_populates="video")

    def to_dict(self) -> Dict[str, str]:
        """Convert a object Video in dict"""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "category_id": self.category_id
        }


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(nullable=False)
    color: str = Field(nullable=False)

    video: "Video" = Relationship(back_populates="category")

    def to_dict(self) -> Dict[str, str]:
        """Convert a object Category in dict"""

        return {
            "id": self.id,
            "title": self.title,
            "color": self.color,
        }
