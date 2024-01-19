from unstructured.partition.pdf import partition_pdf
import textwrap

class PDFLoader:
    def __init__(self, filename):
        """
        Initialize the PDFLoader class with the provided filename.

        Parameters:
        - filename (str): The path to the PDF file.
        """
        self.filename = filename
        self.elements = self.load_pdf()

    def load_pdf(self):
        """
        Load the PDF file and use the provided function to partition it into elements.

        Returns:
        - list: List of elements extracted from the PDF.
        """
        return partition_pdf(filename=self.filename)

    def split_into_sections(self, char_limit=200):
        """
        Split the extracted elements into sections based on a character limit.

        Parameters:
        - char_limit (int): Maximum number of characters in each section.

        Returns:
        - list: List of sections containing text.
        """
        narrative_texts = [elem.text for elem in self.elements]
        output_text = ""
        sections = []

        for index, elem_text in enumerate(narrative_texts[:]):
            section_text = "\n".join(textwrap.wrap(elem_text, width=70))

            if len(output_text + section_text) >= char_limit:
                sections.append(output_text)
                output_text = section_text
            else:
                output_text += section_text

        # Append the remaining text if any
        if output_text:
            sections.append(output_text)

        return sections
