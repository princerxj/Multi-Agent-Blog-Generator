from pydantic import BaseModel, Field 

class BlogState(BaseModel) : 
    ### User Input 
    topic : str = Field(default = "", description = "Topic on which the user want to write the Blog")
    audience : str = Field(default = "General reader", description = "Audience")

    ### Researcher Output 
    research : str = Field(default = "", description = "What we have found in the research")
    research_feedback : str = Field(default = "", description = "User feedback on the research")

    ### writer Output 
    draft : str = Field(default = "", description = "The blog drafted by the writer")
    draft_feedback : str = Field(default = "", description = "Usera feedback on the draft")

    ### Editor Output 
    final_blog : str = Field(default = "", description = "Final Blog")

    ### Meta Data
    revision_count : int = 0