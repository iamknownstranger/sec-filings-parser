from weasyprint import HTML

class Weasy:
    """
    A helper class to convert HTML strings to PNG or PDF using WeasyPrint.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Weasy class with default CSS settings.
        """
        self.css_string = """
            <head>
            <style>
            body {
                margin: 0;
                padding: 0;
                max-width: 100%;
                vertical-align: text-top;
            }
            div {
                background-color: white;
                max-width: 100%;
                padding: 2%;
            }
            table {
                border-collapse: collapse; 
                table-layout: auto;
                max-width: 98%;
                page-break-inside: avoid;
                white-space: normal;
                background-color: white;
            }
            th, tr, td, tbody {
                max-width: 98%;
                word-wrap: break-word;
            }
            </style>
            </head>
        """
            
    def _get_html_with_css(self, html_table_string: str) -> str:
        """
        Wrap the provided HTML table string with default CSS.
        
        Args:
            html_table_string (str): The HTML string to be wrapped with CSS.
        
        Returns:
            str: The complete HTML string with CSS.
        """
        return f"""<html>{self.css_string}
            <body><div>{html_table_string}</div></body></html>"""
    
    def html_to_image(self, html_string: str, file_path: str = 'files/weasy.png', override_css: bool = True) -> str:
        """
        Convert an HTML string to a PNG image.
        
        Args:
            html_string (str): The HTML string to be converted.
            file_path (str): The file path where the PNG image will be saved.
            override_css (bool): Whether to override the HTML string's CSS with the default CSS.
        
        Returns:
            str: The file path of the saved PNG image.
        """
        try:
            if override_css:
                html_string = self._get_html_with_css(html_string)
            HTML(string=html_string).write_png(file_path, resolution=300)
            return file_path
        except Exception as e:
            print(f"Error converting HTML to image: {e}")
            return ""
        
    def html_to_pdf(self, html_string: str, file_path: str = 'files/weasy.pdf', override_css: bool = True) -> str:
        """
        Convert an HTML string to a PDF document.
        
        Args:
            html_string (str): The HTML string to be converted.
            file_path (str): The file path where the PDF document will be saved.
            override_css (bool): Whether to override the HTML string's CSS with the default CSS.
        
        Returns:
            str: The file path of the saved PDF document.
        """
        try:
            if override_css:
                html_string = self._get_html_with_css(html_string)
            HTML(string=html_string).write_pdf(file_path)
            return file_path
        except Exception as e:
            print(f"Error converting HTML to PDF: {e}")
            return ""
