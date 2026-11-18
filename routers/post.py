from time import timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from security import  get_current_user
from datetime import datetime, timezone

router = APIRouter()


@router.post("", response_model=schemas.PostResponse, status_code=201)
def create_post(
    post: schemas.PostCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        db_post = models.Post(
            author_id=current_user.id,
            title=post.title,
            body=post.body,
            status="Live",
            created_at=datetime.now(timezone.utc),
            expires_at=post.expires_at,
        )

        db.add(db_post)
        db.flush()  # generates post ID without committing

        for topic in post.topics:
            db.add(
                models.PostTopic(
                    post_id=db_post.id,
                    topic_id=topic,
                )
            )

        db.commit()
        db.refresh(db_post)

        return db_post
    except IntegrityError as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code=409,
            detail="Failed to create post due to a database integrity error.",
        )

    except Exception as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the post.",
        )