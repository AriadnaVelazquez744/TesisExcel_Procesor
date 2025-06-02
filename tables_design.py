#tables_design.py

from rich.console import Console
from rich.table import Table

def print_rich_pivot_table(df, title="Horarios del profesor"):
    console = Console()
    table = Table(title=title, title_style="bold italic red", show_lines=True, border_style="green", header_style="bold italic blue", caption="🟢 => Libre    🔴 => Ocupado")
    table.add_column("Fecha", style="bold italic cyan")
    for col in df.columns:
        table.add_column(str(col), style="italic bright_white", overflow="fold")
    for idx, row in df.iterrows():
        table.add_row(str(idx), *[str(x) for x in row])
    console.print(table)

def print_rich_df_preview(df, title="Vista previa del archivo procesado"):
    console = Console()
    table = Table(title=title, title_style="bold italic red", show_lines=True, border_style="dark_blue", header_style="italic bold dark_magenta")
    for col in df.columns:
        table.add_column(str(col), style="italic bright_cyan", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

def print_rich_query_results(df, title="Resultados de la consulta"):
    console = Console()
    table = Table(title=title, title_style="bold italic red", show_lines=True, border_style="green", header_style="italic bold black on dark_green")
    for col in df.columns:
        table.add_column(str(col), style="italic yellow", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)

def print_rich_sql_results(df, title="Resultados SQL"):
    console = Console()
    table = Table(title=title, title_style="bold italic red", show_lines=True, border_style="cyan", header_style="bold italic dark_blue")
    for col in df.columns:
        table.add_column(str(col), style="italic bright_blue", overflow="fold")
    for _, row in df.iterrows():
        table.add_row(*[str(x) for x in row])
    console.print(table)