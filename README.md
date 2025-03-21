# Chat with Multiple PDFs

This is a Streamlit application that allows you to chat with the content of multiple PDF documents. You can upload several PDF files, and the application will process them, allowing you to ask questions and receive answers based on the information within those documents.

## How I Did It...

This application was built using the following technologies and libraries:

- **Streamlit:** For creating the interactive web interface.
- **PyPDF2:** For reading and extracting text from PDF files.
- **Pandas:** For handling and exporting conversation history as a CSV file.
- **LangChain:** A framework for developing applications powered by language models. Specifically, it uses:
  - `RecursiveCharacterTextSplitter`: To break down the PDF text into manageable chunks.
  - `GoogleGenerativeAIEmbeddings`: To create vector embeddings of the text chunks using Google's AI models.
  - `FAISS (Facebook AI Similarity Search)`: For efficiently storing and searching the vector embeddings.
  - `ChatGoogleGenerativeAI`: To interact with Google's Gemini language model for generating answers.
  - `load_qa_chain`: To create a question-answering chain.
  - `PromptTemplate`: To define the prompt used for the language model.
- **Google Gemini:** As the underlying language model to understand your questions and generate answers based on the provided PDF content.

## Setup Instructions

Follow these steps to set up and run the application on your local machine:

1.  **Set up a Virtual Environment (Recommended):**
    It's good practice to create a virtual environment to isolate the project dependencies. Open your terminal or command prompt and navigate to the project directory. Then, run the following command to create a virtual environment:

    ```bash
    python -m venv venv
    ```

2.  **Activate the Virtual Environment:**

    - **On Windows:**
      ```bash
      venv\Scripts\activate
      ```
    - **On macOS and Linux:**
      ```bash
      source venv/bin/activate
      ```

3.  **Install Dependencies from `requirements.txt`:**
    The project dependencies are listed in the `requirements.txt` file. You can install them using pip. Make sure you are in the project directory and your virtual environment is activated. Run the following command:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**
    Once the dependencies are installed, you can run the application using Streamlit. In your terminal or command prompt (within the project directory and with the virtual environment activated), run the command:

    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser.

## How to Use the System (Step-by-Step)

Here's a detailed guide on how to use the Chat with Multiple PDFs application:

1.  **Get a Google API Key:**

    - The application uses Google's Gemini model, so you'll need a Google API key.
    - Go to [https://ai.google.dev/](https://ai.google.dev/) and follow the instructions to create a project and get an API key.

2.  **Enter Your Google API Key:**

    - In the left sidebar of the application, you will see a section labeled "Select the Model:". Below that, if you have selected "Google AI", you'll find a text input field that says "Enter your Google API Key:".
    - Paste your Google API key into this field.
    - **Important:** Your API key is sensitive information. Avoid sharing it publicly.

3.  **Upload Your PDF Files:**

    - In the left sidebar, below the "Menu:" section, you will find a file uploader labeled "Upload your PDF Files and Click on the Submit & Process Button".
    - Click on the "Browse files" button or drag and drop one or more PDF files into the uploader.
    - You can upload multiple PDF files at once.

4.  **Submit and Process:**

    - After selecting your PDF files, click the "Submit & Process" button located below the file uploader.
    - The application will then process the PDFs in the background. You will see a "Processing..." spinner, followed by a "Done" message once the processing is complete. This step might take a few moments depending on the size and number of your PDF files.

5.  **Ask a Question:**

    - In the main area of the application, you will see a text input field labeled "Ask a Question from the PDF Files".
    - Type your question related to the content of the uploaded PDF files into this field.

6.  **Get the Answer:**

    - Once you type your question and press Enter (or click outside the text input), the application will use the processed PDF data and the Google Gemini model to generate an answer.
    - The answer will be displayed in a chat-like interface below your question. Your question will appear in a user-style chat bubble, and the answer will appear in a bot-style chat bubble.

7.  **View Previous Conversations:**

    - Below the current question and answer, you will see a section labeled "Previous Conversations".
    - This section will display the history of your previous questions and the corresponding answers. Each previous question will be numbered (1, 2, 3, and so on).

8.  **Using the Sidebar Menu:**

    - **Reset Button:** Located in the top right of the "Menu:" section in the sidebar. Clicking this button will:
      - Clear the conversation history.
      - Clear the user question input field.
      - Reset the Google API key field.
      - Clear the uploaded PDF documents.
      - Remove the processed index (`faiss_index`) so that you can start fresh with new PDFs.
    - **Rerun Button:** Located in the top left of the "Menu:" section in the sidebar. Clicking this button will:
      - Clear the current question in the input field.
      - Remove the last question and answer pair from the conversation history.

9.  **Download Conversation History:**
    - At the bottom of the left sidebar, you will find a button labeled "Download conversation history as CSV file".
    - Clicking this button will download a CSV file containing the record of your conversation, including the questions, answers, the model used, timestamps, and the names of the PDF files you used.
    - You will also see a message in the main area indicating where to find the download button.

## Features

Here's a list of the key features of this application:

- **Chat with Multiple PDFs:** Ask questions and get answers based on the content of several PDF documents.
- **Google AI Integration:** Utilizes the powerful Google Gemini language model for understanding and answering questions.
- **Detailed Answers:** The system aims to provide detailed answers based on the context of your PDFs.
- **Clear Question/Answer Labeling:** The chat interface clearly distinguishes between your questions and the bot's answers.
- **Numbered Previous Conversations:** Your previous questions are numbered for easy tracking of the conversation flow.
- **Conversation History:** The application keeps a history of your interactions for reference.
- **Downloadable Conversation History:** You can download your entire conversation history as a CSV file for record-keeping.
- **Easy to Use Interface:** The Streamlit interface is intuitive and easy for beginners to understand.
- **Reset and Rerun Options:** Convenient buttons to reset the session or rerun the last query.

## Using Multiple PDFs

To use multiple PDF files:

1.  In the file uploader in the sidebar, you can select multiple PDF files at once by holding down the `Ctrl` key (or `Cmd` key on macOS) while clicking on the files, or by dragging a selection box around the files.
2.  Alternatively, you can upload files one by one. Each time you upload a new file, it will be added to the list of PDFs to be processed.
3.  Once you have uploaded all the desired PDF files, click the "Submit & Process" button. The application will process the content of all the uploaded PDFs, and you can then ask questions that might span across multiple documents.

## Contributor Details

[Md. Anwar Hossain]
[ranakrphone@gmail.com]
[GitHub Profile Link](https://github.com/ranak8811)
[LinkedIn Profile Link](https://www.linkedin.com/in/ranak8811/)

## Forking and Cloning the Repository

If you want to contribute to this project or run it locally, you can fork and clone the repository:

1.  **Fork the Repository:**

    - Go to the project's GitHub page.
    - Click on the "Fork" button in the top right corner of the page. This will create a copy of the repository in your GitHub account.

2.  **Clone the Repository:**

    - Open your terminal or command prompt.
    - Navigate to the directory where you want to clone the repository.
    - Run the following command, replacing `YOUR_GITHUB_USERNAME` with your actual GitHub username:

      ```bash
      git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_FORKED_REPOSITORY_NAME.git](https://www.google.com/search?q=https://github.com/YOUR_GITHUB_USERNAME/YOUR_FORKED_REPOSITORY_NAME.git)
      ```

    - This will download the project files to your local machine.

## Live Hosting

[Link to the live hosted version of the application (Will be added later)]

(You can replace the bracketed text above with the actual link to your live hosted application once it's deployed.)

```

```
