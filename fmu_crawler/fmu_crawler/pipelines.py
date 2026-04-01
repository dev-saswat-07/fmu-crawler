import os
import hashlib
import json
import PyPDF2
import io
from PIL import Image
import pytesseract

class FmuPipeline:
    def __init__(self):
        self.download_dir = 'downloads'
        self.text_dir = 'extracted_text'
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.text_dir, exist_ok=True)

    def process_item(self, item, spider):
        if 'file_body' in item:
            url = item['url']
            ext = self._get_extension(url, item['type'])
            filename = hashlib.sha256(url.encode()).hexdigest() + ext
            filepath = os.path.join(self.download_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(item['file_body'])

            sha256 = hashlib.sha256(item['file_body']).hexdigest()
            item['file_path'] = filepath
            item['file_hash'] = sha256

            text = self.extract_text(item['type'], item['file_body'], spider)
            item['content'] = text

            text_filename = os.path.join(self.text_dir, filename + '.txt')
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write(text or '')

            del item['file_body']

        metadata = {
            'url': item['url'],
            'type': item['type'],
            'file_path': item.get('file_path'),
            'file_hash': item.get('file_hash'),
            'text': item.get('content', '')
        }
        with open('metadata.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(metadata, ensure_ascii=False) + '\n')

        return item

    def _get_extension(self, url, file_type):
        ext = os.path.splitext(url)[1]
        if ext:
            return ext
        return '.pdf' if file_type == 'pdf' else '.jpg'

    def extract_text(self, file_type, raw_bytes, spider):
        if file_type == 'pdf':
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
                text = ''
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                return text.strip()
            except Exception as e:
                spider.logger.error(f"PDF extraction failed: {e}")
                return ''
        elif file_type == 'image':
            try:
                image = Image.open(io.BytesIO(raw_bytes))
                text = pytesseract.image_to_string(image)
                return text.strip()
            except Exception as e:
                spider.logger.error(f"OCR failed: {e}")
                return ''
        return ''
