import os
import stripe
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==============================
# CONFIGURACIÓN
# ==============================
STRIPE_API_KEY = "YOUR_API_KEY_HERE"
YEAR = datetime.now().year
EXPORT_PATH = Path(f"./IVA_{YEAR}")
stripe.api_key = STRIPE_API_KEY

# ==============================
# FUNCIONES
# ==============================

def get_all_invoices(year):
    start = int(datetime(year, 1, 1).timestamp())
    end = int(datetime(year + 1, 1, 1).timestamp())

    invoices = []
    starting_after = None
    while True:
        response = stripe.Invoice.list(
            created={"gte": start, "lt": end},
            limit=100,
            starting_after=starting_after,
            expand=["data.customer"]
        )
        invoices.extend(response["data"])
        if not response["has_more"]:
            break
        starting_after = invoices[-1]["id"]
    return invoices

def save_invoice_pdf(invoice, folder):
    pdf_url = invoice.get("invoice_pdf")
    filename = invoice.get("number", f"no_num_{invoice['id']}") + ".pdf"
    filepath = folder / filename

    if filepath.exists():
        print(f"🟡 Factura ya existe, se omite: {filename}")
        return

    if pdf_url:
        import requests
        r = requests.get(pdf_url)
        with open(filepath, "wb") as f:
            f.write(r.content)

def get_quarter(month):
    return (month - 1) // 3 + 1

def generate_excel(data, pathbase, period_name):
    excel_path = pathbase / f"{period_name}.xlsx"
    csv_path   = pathbase / f"{period_name}.csv"

    if not excel_path.exists():
        data.to_excel(excel_path, index=False)
    else:
        print(f"🟡 Ya existe: {excel_path.name}, se omite.")

    if not csv_path.exists():
        data.to_csv(csv_path, index=False)
    else:
        print(f"🟡 Ya existe: {csv_path.name}, se omite.")

# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================
def main():
    EXPORT_PATH.mkdir(parents=True, exist_ok=True)

    all_invoices = get_all_invoices(YEAR)
    registros = []

    for inv in all_invoices:
        if inv.get("status") in ["draft", "void"]:
            continue

        date = datetime.fromtimestamp(inv["created"])
        mes = date.strftime("%m")
        trimestre = f"T{get_quarter(date.month)}"
        cliente = (
            inv.get("customer_name")
            or (inv.get("customer", {}).get("name") if isinstance(inv.get("customer"), dict) else None)
            or "Desconocido"
        )
        total = inv.get("amount_paid", 0) / 100

        # Carpeta para PDFs
        pdf_folder = EXPORT_PATH / str(YEAR) / trimestre / mes / "facturas_pdf"
        pdf_folder.mkdir(parents=True, exist_ok=True)

        if inv.get("invoice_pdf"):
            save_invoice_pdf(inv, pdf_folder)

        registros.append({
            "Fecha": date.strftime("%Y-%m-%d %H:%M:%S"),
            "Cliente": cliente,
            "Número": inv.get("number", ""),
            "Mes": mes,
            "Trimestre": trimestre,
            "Total €": total,
        })

    df = pd.DataFrame(registros)
    if df.empty:
        print("❌ No se encontraron facturas válidas o el DataFrame está vacío.")
        return
    else:
        print("✅ Facturas encontradas:", len(df))
        print("🧾 Columnas disponibles:", df.columns.tolist())
        print(df.head())

    # Exportar por mes
    for mes in df["Mes"].unique():
        mes_num = int(mes)
        trimestre_actual = f"T{get_quarter(mes_num)}"
        path = EXPORT_PATH / str(YEAR) / trimestre_actual / mes / "resumen_excel"
        path.mkdir(parents=True, exist_ok=True)
        df_mes = df[df["Mes"] == mes]
        generate_excel(df_mes, path, f"{YEAR}_MES_{mes}")

    # Exportar por trimestre
    for t in df["Trimestre"].unique():
        path = EXPORT_PATH / str(YEAR) / t / "resumen_excel"
        path.mkdir(parents=True, exist_ok=True)
        df_t = df[df["Trimestre"] == t]
        generate_excel(df_t, path, f"{YEAR}_TRIMESTRE_{t}")


    # Exportar total anual
    path = EXPORT_PATH / str(YEAR) / "resumen_excel"
    path.mkdir(parents=True, exist_ok=True)
    generate_excel(df, path, f"{YEAR}_ANUAL")

    print(f"✅ Todo exportado en: {EXPORT_PATH}")

# ==============================
# EJECUTAR
# ==============================
if __name__ == "__main__":
    main()
