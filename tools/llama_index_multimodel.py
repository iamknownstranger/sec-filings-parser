import os
from typing import Dict, List

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from pydantic import BaseModel, Field

load_dotenv()

import base64

class TableInfo(BaseModel):
    """Information regarding a structured table."""

    name: str = Field(
        ..., description="name of the table (must be underscores and NO spaces)"
    )
    summary: str = Field(
        ..., description="short, concise summary/caption of the table"
    )    
    
    columns: List[str] = Field(
        ..., description="list of columns of the table seperated by comma"
    )    
    
    data: List[Dict] = Field(
        ..., description="The data of the table in list of dicts format"
    )

class LlamaIndexMultiModel:
    
    def __init__(self):    
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.llm = OpenAIMultiModal(
            model="gpt-4o", api_key=OPENAI_API_KEY, max_new_tokens=1000
        )

    def extract_table_from_image(self, image_dir, sibling_content=None):

        image_documents = SimpleDirectoryReader(image_dir).load_data()
        sibling_text =  f"and here is sibling content: {sibling_content}" if sibling_content else ""
        prompt_template_str = f"""Please review the image carefully which has a table {sibling_text}
                                There might be column names that are spread across multiple rows in the table and please standardize the multi level column names by giving renaming in a meaningful way 
                                return the table data with json format
                            """
        openai_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(TableInfo),
            image_documents=image_documents,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
            verbose=True,
        )

        response = openai_program()
        try:
            with open(f'{image_dir}/document.json', 'w') as file:
                file.write(response.model_dump_json())
        except:
            pass
        return response

    def extract_table_from_text(self, table_str):
        prompt_template_str = f"""Please review the following data which has a table and the same table in pandas to_string
                    
                                Table string:
                                {table_str}"s

                                Fix the table structure and misalignment of column where in some columns are split into two while parsing the data
                                There might be column names that are spread across multiple rows in the table.

                                DO NOT include any addional any extra information except the following

                                Always return the response in json format
                            """
        openai_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(TableInfo),
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
            verbose=True,
        )

        response = openai_program()
        return response
