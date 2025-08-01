import streamlit as st
import boto3
import uuid

# Correct AWS Region Code
region = "us-east-1"

# Your agent details
bedrock_agent_id = "NAUTFAXAAJ"
bedrock_agent_alias_id = "GFYOEQ57SI"

client = boto3.client("bedrock-agent-runtime", region_name=region)

def query_agent(user_input, session_id):
    response_stream = client.invoke_agent(
        agentId=bedrock_agent_id,
        agentAliasId=bedrock_agent_alias_id,
        sessionId=session_id,
        inputText=user_input
    )

    full_response = ""

    for event in response_stream['completion']:
        if 'chunk' in event:
            content_chunk = event['chunk']['bytes'].decode("utf-8")
            full_response += content_chunk

    return full_response or "No response from agent."

# Streamlit UI
st.set_page_config(page_title="BMO Credit Policy Assistant", layout="wide")
st.title("💳 BMO Internal Credit Policy Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

user_input = st.text_input("Ask a question about BMO credit policies:")

if user_input:
    with st.spinner("Getting answer..."):
        answer = query_agent(user_input, st.session_state.session_id)
        st.markdown(f"**Answer:** {answer}")