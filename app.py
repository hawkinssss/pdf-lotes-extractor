import pdfplumber
import pandas as pd
import re

pdf_path = "Catálogo_Atualizado.pdf"
dados = []

def extrair_peso(texto):
    if not texto:
        return ""

    t = texto.lower().replace(",", ".")

    padrao = r"(\d+(\.\d+)?)\s*(g|grama|gramas)\b"

    match = re.search(padrao, t)
    if match:
        valor = float(match.group(1))
        return valor

    return ""


with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        table = page.extract_table()

        if not table:
            print(f"⚠️ Página {page_num}: Nenhuma tabela detectada.")
            continue

        header = [h.strip().lower() if h else "" for h in table[0]]

        try:
            idx_lote = next(i for i, h in enumerate(header) if "lote" in h or "contrato" in h)
        except StopIteration:
            idx_lote = 0

        try:
            idx_desc = next(i for i, h in enumerate(header) if "desc" in h or "descr" in h)
        except StopIteration:
            idx_desc = 1

        try:
            idx_valor = next(i for i, h in enumerate(header) if "valor" in h)
        except StopIteration:
            idx_valor = 2

        for linha in table[1:]:
            if not any(linha):
                continue

            lote = linha[idx_lote].strip() if idx_lote < len(linha) and linha[idx_lote] else ""
            descricao = linha[idx_desc].strip() if idx_desc < len(linha) and linha[idx_desc] else ""
            valor = linha[idx_valor].strip() if idx_valor < len(linha) and linha[idx_valor] else ""

            peso_lote = extrair_peso(descricao)

            dados.append({
                "LOTE / CONTRATO": lote,
                "DESCRIÇÃO": descricao,
                "VALOR": valor,
                "PESO LOTE (g)": peso_lote
            })

df = pd.DataFrame(dados)

filtro = ~df["DESCRIÇÃO"].str.contains(r"\b(CONSTAM|CONTÉM)\b", case=False, na=False)
df_filtrado = df[filtro]

df_filtrado.to_excel("analiseAvancada.xlsx", index=False)

print(f"✅ Extração concluída! {len(df_filtrado)} registros salvos em 'analiseAvancada.xlsx'.")
