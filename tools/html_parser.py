from bs4 import BeautifulSoup
import pandas as pd


class HTMLParser:
    """
    Class for extracting and cleaning tables from HTML files using BeautifulSoup.
    """

    def __init__(self):
        pass

    def clean(self, table):
        """
        Cleans a single HTML table element.

        Args:
            table (bs4.element.Tag): The table element to clean.

        Returns:
            pandas.DataFrame: The cleaned table data as a DataFrame.
        """
        df.dropna(how='all', inplace=True)
        
        # Check for columns with NaN headers and drop them if all values in that column are NaN
        columns_to_drop = [col for col in table.columns if pd.isna(col) and table[col].isna().all()]
        table.drop(columns=columns_to_drop, inplace=True)
        
        # Reset index
        table.reset_index(drop=True, inplace=True)
        
            # Identify and drop adjacent columns with identical values
        cols_to_keep = []
        previous_col = None
        
        for col in table.columns:
            if previous_col is None or not table[previous_col].equals(table[col]):
                cols_to_keep.append(col)
            previous_col = col
        
        table = table[cols_to_keep]
        
        # Display the first few rows of the cleaned table
        return table

    def fix_headers(self, table):
        # Prepare to store concatenated headers
        concatenated_headers = []

        # Process the table headers
        if head := table.find('thead'):
            header_row = head.find('tr')
            headers = header_row.find_all('td')

            # Extract header texts
            header_texts = [th.text.strip() for th in headers]

            # Iterate through header texts
            for header_text in header_texts:
                concatenated_headers.append(header_text)

            # Process the table body
            body_rows = table.find('tbody').find_all('tr')

            # Iterate through each row in the body
            for row in body_rows:
                row_cells = row.find_all('td')
                for idx, cell in enumerate(row_cells):
                    if idx < len(concatenated_headers):
                        concatenated_headers[idx] += ' ' + cell.text.strip()

            # Generate the resulting HTML table
            result_table_html = '<table><thead><tr>'

            # Add concatenated headers as table headers
            for header in concatenated_headers:
                result_table_html += f'<th>{header}</th>'

            result_table_html += '</tr></thead><tbody>'

            # Add body rows with existing data
            for row in body_rows:
                result_table_html += str(row)

            result_table_html += '</tbody></table>'
        return table

    def process(self, html_path):
        """
        Extracts all tables from an HTML file and returns them as DataFrames.

        Args:
            html_path (str): Path to the HTML file.

        Returns:
            list: A list of pandas.DataFrame objects representing the cleaned tables.
        """
        cleaned_tables = []
        tables = self.get_tables(html_path)

        # Clean each table and append to the list
        for table in tables:
            try:
                df = pd.read_html('<html>'+table+'</html>')
                cleaned_df = self.clean(df)
                cleaned_tables.append(cleaned_df)
            except:
                continue
        
        return cleaned_tables

    def get_tables_sibling_content(self, html_path):
        """
        Extracts all tables from an HTML file and returns them as html table tags <table>.

        Args:
            html_path (str): Path to the HTML file.

        Returns:
            Dict: A dict of  html table tag <table> objects as key and it's sibling content as value.
        """                
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f, "html.parser")

        content = {}
        
        # Find all table elements
        tables = soup.find_all('table')
        for table in tables:          
            if table.parent.previous_sibling: 
                previous_sibling = table.parent.previous_sibling.get_text()
                content[table] = previous_sibling
            else:
                content[table] = None
        return content
            

    def get_tables(self, html_path):
        """
        Extracts all tables from an HTML file and returns them as html table tags <table>.

        Args:
            html_path (str): Path to the HTML file.

        Returns:
            list: A list of  html table tag <table> objects representing the cleaned tables.
        """        
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find all table elements
        tables = soup.find_all('table')
        return tables

if __name__ == "__main__":
    # Example usage
    html_parser = HTMLParser()
    path = '/home/ubuntu/playground/sec_gov/Archives/edgar/data/1045810/000104581024000029/0001-(10-K)_10-K_nvda-20240128.htm'
    cleaned_dfs = html_parser.get_tables(path)
    # Access individual cleaned DataFrames from the list
    for df in cleaned_dfs:
        print(df)
