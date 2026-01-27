#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV to Excel Converter for SEO Manager
Converts unified CSV file to Excel with 6 separate sheets.

Usage:
    python csv_to_excel.py <input_csv_file>

Example:
    python csv_to_excel.py SEOManager_CLI001_20251117_143025.csv

Author: SEO Manager Team
Version: 1.0.0
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

def convert_csv_to_excel(csv_file: str) -> str:
    """
    Convert unified CSV to Excel with separate sheets.

    Args:
        csv_file: Path to input CSV file

    Returns:
        Path to generated Excel file
    """
    print("\n" + "=" * 80)
    print("  CSV TO EXCEL CONVERTER - SEO Manager")
    print("=" * 80 + "\n")

    # Validate input file
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"  ✗ Error: Archivo no encontrado: {csv_file}")
        sys.exit(1)

    print(f"  📄 Archivo CSV: {csv_file}")

    # Read CSV
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"  ✓ CSV leído correctamente: {len(df)} filas, {len(df.columns)} columnas")
    except Exception as e:
        print(f"  ✗ Error leyendo CSV: {e}")
        sys.exit(1)

    # Check if 'hoja' column exists
    if 'hoja' not in df.columns:
        print("  ✗ Error: El CSV no tiene la columna 'hoja'")
        print("  Este script solo funciona con archivos generados por SEO Manager")
        sys.exit(1)

    # Generate Excel filename
    excel_file = csv_path.stem + '.xlsx'
    excel_path = csv_path.parent / excel_file

    print(f"\n  📊 Generando Excel: {excel_file}")
    print(f"  📁 Ruta completa: {excel_path}\n")

    # Get unique sheet names
    sheet_names = df['hoja'].unique()
    print(f"  Hojas detectadas: {len(sheet_names)}")
    for sheet_name in sheet_names:
        count = len(df[df['hoja'] == sheet_name])
        print(f"    - {sheet_name}: {count} filas")

    # Create Excel with separate sheets
    try:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for sheet_name in sheet_names:
                # Filter data for this sheet
                sheet_data = df[df['hoja'] == sheet_name].copy()

                # Remove 'hoja' column from output (already separated by sheet)
                if 'hoja' in sheet_data.columns:
                    sheet_data = sheet_data.drop(columns=['hoja'])

                # Map sheet names to friendly names
                friendly_names = {
                    'brief': 'Brief',
                    'google_business_profile': 'Google Business Profile',
                    'indicadores_seo': 'Indicadores SEO',
                    'catalogo_woocommerce': 'Catálogo WooCommerce',
                    'optimizacion_seo': 'Optimización SEO',
                    'link_building': 'Link Building'
                }

                output_sheet_name = friendly_names.get(sheet_name, sheet_name)

                # Write to Excel
                sheet_data.to_excel(writer, sheet_name=output_sheet_name, index=False)

                # Auto-adjust column widths
                worksheet = writer.sheets[output_sheet_name]
                for idx, col in enumerate(sheet_data.columns):
                    max_length = max(
                        sheet_data[col].astype(str).apply(len).max(),
                        len(str(col))
                    )
                    # Cap at 50 characters
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[chr(65 + idx)].width = adjusted_width

        print(f"\n  ✓ Excel generado exitosamente: {excel_file}")
        print(f"  📊 {len(sheet_names)} hojas creadas")
        print(f"  💾 Tamaño: {excel_path.stat().st_size / 1024:.2f} KB\n")

        return str(excel_path)

    except Exception as e:
        print(f"\n  ✗ Error generando Excel: {e}")
        sys.exit(1)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("\n" + "=" * 80)
        print("  USO DEL SCRIPT")
        print("=" * 80 + "\n")
        print("  python csv_to_excel.py <archivo_csv>\n")
        print("  Ejemplo:")
        print("    python csv_to_excel.py SEOManager_CLI001_20251117_143025.csv\n")
        sys.exit(1)

    csv_file = sys.argv[1]
    excel_file = convert_csv_to_excel(csv_file)

    print("  ✨ Conversión completada exitosamente!\n")
    print(f"  Puedes abrir el archivo Excel:")
    print(f"  {excel_file}\n")

if __name__ == "__main__":
    main()
