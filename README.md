# TesisExcel Processor 🎓📊

Sistema de Gestión de Defensas de Tesis Universitarias

---

## 📄 Descripción

Este proyecto permite gestionar, consultar y visualizar calendarios de defensas de tesis universitarias a partir de archivos Excel. Ofrece una interfaz de consola avanzada y una interfaz web (Streamlit), facilitando la importación, consulta, análisis y exportación de datos de defensas.

---

## ✨ Características

- 📥 **Procesamiento de archivos Excel**: Importa y normaliza calendarios de defensas.
- 🗄️ **Base de datos SQLite**: Almacena la información usando SQLAlchemy.
- 🔎 **Consultas avanzadas**: Filtra por fecha, estudiante, tutor, oponente, lugar, y más.
- 🖥️ **Visualización en consola**: Tablas coloridas y autoajustables usando rich
- 🌐 **Interfaz web**: Visualización y gestión vía Streamlit.
- 📤 **Exportación**: Resultados exportables a CSV.

---

## 🐍 Requisitos

- 🐍 Python >= 3.8
- 🐧 Linux (recomendado)
- Paquetes: ver `pyproject.toml` o instalar con pip (ver abajo)

---

## ⚙️ Instalación

1. 🛠️ Clona el repositorio:

   ```bash
   git clone https://github.com/LiaLopezRosales/TesisExcel_Procesor.git
   cd tesisexcel-procesor
   ```

2. 🛠️ Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```
   
   O usando pyproject.toml:

   ```bash
   pip install .
   ```

---

## 💻 Uso en Consola

▶️ **Ejecuta la aplicación principal:**

```bash
python consola_app.py
```

**Funcionalidades principales:**

- Procesar archivo Excel y cargarlo a la base de datos.
- Consultar defensas por filtros.
- Realizar consultas SQL personalizadas (solo SELECT).
- Exportar resultados a CSV.
- Abrir la base de datos en DB Browser:
  
    ``` bash  
    ./OpenBrowser.sh defensas.db
    ```

**Pasos de uso**
1. Procesar archivo Excel

- Seleccione opción 1
- Ingrese ruta del archivo Excel
- Vista previa de datos procesados
- Confirme guardado en base de datos
- Elija nombre del archivo .db

2. Consultar defensas
   
- Seleccione opción 2
- Seleccione filtro
- Ingrese parámetro requerido

  2.1. Filtros disponibles:

   - Por fecha (YYYY-MM-DD)
   - Por estudiante (búsqueda parcial)
   - Por profesor (cualquier rol, tutor, oponente, horario)
   - Por lugar

3. Consultas SQL personalizadas

- Seleccione opción 3
- Ingresar consulta SQL respetando las restricciones que se mencionan
- Exportar a CSV si se desea

---

## 🌐 Uso en Interfaz Web (GUI)

▶️ **Ejecuta la app Streamlit:**

```bash  
streamlit run gui.py
```

- Sube archivos Excel, filtra y explora los datos desde el navegador.

---

## 🗂️ Estructura del Proyecto

- `consola_app.py`: Aplicación de consola.
- `gui.py`: Interfaz web (Streamlit).
- `excel_processor.py`: Procesamiento y normalización de archivos Excel.
- `database.py`: Modelo y utilidades de base de datos.
- `tables_design.py`: Tablas coloridas en consola con rich.
- `OpenBrowser.sh`: Script para abrir la base de datos en DB Browser.
- `pyproject.toml`: Dependencias y metadatos del proyecto.
