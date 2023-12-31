import streamlit as st
import fitz  # PyMuPDF
import openai
import os

# Set the theme for your Streamlit app
st.set_page_config(layout='wide', page_title='Maternal Health Legislation App')



# Load the OpenAI API key from secrets.toml
openai_api_key = st.secrets["openai"]["api_key"]



# Center the Streamlit app content
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

# Function to ask a question using OpenAI's API
def ask_openai_question(text, question, openai_api_key):
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Document: {text}\n\nQuestion: {question}\nAnswer:",
        temperature=0,
        max_tokens=100,
        stop=["\n"]
    )
    answer = response.choices[0].text.strip()
    return answer

# Streamlit app
def main():
    st.title("Black Maternal Health Legislation - Question & Answering")

    # Specify the path to the maternalhealth.pdf document
    pdf_path = "MomnibusIntro.pdf"
    pdf_full = "https://www.congress.gov/118/bills/hr3305/BILLS-118hr3305ih.pdf"

    extracted_text = extract_text_from_pdf(pdf_path)

    # Display a header image
    header_image = st.image(
        "https://github.com/AndreaHobby/MaternalHealthLegislationApp/raw/main/MaternalHealthHeader.jpg",
        use_column_width=True)

    # About this App section
    st.markdown("## About this App:")
    st.markdown(
        "This app uses text from the Black Maternal Health Momnibus Act of 2023 which is publicly available information."
        " The full document is linked at the bottom of this page."
        " This is app only analyzes the first 8 pages of the act as this was done for a learning exercise.")
    st.markdown(
        "This app was developed by Andrea Hobby. [LinkedIn Profile](https://www.linkedin.com/in/andreahobby/)"
    )

    # Instructions section
    st.markdown("## Instructions:")
    st.markdown("1. Click the 'Show Extracted Text' button to reveal the extracted text from the legislation document.(Optional)")
    st.markdown("2. Enter your question in the text input field.")
    st.markdown("3. Click the 'Ask' button to get an answer based on the extracted text.")

    # Create a button to show/hide extracted text
    show_text = st.button("Show Extracted Text")
    if show_text:
        st.header("Extracted Text from Maternal Health Legislation")
        st.text(extracted_text)

    st.markdown("#### Have a question?")
    question = st.text_input("Enter your question:")

    if st.button("Ask"):
        if question:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            answer = ask_openai_question(extracted_text, question, openai_api_key)
            st.header("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")




    # Reference section with a clickable link to the PDF
    st.markdown("#### Legislation and Source Code")
    st.markdown(f"[Download the Full Legislation Document here]({pdf_full})")
    st.markdown(
        "You can find the source code for this app on GitHub: [Link to GitHub Repository](https://github.com/AndreaHobby/MaternalHealthLegislationApp)"
    )

    # Disclaimer section
    st.markdown("#### Disclaimer:")
    st.markdown(
        "This app utilizes a language model developed by OpenAI (GPT-3.5 Turbo) to provide answers based on the extracted text from the Black Maternal Health Momnibus Act of 2023. "
        "It is important to note the following:"
    )
    st.markdown(
        "- This app provides answers generated by artificial intelligence, and the responses are based on patterns and information present in the provided text. It does not offer legal advice or replace expert consultation."
    )
    st.markdown(
        "- The language model's responses may not always be up-to-date or completely accurate, and they may vary over time as the model evolves."
    )
    st.markdown(
        "- For the most accurate and current information on maternal health legislation, consult relevant government officials, policy experts, and authoritative sources."
    )


if __name__ == "__main__":
    main()

# Set Your API Key as an Environment Variable:
# In your terminal, set your OpenAI API key as an environment variable.
# You can do this by running the following command (replace YOUR_API_KEY_HERE with your actual OpenAI API key):
# export OPENAI_API_KEY=YOUR_API_KEY_HERE
# Ensure that you don't include quotes around the API key in the environment variable.
# After this, you can run the app in the terminal with streamlit run App.py
