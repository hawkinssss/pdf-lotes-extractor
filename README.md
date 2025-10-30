# Extração de Lotes de PDF para Excel

Este projeto permite extrair automaticamente informações de **lotes, descrições e valores** a partir de um arquivo **PDF** e exportá-las para uma planilha **Excel (.xlsx)**.

O script:
- Mantém o texto da descrição exatamente como está no PDF (com quebras de linha e acentuação);
- Filtra automaticamente os lotes que contenham as palavras **"CONSTAM"** ou **"CONTÉM"** na descrição;
- Gera um arquivo Excel limpo e pronto para análise.

---

## 🧩 Requisitos

- Python **3.8+**
- As seguintes bibliotecas:

```bash
pip install pdfplumber pandas openpyxl
