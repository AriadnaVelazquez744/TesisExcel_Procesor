import streamlit as st
import pandas as pd
import traceback
import re
from sqlalchemy import create_engine, Date, Time, String
from sqlalchemy.orm import sessionmaker
from database import crear_tabla
from excel_processor import procesar_excel

# Configuración inicial obligatoria
st.set_page_config(
    page_title="Gestión de Defensas",
    page_icon="🎓",
    layout="wide"
)

# Título siempre visible
st.title("🏛️ Gestión de Defensas de Tesis Universitarias")

# Conexión a DB con verificación
try:
    engine = create_engine('sqlite:///defensas.db')
    crear_tabla(engine)
    st.success("Conexión a base de datos establecida")
except Exception as e:
    st.error(f"Error de conexión a DB: {str(e)}")
    st.stop()

# Widget de carga de archivo
try:
    uploaded_file = st.file_uploader(
        "📤 Sube el archivo Excel de defensas",
        type=["xlsx", "xls"],
        help="El archivo debe tener la estructura oficial de calendarios de defensas"
    )
except Exception as e:
    st.error(f"Error al crear el uploader: {str(e)}")
    st.stop()

# Procesamiento de datos
if uploaded_file:
    
    try:
        df = procesar_excel(uploaded_file)
        
        # Sección de preview
        st.subheader("Previsualización de Datos")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total de defensas", len(df))
            st.write("Primeros registros:")
            st.dataframe(df.head(3))
            
        with col2:
            st.write("Estadísticas:")
            st.json({
                "Fechas únicas": df['fecha'].unique().tolist(),
                "Lugares únicos": df['lugar'].nunique()
            })
            
    except Exception as e:
        st.error(f"Error procesando el archivo: {str(e)}")
        st.code(traceback.format_exc())
        st.stop()
        
if st.button("💾 Guardar en Base de Datos"):
    try:
        # Mantener todo como strings
        df['hora'] = df['hora'].astype(str).str.replace("NaT", "")
        
        # Filtrar valores inválidos
        df['hora'] = df['hora'].apply(
            lambda x: x if re.match(r"\d{2}:\d{2}", str(x)) else None
        )
        
        # Guardar en BD
        with engine.begin() as connection:
            df.to_sql(
                name='defensas_tesis',
                con=connection,
                if_exists='replace',
                index=False,
                dtype={
                    'fecha': Date(),
                    'hora': String(10),
                    'lugar': String(100)
                }
            )
        st.success(f"✅ {len(df)} defensas guardadas!")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.code(traceback.format_exc())


 # Consultas predefinidas
st.sidebar.header("Filtros Avanzados")

# Obtener valores únicos para los filtros
df_completo = pd.read_sql_table('defensas_tesis', engine)
tutores = ["Todos"] + sorted(df_completo['tutores'].dropna().unique().tolist())
oponentes = ["Todos"] + sorted(df_completo['oponente'].dropna().unique().tolist())

# Widgets de filtro
filtro_tutor = st.sidebar.selectbox(
    "Filtrar por tutor:",
    options=tutores,
    index=0
)

filtro_oponente = st.sidebar.selectbox(
    "Filtrar por oponente:",
    options=oponentes,
    index=0
)

# Aplicar filtros a los datos
df_filtrado = df_completo.copy()

if filtro_tutor != "Todos":
    df_filtrado = df_filtrado[df_filtrado['tutores'].str.contains(filtro_tutor, na=False)]

if filtro_oponente != "Todos":
    df_filtrado = df_filtrado[df_filtrado['oponente'] == filtro_oponente]

# Mostrar resultados
st.subheader(f"Defensas Filtradas")
st.write(f"Mostrando: {len(df_filtrado)} resultados")

# Mostrar tabla con nuevos filtros
st.dataframe(
    df_filtrado,
    use_container_width=True,
    column_order=["fecha", "estudiante", "tutores", "oponente", "lugar", "hora"],
    height=600
)

# Modificar el selectbox de consultas
consulta = st.sidebar.selectbox(
    "Consultas predefinidas:",
    options=[
        "Todas las defensas",
        "Defensas por estudiante",
        "Defensas por lugar",
        "Defensas por tutor",
        "Defensas por oponente"
    ]
)

# Actualizar lógica de consultas
if consulta == "Defensas por tutor":
    resultados = pd.read_sql(
        "SELECT tutores, COUNT(*) as total FROM defensas_tesis GROUP BY tutores ORDER BY total DESC", 
        engine
    )
elif consulta == "Defensas por oponente":
    resultados = pd.read_sql(
        "SELECT oponente, COUNT(*) as total FROM defensas_tesis GROUP BY oponente ORDER BY total DESC", 
        engine
    )
          
# Consultas predefinidas
st.sidebar.header("Consultas")
consulta = st.sidebar.selectbox(
    "Seleccionar consulta",
    options=[
        "Próximas defensas por fecha",
        "Defensas por estudiante",
        "Defensas por lugar"
    ]
)

if consulta == "Próximas defensas por fecha":
    resultados = pd.read_sql("SELECT * FROM defensas_tesis ORDER BY fecha, hora", engine)
elif consulta == "Defensas por estudiante":
    resultados = pd.read_sql("SELECT estudiante, fecha, hora, lugar FROM defensas_tesis ORDER BY estudiante", engine)
elif consulta == "Defensas por lugar":
    resultados = pd.read_sql("SELECT lugar, COUNT(*) as total FROM defensas_tesis GROUP BY lugar", engine)

st.subheader(f"Resultados: {consulta}")
st.dataframe(resultados, use_container_width=True)

# Sección de Visualización Completa
st.sidebar.header("Visualización Completa")
mostrar_db = st.sidebar.checkbox("Mostrar toda la base de datos")

if mostrar_db:
    st.subheader("Base de Datos Completa")
    
    # Cargar todos los datos
    try:
        df_completo = pd.read_sql_table('defensas_tesis', engine)
        
        # Mostrar con filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_fecha = st.date_input("Filtrar por fecha", [])
        with col2:
            filtro_lugar = st.selectbox("Filtrar por lugar", ["Todos"] + df_completo['lugar'].unique().tolist())
        
        # Aplicar filtros
        if filtro_fecha:
            df_filtrado = df_completo[df_completo['fecha'].isin(filtro_fecha)]
        else:
            df_filtrado = df_completo
            
        if filtro_lugar != "Todos":
            df_filtrado = df_filtrado[df_filtrado['lugar'] == filtro_lugar]
        
        # Mostrar datos
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            height=600,
            hide_index=True,
            column_order=["fecha", "estudiante", "tutores", "presidente", "lugar", "hora"]
        )
        
        # Botón de descarga
        st.download_button(
            label="Descargar como CSV",
            data=df_filtrado.to_csv(index=False).encode('utf-8'),
            file_name='defensas_completas.csv',
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f"No se pudo cargar la base de datos: {str(e)}")

# Sección de Estadísticas Rápidas
with st.expander("📊 Estadísticas Generales"):
    if 'df_completo' in locals() and not df_completo.empty:
        total_defensas = len(df_completo)
        
        # Manejo seguro de fechas
        fecha_min = df_completo['fecha'].min()
        fecha_max = df_completo['fecha'].max()
        
        # Convertir a texto si son válidas
        str_fecha_min = fecha_min.strftime("%d/%m/%Y") if pd.notnull(fecha_min) else "N/A"
        str_fecha_max = fecha_max.strftime("%d/%m/%Y") if pd.notnull(fecha_max) else "N/A"
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de defensas", total_defensas)
        col2.metric("Primera defensa", str_fecha_min)
        col3.metric("Última defensa", str_fecha_max)
        
        # Filtrar fechas válidas para el gráfico
        df_fechas_validas = df_completo[pd.notnull(df_completo['fecha'])]
        if not df_fechas_validas.empty:
            st.line_chart(df_fechas_validas.set_index('fecha')['hora'].value_counts())
        else:
            st.warning("No hay fechas válidas para mostrar el gráfico")
    else:
        st.warning("Base de datos vacía o no cargada")
        
with st.expander("📊 Estadísticas por Rol"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 5 Tutores**")
        st.bar_chart(df_completo['tutores'].value_counts().head(5))
        
    with col2:
        st.write("**Top 5 Oponentes**")
        st.bar_chart(df_completo['oponente'].value_counts().head(5))
        
st.sidebar.header("Búsqueda Combinada")
busqueda_avanzada = st.sidebar.text_input("Buscar en todos los campos:")

if busqueda_avanzada:
    mask = df_filtrado.apply(
        lambda row: row.astype(str).str.contains(busqueda_avanzada, case=False).any(),
        axis=1
    )
    df_filtrado = df_filtrado[mask]