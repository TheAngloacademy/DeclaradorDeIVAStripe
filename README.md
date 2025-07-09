# 📊 Exportador de Facturas Stripe para Declaración de IVA

Este script permite descargar todas las facturas del año actual desde Stripe, organizarlas por mes y trimestre, guardar los PDF y generar automáticamente resúmenes en Excel y CSV para facilitar la declaración del IVA.

## ✅ Requisitos

* Python 3.7 o superior
* Una clave secreta de Stripe (`sk_live_...`)
* Acceso a tu cuenta de Stripe con permisos de lectura de facturas

## 📦 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TheAngloacademy/DeclaradorDeIVAStripe.git
   cd DeclaradorDeIVAStripe
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

## ⚙️ Configuración

Edita la variable `STRIPE_API_KEY` en el script para colocar tu clave secreta de Stripe:

```python
STRIPE_API_KEY = "sk_live_..."
```

## 🚀 Uso

Ejecuta el script con:

```bash
python main.py
```

El script generará automáticamente una carpeta `IVA_2025` (o del año actual), con subcarpetas por trimestre, mes y los archivos PDF y Excel correspondientes.

## 📁 Estructura de salida

```
IVA_2025/
├── 2025/
│   ├── T1/
│   │   ├── 01/
│   │   │   ├── facturas_pdf/
│   │   │   └── resumen_excel/
│   │   └── resumen_excel/
│   └── resumen_excel/
└── ...
```

## 💾 Archivos generados

* Facturas individuales en PDF
* Resúmenes mensuales y trimestrales en `.xlsx` y `.csv`
* Un resumen anual completo
