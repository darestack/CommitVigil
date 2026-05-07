import hashlib

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel, EmailStr, Field

from src.agents.commitment_extractor import CommitmentExtractor
from src.api.deps import get_api_key
from src.core.database import get_user_by_git_email
from src.core.logging import logger

router = APIRouter()


class GitCommitInbound(BaseModel):
    author_email: EmailStr
    message: str = Field(..., max_length=2000)


@router.post(
    "/ingest/raw", dependencies=[Depends(get_api_key), Depends(RateLimiter(times=10, seconds=60))]
)
async def ingest_raw_commitment(user_id: str, raw_text: str):
    """
    Extract a structured commitment record from raw chat text.
    """
    extractor = CommitmentExtractor()

    extracted = await extractor.parse_conversation(raw_text)

    # Hash identity before logging.
    identity_hash = (
        hashlib.sha256(extracted.who.encode()).hexdigest()[:12] if extracted.who else "none"
    )

    # In a full workflow, this would be persisted to a tasks table.
    logger.info(
        "commitment_extracted",
        user_id=user_id,
        task=extracted.what,
        owner_hash=identity_hash,
    )

    return {
        "status": "extracted",
        "owner": extracted.who,
        "task": extracted.what,
        "deadline": extracted.when,
        "message": f"Successfully parsed promise from {extracted.who}",
    }


@router.post(
    "/ingest/git", dependencies=[Depends(get_api_key), Depends(RateLimiter(times=10, seconds=60))]
)
async def ingest_git_commitment(commit_data: GitCommitInbound):
    """
    Extract commitments from Git commit messages.
    """
    extractor = CommitmentExtractor()
    author_email = commit_data.author_email
    message = commit_data.message

    user = await get_user_by_git_email(author_email)
    user_id = user.user_id if user else "unknown_git_user"

    extracted = await extractor.parse_conversation(message)
    logger.info("git_commitment_extracted", user_id=user_id, task=extracted.what)

    return {
        "status": "extracted",
        "owner": extracted.who,
        "task": extracted.what,
        "identity_matched": user_id != "unknown_git_user",
    }
