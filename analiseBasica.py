import pdfplumber
import pandas as pd
import re

pdf_path = "Catálogo_Atualizado.pdf"  # seu arquivo PDF
dados = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # Extrai tabelas baseadas nas linhas visuais
        table = page.extract_table()

        if not table:
            # Caso não detecte tabela visualmente, extrai texto bruto
            texto = page.extract_text(x_tolerance=2, y_tolerance=2)
            print("⚠️ Nenhuma tabela detectada nesta página, usando extração de texto simples.")
            print(texto)
            continue

        # Ignora o cabeçalho (primeira linha)
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

# Cria e salva no Excel
df = pd.DataFrame(dados)
df.to_excel("analiseBasica.xlsx", index=False)

print("✅ Extração concluída! Arquivo salvo como 'analiseBasica.xlsx'.")
