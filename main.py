from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select, or_
from database import engine
from models import Proverb, Tag, ProverbTagLink, Language, Topic

app = FastAPI(
    title="Eastern Proverbs API",
    version="1.0.0",
    summary="A collection of various proverbs from Asia",
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get(
    "/proverbs/",
    response_model=List[Proverb],
    tags=["Fetch Data"],
    summary="Fetch proverbs.",
)
def get_proverbs(
    *,
    session: Session = Depends(get_session),
    lang: Annotated[Language | None, Query()] = None,
    tags: Annotated[list[Topic] | None, Query()] = None,
):
    query = select(Proverb)

    if tags:
        query = (
            query.join(ProverbTagLink)
            .join(Tag)
            .where(or_(Tag.topic == tag for tag in tags))
        )

    if lang:
        query = query.where(Proverb.language == lang)

    results = session.exec(query).all()
    return results


@app.get(
    "/proverbs/{proverb_id}",
    response_model=Proverb,
    tags=["Fetch Data"],
    summary="Fetch a proverb by id.",
)
def get_proverb_by_id(*, session: Session = Depends(get_session), proverb_id: int):
    proverb = session.get(Proverb, proverb_id)
    if not proverb:
        raise HTTPException(status_code=404, detail="Proverb not found.")
    return proverb
