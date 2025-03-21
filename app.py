import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import base64
import os

# Update imports for LangChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from datetime import datetime

# Function to extract text from PDF documents
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split the text into smaller chunks for processing
def get_text_chunks(text, model_name):
    if model_name == "Google AI":
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store from the text chunks using FAISS
def get_vector_store(text_chunks, model_name, api_key=None):
    if model_name == "Google AI":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# Function to create a conversational chain using Google Gemini
def get_conversational_chain(model_name, vectorstore=None, api_key=None):
    if model_name == "Google AI":
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer.

        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=api_key)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain

# Function to handle user input and generate responses
def user_input(user_question, model_name, api_key, pdf_docs):
    # Check if API key and PDF files are provided
    if api_key is None or pdf_docs is None:
        st.warning("Please upload PDF files and provide API key before processing.")
        return

    # Create the vector store if it doesn't exist
    if "faiss_index" not in os.listdir():
        with st.spinner("Processing PDFs and creating index..."):
            text_chunks = get_text_chunks(get_pdf_text(pdf_docs), model_name)
            get_vector_store(text_chunks, model_name, api_key)
        st.success("PDFs processed and index created.")

    user_question_output = ""
    response_output = ""
    # Process the question using the selected model
    if model_name == "Google AI":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain("Google AI", vectorstore=new_db, api_key=api_key)
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        user_question_output = user_question
        response_output = response['output_text']
        pdf_names = [pdf.name for pdf in pdf_docs] if pdf_docs else []
        # Append the current question and answer to the conversation history
        st.session_state.conversation_history.append(("Question", user_question_output, model_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ", ".join(pdf_names)))
        st.session_state.conversation_history.append(("Answer", response_output, model_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ", ".join(pdf_names)))

    # Display the current question and answer
    st.markdown(
        f"""
        <style>
            .chat-message {{
                padding: 1.5rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                display: flex;
            }}
            .chat-message.user {{
                background-color: #2b313e;
            }}
            .chat-message.bot {{
                background-color: #475063;
            }}
            .chat-message .avatar {{
                width: 20%;
            }}
            .chat-message .avatar img {{
                max-width: 78px;
                max-height: 78px;
                border-radius: 50%;
                object-fit: cover;
            }}
            .chat-message .message {{
                width: 80%;
                padding: 0 1.5rem;
                color: #fff;
            }}
            .chat-message .info {{
                font-size: 0.8rem;
                margin-top: 0.5rem;
                color: #ccc;
            }}
            .message-label {{
                font-weight: bold;
                margin-bottom: 0.2rem;
                display: block;
            }}
        </style>
        <div class="chat-message user">
            <div class="avatar">
                <img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png">
            </div>
            <div class="message">
                <span class="message-label">Question:</span>
                {user_question_output}
            </div>
        </div>
        <div class="chat-message bot">
            <div class="avatar">
                <img src="https://i.ibb.co/wNmYHsx/langchain-logo.webp" >
            </div>
            <div class="message">
                <span class="message-label">Answer:</span>
                {response_output}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display a separator between the current and previous conversations
    st.markdown("---")
    st.subheader("Previous Conversations")

    # Display previous conversations with numbering
    question_number = 1
    for i in range(0, len(st.session_state.conversation_history) - 2, 2):
        if i < len(st.session_state.conversation_history) - 1:
            question_label, question_message, _, _, _ = st.session_state.conversation_history[i]
            answer_label, answer_message, _, _, _ = st.session_state.conversation_history[i+1]
            if question_label == "Question" and answer_label == "Answer":
                st.markdown(
                    f"""
                    <div class="chat-message user">
                        <div class="avatar">
                            <img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png">
                        </div>
                        <div class="message">
                            <span class="message-label">Question {question_number}:</span>
                            {question_message}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div class="chat-message bot">
                        <div class="avatar">
                            <img src="https://i.ibb.co/wNmYHsx/langchain-logo.webp" >
                        </div>
                        <div class="message">
                            <span class="message-label">Answer:</span>
                            {answer_message}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                question_number += 1

    # Logic for downloading the conversation history
    if len(st.session_state.conversation_history) > 0:
        df = pd.DataFrame(st.session_state.conversation_history, columns=["Label", "Message", "Model", "Timestamp", "PDF Name"])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # Convert to base64
        href = f'<a href="data:file/csv;base64,{b64}" download="conversation_history.csv"><button>Download conversation history as CSV file</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.markdown("To download the conversation, click the Download button on the left side at the bottom of the conversation.")
    st.snow()

# Main function to set up the Streamlit application
def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.header("Chat with multiple PDFs (v1) :books:")

    # Initialize conversation history in session state if it doesn't exist
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    # Links to social media profiles
    linkedin_profile_link = "https://www.linkedin.com/in/ranak8811/"
    kaggle_profile_link = "https://www.kaggle.com/ranak8811"
    github_profile_link = "https://github.com/ranak8811"

    # Display social media links in the sidebar
    st.sidebar.markdown(
        f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({linkedin_profile_link}) "
        f"[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)]({kaggle_profile_link}) "
        f"[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({github_profile_link})"
    )

    # Sidebar for model selection and API key input
    model_name = st.sidebar.radio("Select the Model:", ( "Google AI"))
    api_key = None

    if model_name == "Google AI":
        api_key = st.sidebar.text_input("Enter your Google API Key:")
        st.sidebar.markdown("Click [here](https://ai.google.dev/) to get an API key.")

        if not api_key:
            st.sidebar.warning("Please enter your Google API Key to proceed.")
            return

    # Sidebar menu for reset and rerun actions
    with st.sidebar:
        st.title("Menu:")

        col1, col2 = st.columns(2)

        reset_button = col2.button("Reset")
        clear_button = col1.button("Rerun")

        # Reset button functionality
        if reset_button:
            st.session_state.conversation_history = [] # Clear conversation history
            st.session_state.user_question = None  # Clear user question input
            api_key = None  # Reset Google API key
            st.session_state.pdf_docs = None  # Reset PDF document
            if "faiss_index" in os.listdir():
                import shutil
                shutil.rmtree("faiss_index")

        # Rerun button functionality
        else:
            if clear_button:
                st.session_state.user_question = ""
                if len(st.session_state.conversation_history) > 0:
                    st.session_state.conversation_history.pop()
                    if len(st.session_state.conversation_history) > 0:
                        st.session_state.conversation_history.pop()

        # File uploader for PDF files
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True, key="pdf_uploader")
        # Button to trigger PDF processing
        if st.button("Submit & Process"):
            if pdf_docs:
                st.session_state.pdf_docs = pdf_docs # Store uploaded PDFs in session state
                if "faiss_index" in os.listdir():
                    import shutil
                    shutil.rmtree("faiss_index")
                with st.spinner("Processing..."):
                    # Text chunks and vector store creation moved inside user_input to handle API key dependency
                    st.success("Done")
            else:
                st.warning("Please upload PDF files before processing.")
        # Initialize pdf_docs in session state if not already present
        if 'pdf_docs' not in st.session_state:
            st.session_state.pdf_docs = None

    # Text input for the user's question
    user_question = st.text_input("Ask a Question from the PDF Files", key="user_question") # Added key for state management

    # Process user question if it's provided and PDF files are uploaded
    if user_question and st.session_state.pdf_docs:
        user_input(user_question, model_name, api_key, st.session_state.pdf_docs)
    elif user_question and not st.session_state.pdf_docs:
        st.warning("Please upload PDF files to ask questions.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
