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
- 📈 **Estadísticas**: Muestra tutores más activos, oponentes frecuentes, distribución por lugar, etc.
- 🖥️ **Visualización en consola**: Tablas coloridas y autoajustables usando rich
- 🌐 **Interfaz web**: Visualización y gestión vía Streamlit.
- 📤 **Exportación**: Resultados exportables a CSV.
- 🛠️ **Edición manual**: Abre la base de datos en DB Browser con un solo comando.

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
   # O usando pyproject.toml:
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
- Ver estadísticas generales.
- Realizar consultas SQL personalizadas (solo SELECT).
- Exportar resultados a CSV.
- Abrir la base de datos en DB Browser:
  
    ``` bash  
    ./OpenBrowser.sh defensas.db
    ```

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
