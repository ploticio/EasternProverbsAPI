from enum import Enum
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Language(str, Enum):
    vietnamese = "Vietnamese"
    chinese = "Chinese"
    japanese = "Japanese"
    korean = "Korean"
    tagalog = "Tagalog"
    thai = "Thai"
    indonesian = "Indonesian"
    hindi = "Hindi"


class Topic(str, Enum):
    family = "Family"
    knowledge = "Knowledge"
    Culture = "Culture"
    preserverence = "Preserverence"
    wealth = "Wealth"
    love = "Love"
    patience = "Patience"
    success = "Success"
    happiness = "Happiness"
    friendship = "Friendship"
    forgiveness = "Forgiveness"
    vigilance = "Vigilance"
    respect = "Respect"
    humility = "Humility"


class ProverbTagLink(SQLModel, table=True):
    proverb_id: Optional[int] = Field(
        default=None, foreign_key="proverb.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class Proverb(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quote: str
    translation: str
    language: str
    tags: List["Tag"] = Relationship(
        back_populates="proverbs", link_model=ProverbTagLink
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    proverbs: List[Proverb] = Relationship(
        back_populates="tags", link_model=ProverbTagLink
    )
