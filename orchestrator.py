import json
from io import StringIO
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from tools.html_parser import HTMLParser
from tools.llama_index_multimodel import LlamaIndexMultiModel
from tools.pymupdf_extractor import PYMuPDFExtractor
from tools.tabula_extractor import TabulaExtractor
from tools.postgres import PostgresHelper
from tools.weasy import Weasy

class Orchestrator:
    """
    A class to orchestrate the process of extracting tables from HTML files,
    converting them to images and PDFs, and processing them with various tools.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Orchestrator class and its dependencies.
        """
        load_dotenv()
        self.pymupdf = PYMuPDFExtractor()
        self.tabula = TabulaExtractor()
        self.html_parser = HTMLParser()
        self.llama_index_multi_model = LlamaIndexMultiModel()
        self.postgres = PostgresHelper()
        self.weasy = Weasy()
        
    def run(self, ticker: str, html_file_path: str) -> None:
        """
        Run the orchestration process for a given ticker and HTML file path.

        Args:
            ticker (str): The ticker symbol for the company.
            html_file_path (str): The path to the HTML file containing tables.
        """
        try:
            marker = int(input("Enter an index to pause: "))
            tables = self.html_parser.get_tables(html_file_path)

            # Loop through each table
            for index, table in enumerate(tables):
                image_dir = Path(f'./files/{ticker}/{index}/image')
                image_dir.mkdir(exist_ok=True, parents=True)
                pdf_dir = Path(f'./files/{ticker}/{index}/pdf')
                pdf_dir.mkdir(exist_ok=True, parents=True)
                print(f"Processing Table Index: {index}")

                # Convert HTML to PDF and image
                image_file_path = self.weasy.html_to_image(table, f'{image_dir}/{index}.png')
                pdf_file_path = self.weasy.html_to_pdf(table, f'{pdf_dir}/{index}.pdf')

                # Process PDF with PYMuPDF
                pymupdf_response = self.pymupdf.process(pdf_file_path)
                if pymupdf_response:
                    print(f"PYMuPDF Output: \n{pymupdf_response[0].to_string(index=False)}")

                # Process PDF with Tabula
                tabula_response = self.tabula.process(pdf_file_path)
                if tabula_response:
                    print(f"Tabula Output: \n{tabula_response[0].to_string(index=False)}")

                # Pause at specified marker index
                if index == marker:
                    user_input = input("Enter an index to pause or press Enter to continue: ")
                    if not user_input:
                        marker = index + 1
                    else:
                        marker = int(user_input)

                    # Ask for OpenAI processing
                    run_openai = input("Run OpenAI for this table? [Y/n]: ")
                    if run_openai.lower() == 'y':
                        table_object = self.llama_index_multi_model.extract_table_from_image(image_dir)
                        print(">>> OpenAI processed table_object:", table_object)

                        # Ask to save to PostgreSQL
                        save_to_postgres = input("Do you want to save this to PostgreSQL? [Y/n]: ")
                        if save_to_postgres.lower() == 'y':
                            self.postgres.save_table_object(table_object)

        except Exception as e:
            print(f"An error occurred: {e}")
            
if __name__ == "__main__":
    orchestrator = Orchestrator()
    path = 'nvda-20240128.htm'
    orchestrator.run('nvda', path)
