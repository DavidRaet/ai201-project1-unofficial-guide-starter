from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"
DATA_DIR = BASE_DIR / "data"
OUTPUT_PATH = DATA_DIR / "ingested_documents.json"
CHUNKS_PATH = DATA_DIR / "chunks.json"

CHUNK_SIZE = 256    # WordPiece tokens — all-MiniLM-L6-v2 max sequence length
CHUNK_OVERLAP = 50  # token overlap between consecutive chunks

CHROMA_DIR      = BASE_DIR / "chroma_db"
COLLECTION_NAME = "vassar_cs_unofficial_guide"
TOP_K           = 5

GROQ_MODEL     = "llama-3.3-70b-versatile"
REFUSAL_STRING = "I don't have enough student-sourced information to answer that question reliably."

# Per-file metadata. Keys that vary per review (course_code, approximate_year)
# are absent here for rmp sources — parsed from each review block instead.
DOCUMENT_METADATA: dict[str, dict] = {
    "RMP_Anna_Gommerstadt.pdf": {
        "source": "rmp",
        "professor_name": "Anna Gommerstadt",
        "raw_url": "https://www.ratemyprofessors.com/professor/2649423",
    },
    "RMP_Jacob_Erickson.pdf": {
        "source": "rmp",
        "professor_name": "Jacob Erickson",
        "raw_url": "https://www.ratemyprofessors.com/professor/3061766",
    },
    "RMP_Jason_Waterman.pdf": {
        "source": "rmp",
        "professor_name": "Jason Waterman",
        "raw_url": "https://www.ratemyprofessors.com/professor/2102591",
    },
    "RMP_Jonathan_Gordon.pdf": {
        "source": "rmp",
        "professor_name": "Jonathan Gordon",
        "raw_url": "https://www.ratemyprofessors.com/professor/2422801",
    },
    "RMP_Peter_Lemieszewski.pdf": {
        "source": "rmp",
        "professor_name": "Peter Lemieszewski",
        "raw_url": "https://www.ratemyprofessors.com/professor/2077804",
    },
    "RMP_Rui_Meireles.pdf": {
        "source": "rmp",
        "professor_name": "Rui Meireles",
        "raw_url": "https://www.ratemyprofessors.com/professor/2308938",
    },
    "Misc News Review on CMPU145.pdf": {
        "source": "miscellany",
        "professor_name": "Anna Gommerstadt",
        "course_code": "CMPU-145",
        "raw_url": "https://miscellanynews.org/2023/11/29/features/student-reviews-foundations-of-computer-science/",
    },
    "CS Class Ordering Thread.pdf": {
        "source": "reddit",
        "raw_url": "https://www.reddit.com/r/vassar/comments/98tpux/computer_science_four_year_course_plan/",
    },
    "Studying Computer Science in Vassar.pdf": {
        "source": "reddit",
        "raw_url": "https://www.reddit.com/r/vassar/comments/1bssjrb/studying_computer_science_in_vassar/",
    },
    "Computer Science General Comment.pdf": {
        "source": "reddit",
        "raw_url": "https://www.reddit.com/r/vassar/comments/ftpgej/computer_science/",
    },
}
