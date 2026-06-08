# Project 1 Planning: The Unofficial Guide
---

## Domain
     This Unofficial Guide will focus on student-generated knowledge about Vassar CS inquiries and experiences. This knowledge is valuable because students have a centralized place to ask questions and share information about courses, professors, and workloads. By building a RAG system that can retrieve and generate responses based on this student-generated content, we can provide prospective and current students with insights that are grounded in real experiences, helping them make informed decisions about their course selections and academic or career paths. 
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source            | Description                                                                                          | URL or location                                                                                                |
| -- | ----------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1  | Rate My Professor | Student reviews of Jacob Erickson (CMPU 101, CMPU 241)                                               | https://www.ratemyprofessors.com/professor/3061766
| 2  | Rate My Professor | Student reviews of Peter Lemieszewski (CMPU 102)                                                     | https://www.ratemyprofessors.com/professor/2077804
| 3  | Rate My Professor | Student reviews of Anna Gommerstadt (CMPU 145)                                                       | https://www.ratemyprofessors.com/professor/2649423
| 4  | Rate My Professor | Student reviews of Rui Meireles (CMPU 203)                                                           | https://www.ratemyprofessors.com/professor/2308938
| 5  | Rate My Professor | Student reviews of Jason Waterman (CMPU 224)                                                         | https://www.ratemyprofessors.com/professor/2102591
| 6  | Rate My Professor | Student reviews of Jonathan Gordon (CMPU 240)                                                        | https://www.ratemyprofessors.com/professor/2422801                                             |
| 7  | Miscellany News   | Student review article on CMPU 145 Foundations of CS                                                 | https://miscellanynews.org/2023/11/29/features/student-reviews-foundations-of-computer-science/  |
| 8  | Reddit r/vassar   | CS four-year course plan thread — students discussing course sequencing including CMPU 101, 102, 145 | https://www.reddit.com/r/vassar/comments/98tpux/computer_science_four_year_course_plan/                  |
| 9  | Reddit r/vassar   | Reddit Thread - Studying Computer Science in Vassar          | https://www.reddit.com/r/vassar/comments/1bssjrb/studying_computer_science_in_vassar/                                                               |
| 10 | Reddit r/vassar   | Reddit Thread - Computer Science   | https://www.reddit.com/r/vassar/comments/ftpgej/computer_science/                                                                        |

---

## Chunking Strategy

**Chunking strategy:** Separator-Aware Recursive Splitting

**Chunk size:** 256 tokens 

**Overlap:** 50 tokens 

**Reasoning:**  Given that these documents consist of student reviews and discussions, which can vary in length and structure, we apply recursive character splitting to preserve coherent units of information while keeping chunks manageable for retrieval and generation. The splitter uses a priority-ordered cascade of separators, paragraph breaks, line breaks, sentence-ending punctuation, then spaces, and falling back to finer splits only when a chunk still exceeds the size limit. Chunk size is set to [your CHUNK_SIZE] tokens and overlap to [your CHUNK_OVERLAP] tokens, measured using the all-MiniLM-L6-v2 tokenizer. This approach approximates boundary-aware chunking heuristically: it avoids splitting mid-sentence or mid-paragraph whenever possible. The overlap helps preserve context that might otherwise be severed at chunk edges, which is particularly relevant for reviews and discussions where sentiment or reasoning can span multiple sentences.
---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers

**Top-k:** k=5

**Production tradeoff reflection:** Using `all-MiniLM-L6-v2` works just fine as it's a general purpose embedding model for simplicity and relatively short context. So, if I'm working on a review-heavy corpus that won't need too much context, this model works just fine. However, if I were to start embedding more document-heavy material like elaborate blogs, articles, etc. I should consider using models that are specifically designed for longer contexts, such as `jina-embeddings-v2-base-en` (Jina) or `nomic-embed-text-v1.5` (Nomic AI), which can capture more nuanced information from longer documents. Additionally, if I were to expand my domain to include multilingual content, I would need to consider embedding models that support multiple languages effectively. In terms of accuracy on domain-specific text, if my corpus contains a lot of technical jargon or specific terminology, I might want to explore embedding models that are fine-tuned on similar domains to ensure better performance. 

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Are Professor Hannah's lectures well-received by students? | Yes, Professor Hannah's lectures have widely positive reception and found that her teaching style is engaging and informative. |
| 2 | How is Professor Erickson perceived by students? | Professor Erickson is generally perceived as a knowledgeable and approachable instructor who provides clear explanations and makes understanding the content digestible. |
| 3 | What can I expect from CMPU 145? | Expect the lectures from CMPU145 to be engaging and informative as Professor Gommerstadt is very passionate about what she teaches. |
| 4 | What do students say about the difficulty of CMPU 203 with Meireles? | Students generally find CMPU 203 with Meireles as it is a project-heavy course and ensuring that you frontload the work well early before a deadline is key to success. |
| 5 | Which of these courses has the most project-heavy workload? | CMPU203 is often described as having the most project-heavy workload among the listed courses. Though, other CS courses may also have significant project components, the comments do not explicitly state this. |

---

## Anticipated Challenges

1. Noisy or inconsistent documents: Given that the source documents are student-generated reviews and discussions, there is a risk of encountering noisy or inconsistent information. For example, some reviews may contain irrelevant details, personal biases, or conflicting opinions that could affect the quality of retrieved information and generated responses. To mitigate this risk, we can implement a filtering mechanism during the chunking stage to remove irrelevant content and ensure that only coherent and relevant chunks are stored in the vector database.

2. Inadequate source attribution: Since the system relies on retrieved chunks to generate responses, there is a risk that the model may not properly attribute sources or may generate responses that are not fully grounded in the retrieved context. This could lead to misinformation or insufficient responses. To address this challenge temporarily, we can fallback and tell the user that there is insufficient information to answer the question, and in the long term, we can implement a more robust source attribution mechanism that ensures all generated responses are properly grounded in the retrieved chunks and that sources are clearly cited in the response. Though, this will require a bit of advertising for people to submit more reviews and discussions to the corpus so that there is more information for the system to work with, which is a challenge in itself.
---

## Architecture

**refer to rag-pipeline-diagram.mmd for the architecture diagram written in mermaid.js.**

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
          For this milestone, Claude will be used for code generation and Copilot for code suggestions and completion. I will provide the Chunking Strategy section of this planning document, along with specific requirements for chunk size and overlap. I expect it to produce a function `chunk_text()` that takes in raw text and outputs a list of chunks based on the specified chunk size and overlap, while also being boundary-aware for the RMP reviews. To verify the output, the `chunk_text()` function will be tested on sample documents from my corpus, ensuring that the chunks are of the correct size, have the appropriate overlap, and that the RMP reviews are chunked according to their boundaries without splitting key information across chunks. A test file will be created first to validate the functionality of the chunking process, and I will check the output against expected results based on the input documents.

**Milestone 4 — Embedding and retrieval:**
          For this milestone, Claude will be used for code generation and Copilot for code suggestions and completion. I will provide the Embedding and Retrieval Strategy sections of this planning document, along with specific requirements for the embedding model and vector store. I expect it to produce functions, `embed_text()` that takes in text and returns its embedding using the specified model, and a function `retrieve_chunks()` that takes in a query and retrieves the top-k relevant chunks from the vector store based on cosine similarity. The output will be verified by testing the embedding function on sample documents and ensuring that the vectors are generated correctly. I will also test the retrieval function by querying the vector store with sample queries and checking that the retrieved chunks are relevant and accurate.

**Milestone 5 — Generation and interface:**
          For this milestone, Claude will be used for code generation and Copilot for code suggestions and completion. I will first sketch out the interface and lay out the details on how the LLM should answer a user's query, which will all be documented on a planning document similar to this one as there is no specific section for interface design in this document. Then, that document will be given as context to CLaude. I expect it to produce a function `generate_response()` that takes in a user query and the retrieved chunks as context, and generates a response using the specified LLM while adhering to the system prompt constraints. Additionally, I expect it to produce code for the Gradio interface that includes a search bar for user input, a response pane for displaying the model's answer with inline citations, and source cards for listing retrieved documents with metadata. The output will be verified by testing the generation function with sample queries and ensuring that the responses are accurate, properly grounded in the retrieved context, and include correct source attribution. The interface will be tested using playwright to simulate user interactions and verify that the components function as expected, allowing users to submit queries and view responses without any navigation issues.