# 📊 Exportador de Facturas Stripe para Declaración de IVA

Este script permite descargar todas las facturas del año actual desde Stripe, organizarlas por mes y trimestre, guardar los PDF y generar automáticamente resúmenes en Excel y CSV para facilitar la declaración del IVA.

## ✅ Requisitos

- Python 3.7 o superior
- Una clave secreta de Stripe (`sk_live_...`)
- Acceso a tu cuenta de Stripe con permisos de lectura de facturas

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TheAngloacademy/DeclaradorDeIVAStripe.git
   cd DeclaradorDeIVAStripe
