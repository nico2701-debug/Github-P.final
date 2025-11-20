# -*- coding: latin-1 -*-
# Proyecto_1_dashboard.py
# Autor: Giovanni Mogollon Bastardo
# Descripcion:
# Dashboard 

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Análisis de %GC de secuencias FASTA")

# ======= FUNCION PARA CALCULAR %GC, se hace una suma de las bases G y C para dividirlo entre el total de bases, y poder sacar el % =========
def calcular_gc(seq):
    seq = seq.upper()
    gc_count = seq.count("G") + seq.count("C")
    total_bases = len(seq.replace("N", ""))
    return round((gc_count / total_bases) * 100, 2) if total_bases > 0 else 0

# ======= FUNCION PARA SIMPLIFICAR LOS NOMBRES, simplifica la lectura =========
def nombre_bacteria(encabezado, nombres_usados, max_words=4):
    # Quitar '>' y caracteres no alfabéticos
    nombre = encabezado.replace(">", "").strip()
    nombre = re.sub(r'[^A-Za-z\s]', '', nombre)  # solo letras y espacios
    palabras = nombre.split()[:max_words]  # solo primeras N palabras
    nombre_corto = "_".join(palabras)  # unir con guiones bajos
    contador = 1
    nombre_final = nombre_corto
    while nombre_final in nombres_usados:
        nombre_final = f"{nombre_corto}_{contador}"
        contador += 1
    nombres_usados.add(nombre_final)
    return nombre_final

# ======= SUBIDA DE ARCHIVOS ======
uploaded_files = st.file_uploader(
    "Sube tus archivos FASTA (opcional si quieres usar la carpeta)",
    type=["fasta", "fa"],
    accept_multiple_files=True
)

# ======= LEER DESDE CARPETA ======
usar_carpeta = st.checkbox("Leer FASTA desde carpeta local", value=True)
ruta_carpeta = r"C:\Users\gj301\OneDrive\Escritorio\Python\Proyecto1\Proyecto_1\PythonApplication1\fastas" #esta ruta es la personal, por lo cual cambia dependiendo del usuario

resultados = []
nombres_usados = set()

# ======= PROCESAR ARCHIVOS: subir los archivos fasta, para los cuales se calculará el GC de cada organismo ======
if uploaded_files:
    for file in uploaded_files:
        lineas = file.read().decode("utf-8").splitlines()
        secuencia = "".join(lineas[1:])
        gc = calcular_gc(secuencia)
        nombre_final = nombre_bacteria(lineas[0], nombres_usados)
        resultados.append({"Organismo": nombre_final, "%GC": gc})

elif usar_carpeta:
    archivos = sorted([f for f in os.listdir(ruta_carpeta) if f.endswith((".fasta", ".fa"))])
    for archivo in archivos:
        with open(os.path.join(ruta_carpeta, archivo), "r") as f:
            lineas = f.readlines()
            secuencia = "".join([linea.strip() for linea in lineas[1:]])
            gc = calcular_gc(secuencia)
            nombre_final = nombre_bacteria(lineas[0], nombres_usados)
            resultados.append({"Organismo": nombre_final, "%GC": gc})

# ======= MOSTRAR RESULTADOS ======
if resultados:
    df = pd.DataFrame(resultados)
    st.subheader("Tabla de resultados")
    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(10,6)) #creación de un gráfico de barras
    ax.bar(df["Organismo"], df["%GC"], color="blue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("% de GC")
    plt.title("Comparación del contenido GC entre secuencias")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Sube archivos FASTA o activa la opción de leer desde la carpeta para ver resultados.") #al no marcar la opción de "leerlos desde carpeta local", se pueden seleccionar los archivos fasta manualmente (acción a realizar si no se cambia la ruta en la linea 46 del codigo)
    








