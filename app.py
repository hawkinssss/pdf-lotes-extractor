import pdfplumber
import pandas as pd
import re

pdf_path = "Catálogo_Atualizado.pdf"  # seu arquivo PDF
dados = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()

        if not table:
            texto = page.extract_text(x_tolerance=2, y_tolerance=2)
            print("⚠️ Nenhuma tabela detectada nesta página, usando extração de texto simples.")
            print(texto)
            continue

        for linha in table[1:]:
            if not any(linha):
                continue

            lote = linha[0].strip() if linha[0] else ""
            descricao = linha[1].strip() if linha[1] else ""
            valor = linha[2].strip() if len(linha) > 2 and linha[2] else ""
            anotacoes = linha[3].strip() if len(linha) > 3 and linha[3] else ""

            dados.append({
                "LOTE / CONTRATO": lote,
                "DESCRIÇÃO": descricao,
                "VALOR": valor,
                "ANOTAÇÕES": anotacoes
            })

# Cria o DataFrame
df = pd.DataFrame(dados)

# 🔍 REMOVE linhas onde a descrição contém "CONSTAM" ou "CONTÉM"
filtro = ~df["DESCRIÇÃO"].str.contains(r"\b(CONSTAM|CONTÉM)\b", case=False, na=False)
df_filtrado = df[filtro]

# Salva o resultado
df_filtrado.to_excel("analiseAvancada.xlsx", index=False)

print(f"✅ Extração concluída! {len(df_filtrado)} registros salvos em 'analiseAvancada.xlsx'.")
