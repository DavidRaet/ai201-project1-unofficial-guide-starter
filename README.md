# The Unofficial Guide (vccs-inquiries) — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     This Unofficial Guide will focus on student-generated knowledge about Vassar CS courses and professors. This knowledge is valuable because official course listings describe content but do not describe teaching style, grading philosophy, workload distribution, or which course combinations are dangerous. This system fills that gap.
     
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

Chunk size: 256 tokens 

Overlap: 50 tokens 

Why these choices fit your documents: Given that these documents consist of student reviews and discussions, which can vary in length and structure, a boundary-aware fixed-size chunking strategy allows us to preserve coherent units of information while ensuring that chunks are manageable for retrieval and generation. For RMP Reviews, it's document is first split into review boundaries using a consistent delimiter,"-0", preserving each review as a single chunk. For the Reddit thread comments and the Miscellany News article, we will also apply fixed-size chunking with a chunk size of 300 tokens and an overlap of 50 tokens but omitting the delimiters since these documents only contain a single coherent section. This approach allows us to capture the full sentiment and details of each review or discussion while still ensuring that chunks are manageable for retrieval and generation. The overlap of 50 tokens helps to mitigate the risk of splitting key information across chunk boundaries, which can be particularly important for reviews that may contain important context or sentiment that spans multiple sentences.

Final chunk count: 43 chunks
 
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers

**Production tradeoff reflection:** Using `all-MiniLM-L6-v2` works just fine as it's a general purpose embedding model for simplicity and relatively short context. So, if I'm working on a review-heavy corpus that won't need too much context, this model works just fine. However, if I were to start embedding more document-heavy material like elaborate blogs, articles, etc. I should consider using models that are specifically designed for longer contexts, such as `jina-embeddings-v2-base-en` (Jina) or `nomic-embed-text-v1.5` (Nomic AI), which can capture more nuanced information from longer documents. Additionally, if I were to expand my domain to include multilingual content, I would need to consider embedding models that support multiple languages effectively. In terms of accuracy on domain-specific text, if my corpus contains a lot of technical jargon or specific terminology, I might want to explore embedding models that are fine-tuned on similar domains to ensure better performance. 


---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**  

You are an assistant that helps Vassar College CS students learn about courses and professors.

STRICT GROUNDING RULE: Answer ONLY using the numbered sources provided in the user message. Do NOT use any knowledge from your training data about courses, professors, workloads, or Vassar College. If a fact is not stated in the provided sources, do not include it in your answer.

CITATION RULE: Every claim you make must be cited inline using [Source N] notation, where N is the number of the source it comes from.

SOURCE LIST RULE: At the end of every response, include a "Sources:" section that lists each source you cited, with its URL.

REFUSAL RULE: If the provided sources do not contain enough information to answer the question, respond with EXACTLY the following sentence and nothing else:
{REFUSAL_STRING}

**How source attribution is surfaced in the response:**
e.g
Sources:
[Source 1]
[Source 2]
[Source 3]
[Source 4]
[Source 5]

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Are Professor Anna's lectures well-received by students? | Yes, Professor Hannah's lectures have widely positive reception and found that her teaching style is engaging and informative. |Yes, Professor Anna's lectures are well-received by students [Source 1], with one student commenting that her teaching/lecture style is "effective and fun" [Source 1]. Another student noted that she is a "really engaging lecturer" [Source 4] and that her enthusiasm for the material makes the lectures enjoyable [Source 4]. Additionally, a student mentioned that their enjoyment of the lectures helped them stay on track with the course's workload [Source 5], and described the lectures as a "cozy way to pass autumn by" [Source 5]. |Relevant |Accurate |
| 2 | How is Professor Erickson perceived by students? | Professor Erickson is generally perceived as a knowledgeable and approachable instructor who provides clear explanations and makes understanding the content digestible. | Professor Erickson is perceived by students as highly knowledgeable and able to manage the classroom well [Source 1]. Students find his hands-on labs to be engaging and challenging [Source 1], and his lectures to be effective and engaging [Source 2]. He is also seen as available to answer questions after class [Source 2] and able to simplify complex material [Source 2]. Overall, students seem to have a positive opinion of Professor Erickson, with one student stating they would definitely take another class with him [Source 1]. | Relevant | Accurate |
| 3 | What can I expect from CMPU 145? | Expect the lectures from CMPU145 to be engaging and informative as Professor Gommerstadt is very passionate about what she teaches. | According to the sources, Anna Gommerstadt teaches CMPU-145 and gives "very engaging lectures" [Source 4]. She is also described as "very personable and passionate about what she's teaching" [Source 4]. |Relevant | Accurate |
| 4 | What do students say about the difficulty of CMPU 203 with Meireles? | Students generally find CMPU 203 with Meireles as it is a project-heavy course and ensuring that you frontload the work well early before a deadline is key to success. | Students describe CMPU-203 with Meireles as a "work-heavy course" [Source 2]. However, they also mention that the course itself is "really fun" [Source 2] and that Meireles is an "excellent lecturer" [Source 2]. To manage the workload, students are advised to "front-load your work to avoid a crunch in the back half" [Source 2]. | Relevant | Accurate |
| 5 | What are student's opinions on CMPU240? | CMPU240 is a difficult but rewarding class. The class is highly theoretical but will build a solid foundation in problem-solving and intuitive abilities. Though this class has received heavy criticism due to the student's impressions of the professors. | Students have expressed strongly negative opinions about CMPU-240, with one comment stating that the teacher is "Really really bad" and "Extremely dull and uninspiring" [Source 3], and another comment simply stating that the class and professor are "Awful" [Source 5]. | Partially Relevant | Partially Accurate |


**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What are student's opinions on CMPU240?

**What the system returned:**

Students have expressed strongly negative opinions about CMPU-240, with one comment stating that the teacher is "Really really bad" and "Extremely dull and uninspiring" [Source 3], and another comment simply stating that the class and professor are "Awful" [Source 5]. 


**Root cause (tied to a specific pipeline stage):**
Very likely the ingestion stage. There was a scarcity in the amount of sources that describe CMPU240 in a more rational viewpoint.  

**What you would change to fix it:**
If time allowed, I would try to personally survey more students who have took CMPU240, gather their opinions on the class in more detail rather than vague "oh this class is terrible" kind of phrases.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec has helped me ideate on the minute details on how I would implement each stage of the RAG Pipeline. For example, what kind of chunking strategy would I use given the documents I'm ingesting or the tradeoffs of using one embedding model. Essentially, the spec has given me a foundation on where to work with.
**One way your implementation diverged from the spec, and why:**
Once implementation set in, I initially had a Boundary Aware Fixed-Sized Chunking strategy but because I eventually realized that the documents that I was extracting had all inconsistent and informal formats, we could not rely on this approach to safely predict boundaries. Therefore, the Recursive Splitting approach was used in place to handle the documents, in many cases sentiments and reviews.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I gave Claude, in plan mode, my Embedding and Retrieval approach from the planning.md document and thoroughly read through how it plans to implement the methods for consistency. 
- *What it produced:* It produced all of the tests that match the expected behaviors of the embedding and retrieval process.  
- *What I changed or overrode:* Claude provided a smoke test in main which included a query and returned the results of entering that query and revealing the chunks that were retrieved based on the similarity and connection to it. So, I replaced the initial query that Claude wrote with other queries to see the different results for myself. 

**Instance 2**

- *What I gave the AI:* During the interface prototyping process, I gave Claude a basic prompt on how the interface should look like including the color scheme and layout.
- *What it produced:* Claude produced a interface that somewhat matched the vision for how the prototype should look.
- *What I changed or overrode:* Some of the colors that Claude included did not match the colors I was expecting in the prototype so I trivially changed the specific colors. 
