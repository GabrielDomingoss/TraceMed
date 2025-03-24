from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from database import get_db
from models.process import Process
from models.failure import Failure
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import pandas as pd
import os

router = APIRouter()

@router.get("/pdf", response_class=StreamingResponse)
def gerar_relatorio_pdf(db: Session = Depends(get_db)):
    processos = db.query(Process).all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def escrever_etapa(nome, data, observacao):
        if data:
            data_formatada = data.strftime("%d/%m/%Y %H:%M")
            texto = f"{nome}: {data_formatada} - {observacao or 'Sem observações'}"
        else:
            texto = f"{nome}: Não realizada"
        pdf.set_x(10)
        pdf.multi_cell(0, 8, txt=texto)

    for processo in processos:
        pdf.set_font("Arial", "B", 12)
        pdf.set_x(10)
        pdf.cell(0, 10, f"Processo ID: {processo.id}", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.set_x(10)
        pdf.cell(0, 8, f"Material ID: {processo.material_id}", ln=True)

        escrever_etapa("Recebimento", processo.data_recebimento, processo.observacao_recebimento)
        escrever_etapa("Lavagem", processo.data_lavagem, processo.observacao_lavagem)
        escrever_etapa("Esterilização", processo.data_esterilizacao, processo.observacao_esterilizacao)
        escrever_etapa("Distribuição", processo.data_distribuicao, processo.observacao_distribuicao)

        falhas = db.query(Failure).filter(Failure.process_id == processo.id).all()
        if falhas:
            pdf.set_x(10)
            pdf.cell(0, 10, "Falhas:", ln=True)
            for falha in falhas:
                critica = "Crítica" if falha.critical else "Comum"
                texto = f"• {falha.etapa.capitalize()} - {critica}: {falha.descricao} ({falha.data.strftime('%d/%m/%Y %H:%M')})"
                pdf.set_x(10)
                pdf.multi_cell(0, 8, txt=texto)

        pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/pdf", headers={
        "Content-Disposition": "inline; filename=relatorio_processos.pdf"
    })

@router.get("/xlsx", response_class=FileResponse)
def gerar_relatorio_xlsx(db: Session = Depends(get_db)):
    processos = db.query(Process).options(
        joinedload(Process.material),
        joinedload(Process.failures),
        joinedload(Process.usuario_recebimento),
        joinedload(Process.usuario_lavagem),
        joinedload(Process.usuario_esterilizacao),
        joinedload(Process.usuario_distribuicao)
    ).all()

    dados = []
    for processo in processos:
        row = {
            "ID Processo": processo.id,
            "Material": f"{processo.material.nome} (ID: {processo.material.id})",
            "Serial": processo.material.serial,
            "Recebimento": formatar_etapa(processo.data_recebimento, processo.observacao_recebimento, processo.usuario_recebimento),
            "Lavagem": formatar_etapa(processo.data_lavagem, processo.observacao_lavagem, processo.usuario_lavagem),
            "Esterilização": formatar_etapa(processo.data_esterilizacao, processo.observacao_esterilizacao, processo.usuario_esterilizacao),
            "Distribuição": formatar_etapa(processo.data_distribuicao, processo.observacao_distribuicao, processo.usuario_distribuicao),
            "Falhas": formatar_falhas(processo.failures),
            "Interrompido": "Sim" if any(f.critical for f in processo.failures) else "Não"
        }
        dados.append(row)

    df = pd.DataFrame(dados)

    nome_arquivo = f"relatorio_processos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    caminho = os.path.join("relatorios", nome_arquivo)
    os.makedirs("relatorios", exist_ok=True)
    df.to_excel(caminho, index=False)

    # Ajustes com openpyxl
    wb = load_workbook(caminho)
    ws = wb.active

    # Quebra de linha na coluna de falhas
    col_falhas = 8  # H
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=col_falhas)
        cell.alignment = Alignment(wrap_text=True)

        # Ajusta a altura da linha com base na quantidade de quebras
        num_linhas = cell.value.count("\n") + 1 if cell.value else 1
        ws.row_dimensions[row].height = num_linhas * 15

    # Ajuste de largura automática
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column].width = max_length + 2

    wb.save(caminho)

    return FileResponse(
        caminho,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=nome_arquivo
    )

def formatar_etapa(data, observacao, usuario):
    if not data:
        return "-"
    user = f"{usuario.name} (ID: {usuario.id})" if usuario else "Usuário desconhecido"
    obs = f" - {observacao}" if observacao else ""
    return f"{data.strftime('%d/%m/%Y %H:%M')} - {user}{obs}"

def formatar_falhas(falhas):
    if not falhas:
        return "-"
    return "\n".join(
        f"{f.etapa.capitalize()} - {'Crítica' if f.critical else 'Comum'}: {f.descricao} ({f.data.strftime('%d/%m/%Y %H:%M')})"
        for f in falhas
    )
