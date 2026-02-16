from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from retrieval import retrieve_relevant_chunks

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def assemble_context(chunks, max_chunks=3):
    # Sort by score (ascending = better for L2)
    sorted_chunks = sorted(chunks, key=lambda x: x[1])
    
    selected = sorted_chunks[:max_chunks]
    
    context_text = ""
    for i, (doc, score) in enumerate(selected):
        context_text += f"\n[Chunk {i+1} | Distance: {score}]\n"
        context_text += doc.page_content
        context_text += "\n\n"
    
    return context_text


def answer_query(query):
    retrieved = retrieve_relevant_chunks(query)

    if not retrieved:
        return {
            "answer": "Insufficient information in knowledge base.",
            "sources": []
        }

    context = assemble_context(retrieved)

    prompt = f"""
You are a technical assistant. 
Answer using ONLY the provided context.
You may summarize or combine information from multiple chunks.
If the context does not contain relevant information at all, say: "Insufficient information in knowledge base."
Do not use external knowledge.


Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    # Prepare source previews
    sources = []
    for doc, score in retrieved[:3]:
        sources.append({
            "distance": float(score),
            "page": doc.metadata.get("page"),
            "preview": doc.page_content[:200]
        })


    return {
        "answer": response.content,
        "sources": sources
    }



if __name__ == "__main__":
    question = "What operational risks were identified in the report?"
    answer = answer_query(question)
    print("\nFinal Answer:\n")
    print(answer)
