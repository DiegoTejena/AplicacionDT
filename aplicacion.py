import streamlit as st 
import pandas as pd 
import lasio 
from PIL import Image
from io import StringIO
import altair as alt
import matplotlib.pyplot as plt
st.title("Proyecto Aplicable de Diego Tejena")
inicio = Image.open("Inicio.jpg")
st.image(inicio)
st.sidebar.title("Men煤")

opciones_inicio= st.sidebar.radio("Seleccione una opci贸n",["馃彔 Inicio","Data Informaci贸n","Data Analisis","Data Visualizacion"])
#llamar un archivo
#archivo_las= lasio.read("LGAE-040.las")
#df=archivo_las.df()

if opciones_inicio == "馃彔 Inicio":
	st.write("Bienvenidos a mi primera aplicacion")

	with st.expander("Descripcion del Aplicativo"):
		st.write(""" 
			1. Cargue el archivo .las con el registro a analizar
			2. Ingrese los parametros que desea evaluar
			3. Visualice e interpretelos datos.

			""")

	with st.expander("Descripci贸n de las secciones"):
		st.write("""
    	
			Inicio: En la secci贸n de Inicio se encuentra la descripcion de la aplicaci贸n, las intrucciones y los datos del autor.
			Data Informaci贸n: En esta secci贸n se podr谩 cargar el archivo .las que contenga el registro a analizar.
			Data An谩lisis: Presenta un r谩pido an谩lisis estad铆stico de los datos disponibles y se definen las zonas de inter茅s del registro.
			Data Visualizaci贸n: Se visualizan los graficos generados con la informacion proporcinada.
			""")
	with st.expander("Informaci贸n del autor"):
		st.info("Nombre: Diego Ismael Tejena Soledispa, Ingeniero de Petr贸leos, correo: deigo13tejena@gmail.com, celular: 0984133607")
archivo_las = st.sidebar.file_uploader("Cargar archivo .LAS" , key=None)
		
if archivo_las is None:
	st.write("Suba un archivo con extenci贸n .las")

if archivo_las is not None:
	bytes_data = archivo_las.read()
	str_io = StringIO(bytes_data.decode('Windows-1252'))
	las_file = lasio.read(str_io)
	df = las_file.df()
	df['DEPTH'] = df.index


if opciones_inicio == "Data Informaci贸n":
	st.write("Ingrese informaci贸n")
	with st.expander("Data Frame"):
			st.write(df)
			st.header("Lectura del registro")
			lista_columnas = list(df.columns)
			seleccion_columna = st.multiselect("Seleccione columnas del registro", options= lista_columnas)
			df_filtrado = df[seleccion_columna]
			st.write(df_filtrado)
	with st.expander("Datos del registro"):
				pais = las_file.header['Well'].COUNT.value
				campo = las_file.header['Well'].FLD.value
				provincia = las_file.header['Well'].PROV.value
				compania = las_file.header['Well'].COMP.value
				n_columnas = df.shape[1]
				n_filas = df.shape[0]
				profundidad_min = df.index.values[0]
				profundidad_max = df.index.values[-1]
				st.write("Pa铆s:",pais)
				st.write("Campo:",campo)
				st.write("Provincia:",provincia)
				st.write("Compa帽铆a:",compania)
				st.write("Este registro fue medido desde una profundidad de :", profundidad_min , "[ft]")
				st.write("Este registro fue medido hasta una profundidad de :", profundidad_max , "[ft]")
				st.write("n煤mero de columnas",n_columnas)
				st.write("n煤mero de filas",n_filas)
	
if opciones_inicio == "Data Analisis":
	with st.expander("Estad铆sticas"):
		df_estadisticas = df.describe()
		st.write(df_estadisticas)
	with st.expander("Zonas de inter茅s"):
		columna1,columna2=st.columns(2)
		with columna1:
			limite_superior_z1=st.number_input("Ingrese el l铆mite superior zona 1",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z1=st.number_input("Ingrese el l铆mite inferior zona 1",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_1 = df[limite_superior_z1:limite_inferior_z1]
			st.header("Zona 1")
			st.write(df_zona_1)
		with columna2:
			limite_superior_z2=st.number_input("Ingrese el l铆mite superior zona 2",min_value=0.00,max_value=15000.00,value=10000.00)
			limite_inferior_z2=st.number_input("Ingrese el l铆mite inferior zona 2",min_value=0.00,max_value=15000.00,value=10500.00)
			df_zona_2 = df[limite_superior_z2:limite_inferior_z2]
			st.header("Zona 2")
			st.write(df_zona_2)
if opciones_inicio == "Data Visualizacion":
	lista_columnas = list(df.columns)
	seleccion_columnas = st.selectbox("Seleccione las columnas del registro",options=lista_columnas)
	grafico1= alt.Chart(df).mark_line().encode(x="DEPTH",y=seleccion_columnas)
	st.altair_chart(grafico1)
