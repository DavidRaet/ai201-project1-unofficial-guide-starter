import os
from typing import TYPE_CHECKING

from src.config import GROQ_MODEL, REFUSAL_STRING, TOP_K

if TYPE_CHECKING:
    import groq as _groq

_groq_client: "_groq.Groq | None" = None


def get_groq_client() -> "_groq.Groq":
    global _groq_client
    if _groq_client is None:
        import groq
        _groq_client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
    return _groq_client


def build_context_block(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        fields = [meta["source"]]
        if "professor_name" in meta:
            fields.append(meta["professor_name"])
        if "course_code" in meta:
            fields.append(meta["course_code"])
        if "approximate_year" in meta:
            fields.append(str(meta["approximate_year"]))
        fields.append(meta["raw_url"])
        header = f"[Source {i}] ({' | '.join(fields)})"
        parts.append(f"{header}\n{chunk['text']}")
    return "\n\n".join(parts)


def build_system_prompt() -> str:
    return f"""You are an assistant that helps Vassar College CS students learn about courses and professors.

STRICT GROUNDING RULE: Answer ONLY using the numbered sources provided in the user message. Do NOT use any knowledge from your training data about courses, professors, workloads, or Vassar College. If a fact is not stated in the provided sources, do not include it in your answer.

CITATION RULE: Every claim you make must be cited inline using [Source N] notation, where N is the number of the source it comes from.

SOURCE LIST RULE: At the end of every response, include a "Sources:" section that lists each source you cited, with its URL.

REFUSAL RULE: If the provided sources do not contain enough information to answer the question, respond with EXACTLY the following sentence and nothing else:
{REFUSAL_STRING}""" 


def generate_response(query: str, chunks: list[dict]) -> str:
    if not chunks:
        return REFUSAL_STRING

    context = build_context_block(chunks)
    user_message = f"{context}\n\nQuestion: {query}"

    response = get_groq_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user",   "content": user_message},
        ],
        temperature=0,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    from dotenv import load_dotenv
    load_dotenv()

    from src.vectorstore import make_persistent_client, make_collection, retrieve
    from src.config import COLLECTION_NAME

    client = make_persistent_client()
    collection = make_collection(client)

    query = "Are Professor Anna Gommerstadt's lectures for CMPU-145 well-received by students?"
    print(f"Query: {query}\n")

    chunks = retrieve(query, collection, k=TOP_K)
    answer = generate_response(query, chunks)
    print(answer)


if __name__ == "__main__":
    main()
