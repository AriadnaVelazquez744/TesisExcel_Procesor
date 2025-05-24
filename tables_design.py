#tables_design.py

from rich.console import Console
from rich.table import Table

def print_rich_pivot_table(df, title="Horarios del profesor"):
    console = Console()
    table = Table(title=title, show_lines=True)
    table.add_column("Fecha", style="bold cyan")
    for col in df.columns:
        table.add_column(str(col), style="magenta", overflow="fold")
    for idx, row in df.iterrows():
        table.add_row(str(idx), *[str(x) for x in row])
    console.print(table)

def print_rich_df_preview(df, title="Vista previa del archivo procesado"):
    console = Console()
    table = Table(title=title, show_lines=True)
    for col in df.columns:
        table.add_column(str(col), style="bold green", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

def print_rich_query_results(df, title="Resultados de la consulta"):
    console = Console()
    table = Table(title=title, show_lines=True)
    for col in df.columns:
        table.add_column(str(col), style="bold yellow", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

def print_rich_sql_results(df, title="Resultados SQL"):
    console = Console()
    table = Table(title=title, show_lines=True)
    for col in df.columns:
        table.add_column(str(col), style="bold blue", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)