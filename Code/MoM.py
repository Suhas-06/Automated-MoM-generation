from langchain_ibm import WatsonxLLM
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from langchain import PromptTemplate
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
import os
import sys
from langchain import LLMChain

# Initialize Watsonx LLM model
def initialize_watsonx_llm():
    api_key = "YOUR API KEY"
    project_id = "YOUR PROJECT ID"
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": api_key
    }
    # model_id = ModelTypes.GRANITE_13B_CHAT_V2
    model_id = "meta-llama/llama-3-70b-instruct"
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 1500,
        GenParams.REPETITION_PENALTY: 1
    }
    return WatsonxLLM(
        model_id=model_id,
        url=credentials.get("url"),
        apikey=credentials.get("apikey"),
        project_id=project_id,
        params=parameters
    )

prompt_template = """system

    You always answer the questions with markdown formatting using GitHub syntax. The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes. You must omit that you answer the questions with markdown.
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. 
    Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
    Can you generate a summary with their respective timestamps using the given transcription
    transcription : "{transcript}"
    """
que = """
        Can you give me Minutes of the meeting document based on the given transcriptions(The minutes of the meeting document must include date,attendees,summary,keypoints,actionitems with action owners,next steps)? also add timestamps to the respective keypoints.
        Sub key points should only be included when necessary.
        Action items should start with the description of the task, followed by the owner's name.
        The minutes should follow the format below:
        # Minutes of the Meeting

        Date: [Meeting Date]

        Attendees: [List of Attendees]

        ---

        Summary
        [summary of the meeting]

        ---

        Key Points
        * [Key point 1] (from Timestamp - to Timestamp)
        * [Key point 2] (from Timestamp - to Timestamp)
            + [Sub key point if any]
            + [Sub key point if any]
            ...
        * [Key point 3] (from Timestamp - to Timestamp)
            + [Sub key point if any]
        ...

        ---

        Action Items
        1. [Action Item 1]([Timestamp]) - [Action Owner 1]
        2. [Action Item 2]([Timestamp]) - [Action Owner 2]
        3. [Action Item 3]([Timestamp]) - [Action Owner 3]
        ...

        ---

        Next Steps
        1. [Next Step 1]
        2. [Next Step 2]
        3. [Next Step 3]
        ...
        """
question = f"Question: {que}"
formatted_question = f"""user{question}assistant"""
prompt=f"{prompt_template}{formatted_question}"

watsonx_llm = initialize_watsonx_llm()
# file_path = "C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary\\preprocessed.txt"
file_path = sys.argv[1]
with open(file_path, 'r', encoding='utf-8') as file:
    transcript_data = file.read()
cleaned_transcript = transcript_data.replace('\n', ' ').replace('\r', '').strip()

prompt=prompt.format(transcript=cleaned_transcript)
chain = LLMChain(llm=watsonx_llm, prompt=PromptTemplate.from_template(prompt))
response = chain.invoke({})
response_text = response['text']

# Remove the last line dynamically
lines = response_text.strip().splitlines()
if lines[-1].strip().startswith("Let me know"):
    response_text = "\n".join(lines[:-1])

print(response_text)
output_file = "\\temporary\\MoM_Document.doc"  # Change the file name as needed

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(response_text)

# Optionally, print a message indicating successful file write
print(f"MoM document saved as {output_file}")
