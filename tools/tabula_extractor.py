import tabula
import re

from tools.base import BaseClass

class TabulaExtractor(BaseClass):
    """
    Class for processing and cleaning tables from PDF files using Tabula.
    """

    def __init__(self):
        self.missing_column_pattern = r'\bUnnamed: \d+\b'
    def clean(self, df):
        """
        Cleans column names in a DataFrame by removing 'Col' prefix.

        Args:
            df (pandas.DataFrame): The DataFrame to clean.

        Returns:
            pandas.DataFrame: The cleaned DataFrame with renamed columns.
        """
        cols_to_drop = []
        for col in df.columns:
            if df[col].isna().all() and re.match(self.missing_column_pattern, col):
                cols_to_drop.append(col)
        df.drop(columns=cols_to_drop, inplace=True)
        df.fillna('    ', inplace=True)
        col_names = df.columns.to_series().str.replace(r'\bUnnamed: \d+\b', '   ' , regex=True)
        return df.rename(columns=col_names.to_dict())

    def process(self, file_path):
        """
        Extracts tables from a PDF file, converts them to DataFrames,
        cleans column names, and returns a list of cleaned DataFrames.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            list: A list of pandas.DataFrame objects representing the cleaned tables.
        """
        cleaned_tables = []
        dfs = tabula.read_pdf(file_path, pages='all')
        for df in dfs:
            cleaned_df = self.clean(df.copy())  # Avoid modifying original data
            cleaned_tables.append(cleaned_df)
        return cleaned_tables

if __name__ == "__main__":
    pdf_processor = TabulaExtractor()
    cleaned_dfs = pdf_processor.process("nvda.pdf")

    # Access individual cleaned DataFrames from the list
    for df in cleaned_dfs:
        print(df)
