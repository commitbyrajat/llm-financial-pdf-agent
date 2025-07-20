from pypdf import PdfReader


class PdfRetriever:
    def __init__(self, file_path):
        self.reader = PdfReader(file_path)
        self.pages = []
        self.tokens = 0
        for page in self.reader.pages:
            text = page.extract_text()
            self.pages.append(text)
            self.tokens += len(text)

    def get_docs(self):
        print("Page Count: ", len(self.pages))
        return self.pages

    def get_tokens(self):
        return self.tokens
