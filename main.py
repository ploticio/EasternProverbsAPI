from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, or_, func
from database import engine, init_database
from models import Proverb, Tag, ProverbTagLink, Language, Topic, ProverbWithTags

description = "# Eastern Proverbs API ⛩️ \n\nPublic REST API that has collection of various proverbs from Asia. Find the wisdom & inspiration to keep you going throughout the day.\n\nFind the source code [here](https://github.com/ploticio/EasternProverbsAPI)"

app = FastAPI(
    title="Eastern Proverbs API",
    version="1.0.0",
    summary="A collection of various proverbs from Asia.",
    description=description,
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    init_database()


@app.get(
    "/proverbs/",
    response_model=List[ProverbWithTags],
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

    proverbs = []
    for result in results:
        topicProverb = ProverbWithTags.from_orm(result)
        setattr(topicProverb, "topics", [tags.topic for tags in result.tags])
        proverbs.append(topicProverb)

    return proverbs


@app.get(
    "/proverbs/random",
    response_model=ProverbWithTags,
    tags=["Fetch Data"],
    summary="Fetch a random proverb.",
)
def get_random_proverb(*, session: Session = Depends(get_session)):
    proverb = session.exec(select(Proverb).order_by(func.random())).first()
    comp_proverb = ProverbWithTags.from_orm(proverb)
    setattr(comp_proverb, "topics", [tags.topic for tags in proverb.tags])
    return comp_proverb


@app.get(
    "/proverbs/{proverb_id}",
    response_model=ProverbWithTags,
    tags=["Fetch Data"],
    summary="Fetch a proverb by id.",
)
def get_proverb_by_id(*, session: Session = Depends(get_session), proverb_id: int):
    proverb = session.get(Proverb, proverb_id)
    if not proverb:
        raise HTTPException(status_code=404, detail="Proverb not found.")
    comp_proverb = ProverbWithTags.from_orm(proverb)
    setattr(comp_proverb, "topics", [tags.topic for tags in proverb.tags])
    return comp_proverb
