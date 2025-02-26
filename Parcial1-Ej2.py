# Mediante el algoritmo RSA Alice firmará digitalmente el contrato NDA.pdf

import Crypto.Util.number as num
import Crypto.Random as rand
import hashlib
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
import os

def generar_llaves():
    primo1 = num.getPrime(1024, randfunc=rand.get_random_bytes)
    primo2 = num.getPrime(1024, randfunc=rand.get_random_bytes)

    publica = primo1 * primo2
    phi = (primo1 - 1) * (primo2 - 1)
    privada = num.inverse(e, phi)
    return publica, privada

def generar_hash(message):
    encoded_message = message.encode()
    hash_bytes = hashlib.sha512(encoded_message).digest()
    hash_int = int.from_bytes(hash_bytes, byteorder='big')
    return hash_int

def obtener_firma(startWith, reader):
    pdf_text = reader.pages[-1].extract_text()
    text_firma = pdf_text.split()
    is_firma = False
    firma = ""
    for text in text_firma:
        if is_firma:
            firma += text

        if text.startswith(startWith):
            is_firma = True
    return int(firma)

e = 65537

# Obtención de las claves de Alice
publica_Alice, privada_Alice = generar_llaves()

# Obtención de las claves de Bob
publica_Bob, privada_Bob = generar_llaves()

# Obtención de las claves de la Autoridad Certificadora
publica_AC, privada_AC = generar_llaves()

# Obtención de la firma de Alice
hM_Alice = generar_hash("En efecto, esta es la firma de Alice")
firma_Alice = pow(hM_Alice, privada_Alice, publica_Alice)

# Agregación de la firma de Alice al PDF
reader1 = PdfReader("NDA.pdf")
writer1 = PdfWriter()

last_page = reader1.pages[-1]

for page in reader1.pages[:-1]:
    writer1.add_page(page)

pdf = FPDF()
pdf.set_font("Arial", size=8)

pdf.add_page()
pdf.ln(200)
pdf.multi_cell(0, 4, f"Firma Alice: \n{firma_Alice}")

pdf.output("Extra.pdf")
Alice_reader = PdfReader("Extra.pdf")
Alice_page = Alice_reader.pages[0]

last_page.merge_page(Alice_page)

writer1.add_page(last_page)

with open("NDA_1_firma.pdf", "wb") as f:
    writer1.write(f)

# Autoridad Certificadora verifica la firma de Alice
firma_pdf_Alice = obtener_firma("Alice", reader1)

hM1_Alice = pow(firma_pdf_Alice, e, publica_Alice)
print(f"Verificación firma Alice: {hM_Alice == hM1_Alice}")

# Obtención de la firma de Autoridad Certificadora
hM_AC = generar_hash("En efecto, esta es la firma de la Autoridad Certificadora")
firma_AC = pow(hM_AC, privada_AC, publica_AC)

# Agregación de la firma de Autoridad Certificadora al PDF
reader2 = PdfReader("NDA_1_firma.pdf")
writer2 = PdfWriter()

last_page = reader2.pages[-1]

for page in reader2.pages[:-1]:
    writer2.add_page(page)

pdf = FPDF()
pdf.set_font("Arial", size=8)

pdf.add_page()
pdf.ln(235)
pdf.multi_cell(0, 4, f"Firma Autoridad Certificadora: \n{firma_AC}")

pdf.output("Extra.pdf")
AC_reader = PdfReader("Extra.pdf")
AC_page = AC_reader.pages[0]

last_page.merge_page(AC_page)

writer2.add_page(last_page)

with open("NDA_2_firmas.pdf", "wb") as f:
    writer2.write(f)


# Bob verifica la firma de la Autoridad Certificadora
firma_pdf_AC = obtener_firma("Certificadora", reader2)

hM1_AC = pow(firma_pdf_AC, e, publica_AC)
print(f"Verificación firma AC: {hM_AC == hM1_AC}")

# Eliminar el archivo Extra.pdf
# En este archivo se guardaba la firma para hacer merge con el pdf principal
if os.path.exists("Extra.pdf"):
    os.remove("Extra.pdf")
