from typing import Dict, Optional

from sqlmodel import Field, SQLModel


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    url: str = Field(nullable=False)

    def to_dict(self) -> Dict[str, str]:
        """Convert a object Video in dict"""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
        }
