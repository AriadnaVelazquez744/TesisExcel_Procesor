# consola_app.py
import pandas as pd
import re
import numpy as np
import os
import subprocess
from pathlib import Path
from excel_processor import procesar_excel
from database import crear_tabla, DefensaTesis
from sqlalchemy import create_engine, Date, Time, String, text
from tabulate import tabulate
import tables_design as tb

class AplicacionConsola:
    def __init__(self):
        self.engine = create_engine('sqlite:///defensas.db')
        crear_tabla(self.engine)
        self.df = None
        
    def mostrar_menu_principal(self):
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Procesar archivo Excel")
        print("2. Consultar defensas")
        print("3. Consulta SQL personalizada")
        print("4. Modificar base de datos (DB Browser)")  # Nueva opción
        print("5. Salir")
        return input("Seleccione una opción: ")
    
    def horarios_libres_profesor(self):
        print("\n=== HORARIOS LIBRES POR PROFESOR ===")
        nombre_prof = input("Ingrese nombre del profesor: ").strip()

        # Consulta para obtener las fechas donde participa el profesor y todas las horas posibles del sistema
        query = """
        WITH dias_profesor AS (
            SELECT DISTINCT fecha 
            FROM defensas_tesis 
            WHERE 
                tutores LIKE :profesor OR
                presidente LIKE :profesor OR
                miembro_1 LIKE :profesor OR
                miembro_2 LIKE :profesor OR
                oponente LIKE :profesor
        ),
        horas_ocupadas AS (
            SELECT 
                fecha,
                substr(hora, 1, 5) AS hora
            FROM defensas_tesis 
            WHERE 
                tutores LIKE :profesor OR
                presidente LIKE :profesor OR
                miembro_1 LIKE :profesor OR
                miembro_2 LIKE :profesor OR
                oponente LIKE :profesor
        ),
        todas_horas AS (
            SELECT DISTINCT substr(hora,1,5) AS hora
            FROM defensas_tesis
        )
        SELECT 
            dp.fecha AS Fecha,
            th.hora AS Hora,
            CASE WHEN ho.hora IS NULL THEN 1 ELSE 0 END AS Libre
        FROM dias_profesor dp
        CROSS JOIN todas_horas th
        LEFT JOIN horas_ocupadas ho 
            ON dp.fecha = ho.fecha 
            AND th.hora = ho.hora
        ORDER BY dp.fecha, th.hora;
        """

        try:
            with self.engine.connect() as conn:
                params = {'profesor': f'%{nombre_prof}%'}
                resultados = pd.read_sql(text(query), conn, params=params)

                if not resultados.empty:
                    # Formatear fecha a dd/mm/YYYY
                    resultados['Fecha'] = pd.to_datetime(resultados['Fecha']).dt.strftime('%d/%m/%Y')
                    # Asignar 🟢 Libre o 🔴 Ocupado
                    resultados['Estado'] = np.where(resultados['Libre'] == 1, '🟢 Libre', '🔴 Ocupado')

                    # Obtener lista dinámica de horas (ordenada)
                    horas_unicas = sorted(resultados['Hora'].unique())

                    # Crear tabla pivote usando las horas dinámicas
                    tabla_pivote = resultados.pivot_table(
                        index='Fecha',
                        columns='Hora',
                        values='Estado',
                        aggfunc='first',
                        fill_value='🔴 Ocupado'
                    ).reindex(columns=horas_unicas)

                    # Mostrar la tabla pivote
                    print(f"\n                    📅 Horarios del profesor {nombre_prof}                     ")
                    print(tabla_pivote.to_string())

                    # Calcular estadísticas
                    libres = resultados[resultados['Libre'] == 1]
                    total_libres = len(libres)
                    horas_por_dia = libres.groupby('Fecha').size()

                    print(f"\n📊 Estadísticas:")
                    print(f"- Total de horas libres: {total_libres}")
                    print(f"- Horas libres por día:\n{horas_por_dia.to_string()}")

                else:
                    print("\n⚠️ El profesor no tiene defensas registradas en el sistema.")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


    def procesar_archivo(self, ruta_archivo):
        try:
            self.df = procesar_excel(ruta_archivo)
            print("\n✅ Archivo procesado correctamente")
            tb.print_rich_df_preview(self.df.head(3), title="Vista previa del archivo procesado")

            guardar = input("\n¿Desea guardar en base de datos? (s/n): ").lower()
            if guardar == 's':
                self.guardar_en_bd()  # Llamar al método modificado
                
        except Exception as e:
            print(f"\n❌ Error procesando archivo: {str(e)}")

    def guardar_en_bd(self):
        while True:
            nombre_archivo = input("\nNombre del archivo de base de datos (sin extensión .db): ").strip()
            if not nombre_archivo:
                print("❌ Debe ingresar un nombre válido")
                continue
                
            nombre_archivo += ".db"
            
            if os.path.exists(nombre_archivo):
                print(f"\n⚠️ ¡Atención! El archivo '{nombre_archivo}' ya existe.")
                confirmar = input("¿Desea sobrescribirlo? (s/n): ").lower()
                if confirmar != 's':
                    print("Operación cancelada.")
                    return
                    
            try:
                # Crear motor dinámico con el nombre proporcionado
                self.engine = create_engine(f'sqlite:///{nombre_archivo}')
                crear_tabla(self.engine)
                
                # Convertir tipos y guardar
                self.df['fecha'] = pd.to_datetime(self.df['fecha']).dt.date
                self.df['hora'] = self.df['hora'].astype(str).str.slice(0, 5)
                
                with self.engine.begin() as conn:
                    self.df.to_sql(
                        name='defensas_tesis',
                        con=conn,
                        if_exists='replace',
                        index=False,
                        dtype={
                            'fecha': Date(),
                            'hora': String(5),
                            'lugar': String(100)
                        }
                    )
                print(f"\n✅ Datos guardados exitosamente en: {nombre_archivo}")
                break
                
            except Exception as e:
                print(f"\n❌ Error al guardar: {str(e)}")
                reintentar = input("¿Desea intentar con otro nombre? (s/n): ").lower()
                if reintentar != 's':
                    print("Operación cancelada.")
                    break

    def mostrar_filtros(self):
        print("\n=== FILTROS DISPONIBLES ===")
        print("1. Por fecha")
        print("2. Por estudiante")
        print("3. Por tutor")
        print("4. Por oponente")
        print("5. Por lugar")
        print("6. Por profesor (cualquier rol)")  
        print("7. Horarios libres por profesor")  # Nueva opción
        print("8. Volver al menú principal")
        return input("Seleccione filtro: ")

    def ejecutar_consulta(self, consulta_sql):
        try:
            with self.engine.connect() as conn:
                resultados = pd.read_sql_query(consulta_sql, conn)
                if not resultados.empty:
                    # Resaltar coincidencias
                    # resultados = resultados.map(lambda x: f"\033[93m{x}\033[0m" if isinstance(x,str) and any(rol in x for rol in ['tutor','presidente','miembro','oponente']) else x)
                    
                    # print(tabulate(
                    #     resultados[['fecha', 'estudiante', 'tutores', 'presidente', 
                    #             'miembro_1', 'miembro_2', 'oponente', 'lugar']],
                    #     headers=['Fecha', 'Estudiante', 'Tutores', 'Presidente', 
                    #         'Miembro 1', 'Miembro 2', 'Oponente', 'Lugar'],
                    #     tablefmt='fancy_grid',
                    #     showindex=False
                    # ))
                    tb.print_rich_query_results(resultados[['fecha', 'estudiante', 'tutores', 'presidente', 
                        'miembro_1', 'miembro_2', 'oponente', 'lugar']], title="Resultados de la consulta")
                    print(f"\n📊 Total de defensas encontradas: {len(resultados)}")
                else:
                    print("\n⚠️ No se encontraron defensas para este profesor")
                    
        except Exception as e:
            print(f"\n❌ Error en la consulta: {str(e)}")
            
    def generar_query_profesor(nombre_profesor):
        return f"""
        SELECT * FROM defensas_tesis 
        WHERE 
            tutores LIKE '%{nombre_profesor}%' OR
            presidente LIKE '%{nombre_profesor}%' OR
            miembro_1 LIKE '%{nombre_profesor}%' OR
            miembro_2 LIKE '%{nombre_profesor}%' OR
            oponente LIKE '%{nombre_profesor}%'
        ORDER BY fecha, hora
        """     
    def menu_consultas(self):
        def generar_query_profesor(nombre_profesor):
            return f"""
            SELECT * FROM defensas_tesis 
            WHERE 
                tutores LIKE '%{nombre_profesor}%' OR
                presidente LIKE '%{nombre_profesor}%' OR
                miembro_1 LIKE '%{nombre_profesor}%' OR
                miembro_2 LIKE '%{nombre_profesor}%' OR
                oponente LIKE '%{nombre_profesor}%'
            ORDER BY fecha, hora
            """     
        while True:
            opcion = self.mostrar_filtros()
            
            if opcion == '8':
                break
                
            campo, valor = None, None
            
            if opcion == '1':
                campo = 'fecha'
                valor = input("Ingrese fecha (YYYY-MM-DD): ")
            elif opcion == '2':
                campo = 'estudiante'
                valor = input("Ingrese nombre estudiante: ").strip()
            elif opcion == '3':
                campo = 'tutores'
                valor = input("Ingrese nombre tutor: ").strip()
            elif opcion == '4':
                campo = 'oponente'
                valor = input("Ingrese nombre oponente: ").strip()
            elif opcion == '5':
                campo = 'lugar'
                valor = input("Ingrese lugar: ").strip()
            elif opcion == '6': 
                nombre_prof = input("Ingrese nombre del profesor: ").strip()
                consulta = generar_query_profesor(nombre_prof)
                self.ejecutar_consulta(consulta)
                continue
            elif opcion == '7':  
                self.horarios_libres_profesor()
                continue
            else:
                print("\n⚠️ Opción no válida")
                continue
                
            consulta = f"SELECT * FROM defensas_tesis WHERE {campo} LIKE '%{valor}%'"
            self.ejecutar_consulta(consulta)

    
    def consulta_personalizada(self):
        print("\n=== CONSULTA SQL PERSONALIZADA ===")
        print("Normas de seguridad:")
        print("- Solo se permiten consultas SELECT")
        print("- No se permite múltiples statements")
        print("- Límite de 1000 registros por consulta")
        
        consulta = input("\nIngrese su consulta SQL (o 'exit' para salir):\n").strip()
        
        if consulta.lower() == 'exit':
            return
        
        # Validación de seguridad
        if not consulta.upper().startswith("SELECT"):
            print("\n❌ Error: Solo se permiten consultas SELECT")
            return
            
        if ';' in consulta:
            print("\n❌ Error: No se permiten múltiples statements")
            return
            
        try:
            with self.engine.connect() as conn:
                # Ejecutar con límite de resultados
                resultados = pd.read_sql_query(
                    sql=text(consulta),
                    con=conn,
                    params={},
                    coerce_float=False,
                    chunksize=None
                ).head(1000)
                
                if not resultados.empty:
                    print(f"\n🔍 Resultados ({len(resultados)} registros):")
                    # print(tabulate(resultados, headers='keys', tablefmt='psql', showindex=False))
                    tb.print_rich_sql_results(resultados, title="Resultados SQL")

                    # Opción para guardar resultados
                    guardar = input("\n¿Desea exportar a CSV? (s/n): ").lower()
                    if guardar == 's':
                        nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
                        resultados.to_csv(f"{nombre_archivo}.csv", index=False)
                        print(f"✅ Datos guardados en {nombre_archivo}.csv")
                else:
                    print("\nℹ️ La consulta no devolvió resultados")
                    
        except Exception as e:
            print(f"\n❌ Error en la consulta: {str(e)}")
            # Mostrar sugerencias para errores comunes
            if "no such table" in str(e):
                print("\nℹ️ Tablas disponibles: defensas_tesis")
            elif "no such column" in str(e):
                print("\nℹ️ Columnas disponibles: fecha, estudiante, tutores, presidente, miembro_1, miembro_2, oponente, hora, lugar")

    def ejecutar(self):
        print("=== SISTEMA DE GESTIÓN DE DEFENSAS ===")
        
        while True:
            opcion = self.mostrar_menu_principal()
            
            if opcion == '1':
                ruta = input("\nIngrese la ruta del archivo Excel: ").strip()
                self.procesar_archivo(ruta)
            elif opcion == '2':
                self.menu_consultas()
            elif opcion == '3':  # Nueva opción
                self.consulta_personalizada()
            elif opcion == '4':
                print("\n Ejecutar desde terminal: ./OpenBrowser.sh database.db ( si es la primera vez ejecute antes: chmod +x abrir_db_browser.sh) ")
            elif opcion == '5':
                print("\n👋 ¡Hasta pronto!")
                break
            else:
                print("\n⚠️ Opción no válida, intente nuevamente")

if __name__ == "__main__":
    app = AplicacionConsola()
    app.ejecutar()