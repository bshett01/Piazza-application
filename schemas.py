from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, EmailStr, Field,field_validator,ConfigDict


ALLOWED_TOPICS = {"politics", "health", "sport", "tech"}
# Request body for registration.
class UserCreate(BaseModel):
  
    email: EmailStr
    password: str = Field(min_length=6)


# Request body for login.
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response body for a user.
# Notice that the password is not included.
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


# Response body returned after login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str



class PostCreate(BaseModel):
  
    title: str= Field(min_length=1)
    body: str = Field(min_length=1) 
    topics: list[str]= Field(min_length=1) 
    expires_at: datetime
    @field_validator("topics")
    @classmethod
    def validate_topics(cls, topics: list[str]) -> list[str]:

        normalized_topics = []

        for topic in topics:
            normalized = topic.strip().lower()

            if normalized not in ALLOWED_TOPICS:
                raise ValueError(
                    f"'{topic}' is not a valid topic. "
                    f"Allowed topics: {', '.join(ALLOWED_TOPICS)}"
                )

            normalized_topics.append(normalized)

        return normalized_topics

    
    @field_validator("expires_at")
    @classmethod
    def validate_expiry(cls, value):
        if value <= datetime.now(timezone.utc):
            raise ValueError("expires_at must be in the future")
        return value

class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    status: str
    created_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
    


class PostTopic(BaseModel):
    post_id: str
    topic_id: str