from fastapi import FastAPI
from openai import OpenAI
import json
import dotenv
import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.utils import (
    upload_file_to_openai,
    generate_pdf_input,
    delete_file_from_openai,
    fetch_lexicon,
    fetch_prompt,
    setup_logger
)


def init_conversation():

    # logger.info('> Uploading medical history to OpenAI...')
    medical_history_file = upload_file_to_openai(client, MEDICAL_HISTORY_PATH)
    pdf_input = generate_pdf_input(client, medical_history_file.id, prompt="Attached is the medical history:")
    
    policy_wording_file = upload_file_to_openai(client, POLICY_WORDING_PATH)
    policy_wording_input = generate_pdf_input(client, policy_wording_file.id, prompt="Attached is the policy wording:")
    
    # Initialize conversation with system context
    return [
        {"role": "user", "content": fetch_prompt()},
        {"role": "system", "content": f"Lexicon: {fetch_lexicon()}"},
        pdf_input,
        policy_wording_input
    ]


app = FastAPI()
logger = setup_logger('medical-histories-backend')
logger.info('🚀 Starting FastAPI backend server...')
logger.info('🐳 Running in Docker container')
logger.info('⚡️ API endpoints ready')
dotenv.load_dotenv()

MODEL = "gpt-4.1"
MODEL_MESSAGES = "gpt-4.1-nano"
MEDICAL_HISTORY_PATH = "./data/file_5062418c-c7d2-4493-8a05-3a39485318c4.pdf"
POLICY_WORDING_PATH = "./data/GeneralPolicyWording-V18.pdf"


class MessageUpdate(BaseModel):
    message: str


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CONVERSATION = init_conversation()


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/launch-analysis")
def launch_analysis():

    response = client.responses.create(
        model=MODEL,
        input=CONVERSATION
    )

    return response


@app.post("/add-message")
async def add_message(message_update: MessageUpdate):

    message = """
    Answer this question: message_update.message

    Use previous messages to answer the question.
    Keep your answer as short and concise as possible.
    provide relevant dates when possible.
    """

    logger.info(f"Adding message: {message_update.message}")

    # Get existing conversation
    CONVERSATION.append({"role": "user", "content": message_update.message})   

    # Get AI response
    response = client.responses.create(
        model=MODEL_MESSAGES,
        input=CONVERSATION
    )

    return response


@app.get("/list-conversation-thread")
async def list_conversation_tokens():
    return {
        "messages": CONVERSATION
    }