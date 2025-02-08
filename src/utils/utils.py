from google.cloud.vision_v1 import types
from google.cloud import vision_v1
import face_recognition as fr
import os
import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def extrair_dado(texto, documento):
    linhas = texto.split("\n")
    user_data = {
        'nome': '',
        'data_nascimento': '',
        'data_emissao': '',
        'numero_registro': '',
        'cpf': '',
        'nome_pai': '',
        'nome_mae': ''
    }

    if documento == 'cnh':
        for i, linha in enumerate(linhas):
            if "NOME E SOBRENOME" in linha:
                user_data['nome'] = linhas[i + 1] if i + 1 < len(linhas) else ''
            if "DATA, LOCAL E UF DE NASCIMENTO" in linha:
                user_data['data_nascimento'] = linhas[i + 1] if i + 1 < len(linhas) else ''
            if "DATA EMISSÃO" in linha:
                user_data['data_emissao'] = linhas[i + 1] if i + 1 < len(linhas) else ''
            if "DOC IDENTIDADE/ORG. EMISSOR/UF" in linha:
                user_data['numero_registro'] = linhas[i + 1] if i + 1 < len(linhas) else ''
            if "CPF" in linha:
                user_data['cpf'] = linhas[i + 1] if i + 1 < len(linhas) else ''
            if "FILIAÇÃO" in linha:
                user_data['nome_pai'] = linhas[i + 6] if i + 6 < len(linhas) else ''
                user_data['nome_mae'] = linhas[i + 7] if i + 7 < len(linhas) else ''
    return user_data





def carregar_codificacoes_pessoas(pasta):

    codificacoes = []
    nomes = []
    
    for nome_arquivo in os.listdir(pasta):
        caminho_imagem = os.path.join(pasta, nome_arquivo)
        
        if caminho_imagem.lower().endswith(('.png', '.jpg', '.jpeg')):
            imagem_referencia = fr.load_image_file(caminho_imagem)
            imagem_referencia_rgb = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2RGB)
            
            codificacoes_rosto = fr.face_encodings(imagem_referencia_rgb)
            if codificacoes_rosto:
                codificacoes.append(codificacoes_rosto[0])
                nomes.append(nome_arquivo.split('.')[0])
    
    return codificacoes, nomes

def reconhecer_rosto_para_login(imagem_input, pasta_imagens):

    codificacoes_pessoas, nomes_pessoas = carregar_codificacoes_pessoas(pasta_imagens)

    if not codificacoes_pessoas:
        return "null"  

    imagem_input_rgb = cv2.cvtColor(imagem_input, cv2.COLOR_BGR2RGB)

    face_locations = fr.face_locations(imagem_input_rgb)
    if not face_locations:
        return "null"  

    for face_location in face_locations:
        codificacao_rosto = fr.face_encodings(imagem_input_rgb, [face_location])

        if codificacao_rosto:
            for i, codificacao in enumerate(codificacoes_pessoas):
                match = fr.compare_faces([codificacao], codificacao_rosto[0])

                if match[0]:  
                    return nomes_pessoas[i] 
    return "null"  






def detect_document_text(image_path: str):
    api_key = 'AIzaSyAOiewr_WEerviGsVCZ_Skc66Jt8rckm4M'
    client = vision_v1.ImageAnnotatorClient(client_options={"api_key": api_key})
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    # Detecta o texto do documento
    response = client.document_text_detection(image=image)
    # Checa se o serviço detectou algum texto
    if response.text_annotations:
        full_text = response.text_annotations[0].description
        return full_text
    else:
        print("Nenhum texto detectado.")


def enviar_email(destinatario, assunto, mensagem):
    remetente = "seuemail@gmail.com"
    senha = "sua_senha"

    # Criando a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(mensagem, "plain"))

    try:
        # Conectando ao servidor SMTP do Gmail
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
