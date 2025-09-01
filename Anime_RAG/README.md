## Description of the document you selected

I selected the Wikipedia article about **anime**. This article describes the history, production, and cultural role of anime as a style of Japanese animation.

---

## 5 important questions and answers

### 1. Why do we need to chunk the text before storing it in the vector database?

**Answer:**
Chunking breaks long documents into smaller, manageable pieces that fit within the token limits of language models. It also helps preserve local context, making retrieval more precise. If you indexed entire documents as single chunks, the embeddings would be less focused, and retrieval would be less accurate. Overlapping chunks help ensure continuity across boundaries.

---

### 2. How is the retrieved text processed before being stored in the vector database?

**Answer:**
After the raw text is collected (in this case from the Anime Wikipedia page), it is split into smaller chunks using tools like `RecursiveCharacterTextSplitter`. These chunks are overlapping segments of a fixed size (e.g., 500 characters with 50 character overlap) to preserve context. Each chunk is then converted into a high-dimensional vector embedding using a Sentence-Transformers model (e.g., `all-distilroberta-v1`). These embeddings are indexed in FAISS for efficient similarity search.

---

### 3. How does the system find relevant pieces of information to answer a user’s question?

**Answer:**
When a user asks a question, the system embeds the question into the same vector space as the stored chunks. It then queries the FAISS vector store to find the top-k chunks most similar to the question vector. These retrieved chunks provide the contextual information the model needs to generate accurate and grounded answers.

---

### 4. How does the language model use the retrieved chunks to generate an answer?

**Answer:**
The retrieved chunks are combined into a context block and provided as part of the prompt to the language model (OpenAI’s `gpt-3.5-turbo`). The prompt instructs the model to answer the user’s question using **only** the provided context. This constrains the model’s generation to grounded information, improving accuracy and reducing hallucination compared to answering without retrieval.

---

### 5. What types of embeddings are used, and why are they important for this system?

**Answer:**
The system uses dense vector embeddings produced by a free Sentence-Transformers model (`all-distilroberta-v1`). These embeddings capture the semantic meaning of text chunks and questions in a numerical format, enabling FAISS to perform similarity searches based on meaning, not just keywords. This semantic search is essential to finding the most relevant context for the user’s queries.

---

## 3 Questions and Answer Quality

**Your question:** Who draws anime?  
**Answer:** Anime is typically drawn by a team of animators, which can include key animators, in-between animators, background artists, and other specialists in the animation industry.

**Your question:** What is anime?  
**Answer:** Anime is hand-drawn and computer-generated animation originating from Japan. Outside Japan and in English, anime refers specifically to animation produced in Japan. In Japanese, anime describes all animated works, regardless of style or origin.

**Your question:** Are anime cartoons?  
**Answer:** Yes, anime can be considered a form of cartoon as it is a type of animated work.

---

## Chunk Size & Overlap Experiments

To test how chunk size and overlap affect response quality, I asked the model to "Explain the history of anime."

- **Chunk size = 1000, overlap = 500**  
  *Answer:* The model produced a long, detailed description including the origins of anime in early 20th-century Japan, post-WWII influences, and the rise of modern studios.  

- **Chunk size = 500, overlap = 50 (default)**  
  *Answer:* The response was solid, covering major points such as Japanese cultural influence and anime’s spread worldwide, but less detailed than the larger chunk size.  

- **Chunk size = 100, overlap = 50**  
  *Answer:* The answer was shorter and less complete, omitting important details about history and focusing only on a couple of facts.  

**Conclusion:** Larger chunks with more overlap generally provide richer answers because they preserve more context. Smaller chunks increase granularity but risk losing continuity.

