import pytest
from pathlib import Path
from src.ingest import (
    extract_pdf_text,
    parse_rmp_reviews,
    parse_single_document,
    ingest_documents,
)
from src.config import DOCUMENTS_DIR, DOCUMENT_METADATA

ERICKSON_PDF = DOCUMENTS_DIR / "RMP_Jacob_Erickson.pdf"
MISC_PDF = DOCUMENTS_DIR / "Misc News Review on CMPU145.pdf"
REDDIT_PDF = DOCUMENTS_DIR / "CS Class Ordering Thread.pdf"


# ── RMP parsing ──────────────────────────────────────────────────────────────

class TestParseRmpReviews:
    def setup_method(self):
        text = extract_pdf_text(ERICKSON_PDF)
        base = DOCUMENT_METADATA["RMP_Jacob_Erickson.pdf"]
        self.records = parse_rmp_reviews(text, base)

    def test_produces_four_records(self):
        assert len(self.records) == 4

    def test_course_codes(self):
        codes = [r["metadata"]["course_code"] for r in self.records]
        assert codes == ["CMPU-101", "CMPU-241", "CMPU-241", "CMPU-101"]

    def test_years(self):
        years = [r["metadata"]["approximate_year"] for r in self.records]
        assert years == [2025, 2025, 2025, 2024]

    def test_text_has_no_triple_quotes(self):
        for r in self.records:
            assert '"""' not in r["text"]

    def test_text_has_no_year_line(self):
        for r in self.records:
            assert "year:" not in r["text"]

    def test_spacing_variant_normalises(self):
        # Comment #4 uses "CMPU-101-" (no space before dash)
        assert self.records[3]["metadata"]["course_code"] == "CMPU-101"

    def test_required_metadata_keys_present(self):
        for r in self.records:
            for key in ("source", "professor_name", "course_code", "raw_url", "approximate_year"):
                assert key in r["metadata"], f"Missing key: {key}"

    def test_year_is_int(self):
        for r in self.records:
            assert isinstance(r["metadata"]["approximate_year"], int)

    def test_course_code_is_scalar_string(self):
        for r in self.records:
            assert isinstance(r["metadata"]["course_code"], str)


# ── Reddit parsing ────────────────────────────────────────────────────────────

class TestParseRedditDocument:
    def setup_method(self):
        text = extract_pdf_text(REDDIT_PDF)
        base = DOCUMENT_METADATA["CS Class Ordering Thread.pdf"]
        self.records = parse_single_document(text, base)

    def test_produces_one_record(self):
        assert len(self.records) == 1

    def test_no_professor_name(self):
        assert "professor_name" not in self.records[0]["metadata"]

    def test_no_course_code(self):
        assert "course_code" not in self.records[0]["metadata"]

    def test_no_approximate_year(self):
        assert "approximate_year" not in self.records[0]["metadata"]

    def test_source_and_url_present(self):
        meta = self.records[0]["metadata"]
        assert meta["source"] == "reddit"
        assert "raw_url" in meta

    def test_text_is_nonempty(self):
        assert len(self.records[0]["text"].strip()) > 0


# ── Miscellany parsing ────────────────────────────────────────────────────────

class TestParseMiscellanyDocument:
    def setup_method(self):
        text = extract_pdf_text(MISC_PDF)
        base = DOCUMENT_METADATA["Misc News Review on CMPU145.pdf"]
        self.records = parse_single_document(text, base)

    def test_produces_one_record(self):
        assert len(self.records) == 1

    def test_source_is_miscellany(self):
        assert self.records[0]["metadata"]["source"] == "miscellany"

    def test_professor_name_present(self):
        assert self.records[0]["metadata"]["professor_name"] == "Anna Gommerstadt"

    def test_course_code_present(self):
        assert self.records[0]["metadata"]["course_code"] == "CMPU-145"

    def test_no_approximate_year(self):
        assert "approximate_year" not in self.records[0]["metadata"]


# ── Full ingestion ────────────────────────────────────────────────────────────

class TestIngestDocuments:
    def setup_method(self):
        self.records = ingest_documents()

    def test_total_record_count_reasonable(self):
        # 6 RMP files (multiple reviews each) + 4 prose docs = well above 10
        assert len(self.records) > 10

    def test_all_records_have_source_and_url(self):
        for r in self.records:
            assert "source" in r["metadata"]
            assert "raw_url" in r["metadata"]

    def test_no_record_has_list_metadata(self):
        for r in self.records:
            for v in r["metadata"].values():
                assert not isinstance(v, list), f"List found in metadata: {r['metadata']}"

    def test_no_null_metadata_values(self):
        for r in self.records:
            for v in r["metadata"].values():
                assert v is not None

    def test_source_values_are_valid(self):
        valid = {"rmp", "reddit", "miscellany", "syllabus", "official"}
        for r in self.records:
            assert r["metadata"]["source"] in valid
