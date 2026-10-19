import os
import re
import json
import pdfplumber
import voyageai
from dotenv import load_dotenv

load_dotenv()

client = voyageai.Client()

DOCS_FOLDER = "documents"
OUTPUT_FILE = "index.json"


def split_into_sections(text):
    """
    يقسم نص الصفحة لأقسام، بالاعتماد على نمط 'رقم. عنوان'
    مثال: '1. Introduction' أو '3. Key Details'
    """
    pattern = r'(?=\n?\d+\.\s+[A-Z])'
    parts = re.split(pattern, text)
    sections = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n", 1)
        if len(lines) == 2:
            title = lines[0].strip()
            body = lines[1].strip()
        else:
            title = "General"
            body = part
        sections.append({"title": title, "body": body})
    return sections

def build_chunks():
    chunks = []
    chunk_id = 0
    for filename in os.listdir(DOCS_FOLDER):
        if not filename.endswith(".pdf"):
            continue
        filepath = os.path.join(DOCS_FOLDER, filename)
        doc_name = filename.replace("Almamlaka_", "").replace(".pdf", "").replace("_", " ")
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                sections = split_into_sections(text)
                for section in sections:
                    # نتجاهل أي قسم عنوانه مش نمط "رقم. عنوان" (زي عنوان المستند العام)
                    if not re.match(r'^\d+\.\s', section["title"]):
                        continue
                    chunk_id += 1
                    chunks.append({
                        "id": f"chunk-{chunk_id}",
                        "doc": doc_name,
                        "file": filename,
                        "page": page_num,
                        "section": section["title"],
                        "text": section["body"]
                    })
    return chunks


def main():
    print("جاري قراءة الملفات وتقطيعها...")
    chunks = build_chunks()
    print(f"تم إيجاد {len(chunks)} مقطع.")

    texts = [chunk["text"] for chunk in chunks]

    print("جاري حساب الـ embeddings عبر Voyage...")
    result = client.embed(texts, model="voyage-multilingual-2", input_type="document")

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = result.embeddings[i]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"تم حفظ الفهرس بنجاح في {OUTPUT_FILE}")


if __name__ == "__main__":
    main()