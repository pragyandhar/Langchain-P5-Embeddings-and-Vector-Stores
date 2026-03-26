from loader import load_file
from splitter import splitter
from chain import build_chain
from vectorstore import build_vectorstore, build_retriever

def main():
    print("\n--- Chat With Your Document ---\n")

    file_path = str(input("Enter the path to your document (PDF or TXT): ")).strip()

    # Load and split the document
    print("\nLoading and splitting document...")
    documents = load_file(file_path)
    chunks = splitter(documents)

    # Build vector store and retriever
    vectorstore = build_vectorstore(chunks)
    retriever = build_retriever(vectorstore)

    # Build the question-answering chain
    chain = build_chain(retriever)
    print("\nYou can now ask questions about the document. Type 'exit' to quit.")
    while True:
        question = input("\nYour question: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break

        if not question:
            continue

        # Show which chunks were retrieved
        retrieved_chunks = retriever.invoke(question)
        print(f"\n[Retrieved {len(retrieved_chunks)} chunks]")
        for i, chunk in enumerate(retrieved_chunks):
            print(f"  Chunk {i+1}: {chunk.page_content[:80]}...")

        answer = chain.invoke({"question": question})
        print(f"\nAssistant: {answer}")        

if __name__ == "__main__":
    main()
