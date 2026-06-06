import os
from unittest.mock import MagicMock, patch

import pytest

from src.config import GROQ_MODEL, REFUSAL_STRING
from src.generate import build_context_block, build_system_prompt, generate_response

# ── Sample fixtures ────────────────────────────────────────────────────────────

RMP_CHUNK = {
    "chunk_id": "abc-123",
    "text": "CMPU-101 - Comment #1: Kind, friendly, and caring professor.",
    "metadata": {
        "source": "rmp",
        "professor_name": "Jacob Erickson",
        "course_code": "CMPU-101",
        "approximate_year": 2025,
        "raw_url": "https://www.ratemyprofessors.com/professor/3061766",
        "chunk_index": 0,
    },
}

REDDIT_CHUNK = {
    "chunk_id": "def-456",
    "text": "I think it's important to emphasize that there is no real recommended sequence.",
    "metadata": {
        "source": "reddit",
        "raw_url": "https://www.reddit.com/r/vassar/comments/98tpux/",
        "chunk_index": 0,
    },
}

SAMPLE_CHUNKS = [RMP_CHUNK, REDDIT_CHUNK]


# ── build_context_block ────────────────────────────────────────────────────────

def test_context_block_has_source_labels():
    block = build_context_block(SAMPLE_CHUNKS)
    assert "[Source 1]" in block
    assert "[Source 2]" in block


def test_context_block_includes_chunk_text():
    block = build_context_block(SAMPLE_CHUNKS)
    assert RMP_CHUNK["text"] in block
    assert REDDIT_CHUNK["text"] in block


def test_context_block_includes_professor_name():
    block = build_context_block(SAMPLE_CHUNKS)
    assert "Jacob Erickson" in block


def test_context_block_omits_missing_fields():
    block = build_context_block(SAMPLE_CHUNKS)
    # The Reddit chunk has no professor_name — "None" must not appear
    assert "None" not in block


# ── build_system_prompt ────────────────────────────────────────────────────────

def test_system_prompt_contains_refusal_string():
    prompt = build_system_prompt()
    assert REFUSAL_STRING in prompt


def test_system_prompt_forbids_outside_knowledge():
    prompt = build_system_prompt()
    lower = prompt.lower()
    assert any(phrase in lower for phrase in [
        "only", "do not use", "never", "outside", "training"
    ]), "System prompt must forbid using outside/training knowledge"


# ── generate_response ─────────────────────────────────────────────────────────

def test_empty_chunks_returns_refusal():
    result = generate_response("What is the workload?", [])
    assert result == REFUSAL_STRING


def _make_mock_groq(content: str) -> MagicMock:
    mock_message = MagicMock()
    mock_message.content = content
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_generate_response_calls_groq_with_correct_model():
    mock_client = _make_mock_groq("Some answer. [Source 1]\n\nSources:\n- [Source 1] rmp")
    with patch("src.generate.get_groq_client", return_value=mock_client):
        generate_response("What is CMPU 101 like?", SAMPLE_CHUNKS)

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == GROQ_MODEL


def test_generate_response_returns_string():
    mock_client = _make_mock_groq("Professor Erickson is kind. [Source 1]\n\nSources:\n- [Source 1] rmp")
    with patch("src.generate.get_groq_client", return_value=mock_client):
        result = generate_response("What is CMPU 101 like?", SAMPLE_CHUNKS)

    assert isinstance(result, str)
    assert len(result) > 0
