# The Unofficial Guide (vccs-inquiries) — Project 1

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     This Unofficial Guide will focus on student-generated knowledge about Vassar CS courses and professors. This knowledge is valuable because official course listings describe content but do not describe teaching style, grading philosophy, workload distribution, or which course combinations are dangerous. This system fills that gap.
     
---


## Sample Interaction

Input Field:
A text box with the placeholder: "Ask anything about Vassar CS courses and professors..."
Accepts free-form natural language queries about Vassar CS courses, professors, workload, or course recommendations
Supports Enter/Return key submission or clicking the submit button (→)

Output Display:
A chat interface showing conversation history
Each assistant response includes inline source citations in the format [Source N]
At the end of each response, a "Sources:" section lists all clickable cited sources 

Sample Query: 
How is Professor Erickson perceived by students?


Professor Erickson is perceived by students as highly knowledgeable and able to manage the classroom well [Source 1]. Students find his hands-on labs to be engaging and challenging [Source 1], and his lectures to be effective and engaging [Source 2]. He is also appreciated for simplifying complex material, making it more digestible [Source 2]. Additionally, students appreciate his availability to answer questions after class [Source 2]. Overall, students seem to have a positive opinion of Professor Erickson, with one student stating they would definitely take another class with him [Source 1].

Sources:

https://www.ratemyprofessors.com/professor/3061766
https://www.ratemyprofessors.com/professor/3061766


     
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

Why these choices fit your documents: Given that these documents consist of student reviews and discussions, which can vary in length and structure, we apply recursive character splitting to preserve coherent units of information while keeping chunks manageable for retrieval and generation. The splitter uses a priority-ordered cascade of separators, paragraph breaks, line breaks, sentence-ending punctuation, then spaces, and falling back to finer splits only when a chunk still exceeds the size limit. Chunk size is set to [your CHUNK_SIZE] (256 tokens) tokens and overlap to [your CHUNK_OVERLAP] (50) tokens, measured using the all-MiniLM-L6-v2 tokenizer. This approach approximates boundary-aware chunking heuristically: it avoids splitting mid-sentence or mid-paragraph whenever possible. The overlap helps preserve context that might otherwise be severed at chunk edges, which is particularly relevant for reviews and discussions where sentiment or reasoning can span multiple sentences.

Final chunk count: 43 chunks
 
Sample Chunks: 

Document name: RMP_Rui_Meireles.pdf
{
    "chunk_id": "97586eb2-7293-467e-ab88-90cdf06f5938",
    "text": "CMPU-203 - Comment #5: He is always readily available when we needed help with errors in our\ncode or just didn't understand how to do something. He is super enthusiastic about our ideas and\nalways knows how to improve upon them. He's very encouraging and I would love to have him as a\nprofessor again!",
    "metadata": {
      "source": "rmp",
      "professor_name": "Rui Meireles",
      "raw_url": "https://www.ratemyprofessors.com/professor/2308938",
      "course_code": "CMPU-203",
      "approximate_year": 2023,
      "chunk_index": 0
    }
  },

Document name: Misc News Review on CMPU145.pdf
  {
    "chunk_id": "6fed0ea2-64f3-4d57-be34-7423c06e4bf3",
    "text": "I chose my seat, a chair with a nice view of Ben Franklin’s behind, as a silent wish for a lucky\nsemester. The class occurred on Tuesdays and Thursdays at 10:30 a.m. (with a lab on Thursday\nfrom 6 to 8 p.m.). Entitled CMPU 145: “Foundations of Computer Science” and taught by Professor\nof Computer Science Anna Gommerstadt, the course is a requirement for all Computer Science\nmajors and correlates. And while it is impossible to know how much I would have enjoyed the class\nhad I chosen it without its use for my major, in this universe, I can affirm it was a heck of a good\ntime.\nWhat exactly did I learn? What is meant by the vague and all-encompassing word “Foundations”?\nWell, per my trusty syllabus, “This course introduces the theoretical, structural, and algorithmic\nfoundations of computer science.” In essence, we learned the basics of functional programming\nthrough a language called OCaml. This contrasts with other programming paradigms, like\nprocedural languages or object-oriented languages. Functional programming utilizes functions to\nsolve the problems we face when computing. In both lecture and labs, we developed our skills",
    "metadata": {
      "source": "miscellany",
      "professor_name": "Anna Gommerstadt",
      "course_code": "CMPU-145",
      "raw_url": "https://miscellanynews.org/2023/11/29/features/student-reviews-foundations-of-computer-science/",
      "chunk_index": 0
    }
  },

  Document name: Misc News Review on CMPU145.pdf

  {
    "chunk_id": "62406b40-a6be-4a67-81b3-010ee0b9f844",
    "text": "through a language called OCaml. This contrasts with other programming paradigms, like\nprocedural languages or object-oriented languages. Functional programming utilizes functions to\nsolve the problems we face when computing. In both lecture and labs, we developed our skills\nworking with OCaml, proofs, recursive data structures, sets, logic, etc. to assist with higher-level\ncomputer science coursework.\nI was initially skeptical—from the feedback of others in the department—about how I would fare in\nour assignments, but I can pleasantly say they are jolly and understandable. Professor\nGommerstadt’s lectures are engaging and spirited with the energy one needs to understand the\nintersections and unions of sets. Although one is often searching hard for dry-erase markers in\nSanders Physics 105, when all is said and done, the material is interesting and relevant. Even the\nproofs were not too difficult, just “foundation”-al!\nWhile I suffered from a mid-semester concussion, Professor Gommerstadt was accommodating,\nand my enjoyment of the lectures kept me on track with the course’s workload. Her love of sloths\nand use of Vim, a text editor, for live lecture coding was a cozy way to pass autumn by. In the labs",
    "metadata": {
      "source": "miscellany",
      "professor_name": "Anna Gommerstadt",
      "course_code": "CMPU-145",
      "raw_url": "https://miscellanynews.org/2023/11/29/features/student-reviews-foundations-of-computer-science/",
      "chunk_index": 1
    }
  },

  Document name: Misc News Review on CMPU145.pdf

  {
    "chunk_id": "dbd8d4c8-5416-46fa-9176-27648c86a60d",
    "text": "and my enjoyment of the lectures kept me on track with the course’s workload. Her love of sloths\nand use of Vim, a text editor, for live lecture coding was a cozy way to pass autumn by. In the labs\non Thursday nights, the questions were more puzzle than problem, and our coaches kept us on our\ntoes!\nI would recommend anyone take this section, even if they have only the slightest interest in\ncomputers and their functioning. It is truly worth a stop on the many twists and turns of a Vassar\neducation.",
    "metadata": {
      "source": "miscellany",
      "professor_name": "Anna Gommerstadt",
      "course_code": "CMPU-145",
      "raw_url": "https://miscellanynews.org/2023/11/29/features/student-reviews-foundations-of-computer-science/",
      "chunk_index": 2
    }
  },

    Document name: CS Class Ordering Thread.pdf

  {
    "chunk_id": "d79f1d1b-b152-4630-95e7-8d75c8c8c012",
    "text": "Just for fun, here is a mock schedule:\n1Fall: 101\n1Spring: 102 / 145\n2F: 203 / 224\n2S: 241 / 245\n3F: 240 / 366\n4S: 334 / 365\n4F: 331\nHonestly though, everything between 2F and 4S here is pretty much just what you want. I picked\nprobably the most common courses/ordering to take but there's a good amount of flexibility. You\ncan throw the required math class in whenever you feel comfortable. In general, the ones set in\nstone here are doing 101/102/145 first and doing 331/334 close to last.\nI think it's important to emphasize that there is no real \"recommended sequence\". Beyond the\nrequired courses, your advisor would harp on taking the classes you are interested in. I think it's\npretty uncommon for two kids to graduate with the exact same CS courses under their belts.",
    "metadata": {
      "source": "reddit",
      "raw_url": "https://www.reddit.com/r/vassar/comments/98tpux/computer_science_four_year_course_plan/",
      "chunk_index": 0
    }
  },


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
{REFUSAL_STRING} ("I don't have enough student-sourced information to answer that question reliably.")

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
The retrieval stage disproportionately surfaced negative chunks because the embedding space for short, emotionally charged text (e.g., "Really really bad", "Awful") clusters more tightly around negative sentiment queries. The few neutral or constructive CMPU240 comments that existed in the corpus were embedded in longer Reddit chunks where the course name appeared with less semantic weight, which caused  them to rank below the blunter RMP reviews. The root cause is sparse data, but the failure occurs at retrieval: cosine similarity favored high-signal negative chunks over lower-density balanced ones.

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

---


## Retrieval Tests


Retrieval Test Examples:

Example 1:
'Are Professor Anna's lectures for CMPU145 well-received by students?'
  [1] (dist=0.3654) [Anna Gommerstadt] CMPU-145 - Comment #1: Anna's teaching/lecture style is effective and fun. Enoug...
  [2] (dist=0.4431) [Anna Gommerstadt] CMPU-145- Comment #5: Had her for both 102 and 145, and she gives very engaging ...
  [3] (dist=0.4619) [Jacob Erickson] CMPU-241 - Comment #3: Effective, engaging lectures and available to answer ques...
  [4] (dist=0.5087) [Anna Gommerstadt] and my enjoyment of the lectures kept me on track with the course’s workload. He...
  [5] (dist=0.5165) [Rui Meireles] CMPU-203 - Comment #2: Rui comes off as shy but he is very sweet and helpful. Le...


Chunks 1, 2, and 4 are directly sourced from Anna Gommerstadt's RMP reviews and the Miscellany article have both explicitly mentioned her lecture style for CMPU-145, which maps tightly to the query. Chunk 3 for example, (Erickson) surfaced likely because it shares the word "lectures" and similar positive phrasing, making it a false positive at the embedding level. The retrieval is largely on-target, with two off-topic results out of five.

Example 2:

'How is Professor Erickson perceived by students?'
  [1] (dist=0.2799) [Jacob Erickson] CMPU-101- Comment #4: Professor Erickson is highly knowledgeable and manages the...
  [2] (dist=0.5005) [Jacob Erickson] CMPU-241 - Comment #3: Effective, engaging lectures and available to answer ques...
  [3] (dist=0.5071) [Peter Lemieszewski] CMPU-102 - Comment #2 : Peter is an amazing human being. He always came to class...
  [4] (dist=0.5147) [Peter Lemieszewski] CMPU-102 - Comment #3 : Peter is an amazing guy. He is very hard working and ver...
  [5] (dist=0.5189) [Peter Lemieszewski] CMPU102 - Comment #7 : Pete is a super nice and accessible professor. But he is ...

Chunks 1 and 2 are directly from Erickson's RMP reviews and rank closest by cosine distance (0.28 and 0.50), confirming the embedding model correctly prioritized the named professor. Chunks 3, 4, and 5 are all Peter Lemieszewski reviews, which were retrieved likely because they share structural and tonal similarity to Erickson reviews (short, professor-focused, positive sentiment). This shows the model retrieved by semantic pattern as much as by named entity, which is a limitation worth noting.


Example 3:
What do students say about the difficulty of CMPU 203 with Meireles?
  [1] (dist=0.5931) [Peter Lemieszewski] CMPU-102 - Comment #9 : Not helpful at all...
  [2] (dist=0.5937) [Rui Meireles] CMPU-203 - Comment #4: 10/10. A work-heavy course, but Meireles is an excellent ...
  [3] (dist=0.6522) [Peter Lemieszewski] CMPU-102 - Comment #5: Very helpful outside of class but be prepared to do extra...
  [4] (dist=0.6589) [Peter Lemieszewski] CMPU102 - Comment #6: Very little homework. Easy grader. Absolutely useless lect...
  [5] (dist=0.6649) [Jonathan Gordon] CMPU-240 - Comment #2: Really really bad. I don't understand why some people dec...


Chunk 2 is the most relevant, directly referencing Meireles and CMPU-203's workload. However, chunks 1, 3, 4, and 5 are all Lemieszewski or Gordon reviews with no connection to the query. Additionally, the high cosine distances (0.59-0.66) confirm weak retrieval overall. This suggests the corpus has too few CMPU-203 chunks for the retrieval stage to consistently surface relevant results for this query.


     
     
---