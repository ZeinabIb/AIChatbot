from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

from database import get_db
from models import UserCreate, UserInput, User, Chat, ChatContent, Token
from auth import (
    create_access_token,
    get_current_user,
    verify_password,
    get_password_hash,
)

logger = logging.getLogger(__name__)

router = APIRouter()

model_name = "microsoft/DialoGPT-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    logger.info("Received login request for username: %s", form_data.username)

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        logger.warning("User not found: %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # user exists
    logger.info("User found: %s", form_data.username)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    logger.info("Creating user with username: %s", user.username)
    logger.debug("Hashed password: %s", hashed_password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/generate/")
async def generate_response(
    user_input: UserInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Create or get chat session
    chat = db.query(Chat).filter(Chat.user_id == current_user.user_id).first()
    if not chat:
        chat = Chat(user_id=current_user.user_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)

    new_user_input_ids = tokenizer.encode(
        user_input.text + tokenizer.eos_token, return_tensors="pt"
    )
    bot_input_ids = new_user_input_ids
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
    )

    # Saving to db
    user_message = ChatContent(
        chat_id=chat.chat_id, message_content=user_input.text, message_type=0
    )
    bot_response = ChatContent(
        chat_id=chat.chat_id, message_content=response, message_type=1
    )
    db.add(user_message)
    db.add(bot_response)
    db.commit()
    db.refresh(user_message)
    db.refresh(bot_response)

    return {"response": response}


@router.get("/messages/{user_id}")
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    user_messages = (
        db.query(ChatContent).join(Chat).filter(Chat.user_id == user_id).all()
    )
    return user_messages
