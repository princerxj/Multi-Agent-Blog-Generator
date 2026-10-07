import os 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

### Get LLM 
def get_llm(model_name : str = "openai/gpt-oss-20b", temperature : float = 0.5) : 
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model = model_name, 
        api_key=api_key, 
        temperature=temperature
    )
    return llm 

### Researcher Agent 
researcher_prompt = ChatPromptTemplate.from_messages([
    {"role" : "System", "content" : """

        "You are a research agent. Give a blog topic and target audience, produce a clear, "
        "structured research outline. Include : \n"
        "1. 5-7 Key points the blog should cover \n"
        "2. Important facts , stats, or examples for each point \n"
        "3. Suggested angle or hook \n"
        "Be concise. Use Bullet Points . Do not write the full blog yet."

    """}, 
    {"role" : "user", "content" : "Topic : {topic}, Audience : {audience}, {revision_hints}, Write the research outline now."}
])

def researcher_agent(llm: ChatGroq, topic : str , audience : str, feedback : str = "") -> str :
    revision_hints = f"The human provided this feedback on your previous research - please address it : {feedback}"

    if not feedback : 
        revision_hints = "This is your first attempt . "

    chain = researcher_prompt | llm 

    result = chain.invoke({
        "topic" : topic, 
        "audience" : audience, 
        "revision_hints" : revision_hints
    })

    return result.content

### Writer agent 
writer_prompt = ChatPromptTemplate.from_messages([
    {"role" : "system", "content" : """
        "You are a blog writer agent. Using the research notes provided, write a complete,"
        "engaging blog post . \n"
        "Rules : \n"
        "- Length : 500 - 800 words \n"
        "- structure : catchy title, intro hook, 3-5 sections with H2 headings , conclusion \n"
        "- Tone : clear, friendly , suited to the target audience \n"
        "- Use markdown formatting . \n" 
        "- Do not add a 'word count' line at the end " 
    """}, 
    {"role" : "user", "content" : """
        Topic : {topic}, 
        Audience : {audience}, 
        Research_Notes : {research}, 
        {revision_hints}. 
        Write the full blog post now.
    """}
])

def writer_agent(llm : ChatGroq, topic : str, audience : str, research : str = "", feedback : str = "") -> str : 
    revision_hints = f"The human provided this feedback on your previous draft and asked for these changes : {feedback}. Please apply these changes during writing the blog ."
    if not feedback : 
        revision_hints = "This is your first attempt. "

    chain = writer_prompt | llm 

    result = chain.invoke({
        "topic" : topic, 
        "audience" : audience, 
        "research" : research, 
        "revision_hints" : revision_hints
    })

    return result.content

### Editor Agent 
editor_prompt = ChatPromptTemplate.from_messages([
    {"role" : "system", "content" : """
        "You are an editor agent - the final quality gate before publising . \n"
        "Take the draft and produce the Final polished version. Specifically : \n"
        "- Fix grammar , spelling, and awkward phrasing \n"
        "- Tighten wordy sentences \n"
        "- Improve flow and transitions between sections \n"
        "- Make the title and intro more compelling if needed \n" 
        "- Keep the same structure and markdown formatting \n" 
        "- Blog wordings should look like human not AI, and don't use any special chars and complex / fancy words. \n"
        "Output only the final polished blog post - no commentary."
    """}, 
    {"role" : "user", "content" : """
        Topic : {topic}, 
        Draft : {draft}

        Return the published blog post. 
    """}
])

def editor_agent(llm : ChatGroq, topic : str, draft : str = "") -> str : 
    chain = editor_prompt | llm 

    result = chain.invoke({
        "topic" : topic, 
        "draft" : draft
    })

    return result.content

