# E-commerce Predictive Analytics MVP

Sistema de análisis predictivo para comercio electrónico basado en RFM (Recency, Frequency, Monetary) con recomendaciones explicables generadas por IA.

## 🎯 Características

- **Análisis RFM**: Segmentación de clientes basada en comportamiento de compra
- **Predicción de Recompra**: Estimación de fechas óptimas de contacto basada en ciclos de consumo
- **Recomendaciones Explicables**: Razonamiento generado para cada sugerencia
- **Dashboard Interactivo**: Visualización en tiempo real con Streamlit

## 🛠 Stack Tecnológico

### Backend
- **Python 3.11**
- **FastAPI**: API REST
- **SQLModel**: ORM y validación de datos
- **Pandas**: Análisis de datos
- **SQLite**: Base de datos (MVP)

### Frontend
- **Streamlit**: Dashboard interactivo
- **Plotly**: Visualizaciones

## 📦 Instalación

### 1. Configurar entorno virtual

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ejecutar el Dashboard

```bash
# Desde el directorio raíz del proyecto
backend/venv/bin/streamlit run backend/app/dashboard.py
```

El dashboard estará disponible en [http://localhost:8501](http://localhost:8501)

### 3. Generar Datos de Prueba

Una vez en el dashboard, haz clic en el botón **"⚡ Generate Mock Data (Reset DB)"** en la barra lateral para crear datos ficticios.

## 🚀 Uso

### Generar Recomendaciones

El dashboard incluye un flujo completo:

1. **Generación de datos**: Simula 4 años de historial de compras
2. **Análisis RFM**: Calcula métricas por cliente-producto
3. **Motor de recomendaciones**: Identifica ventanas óptimas de contacto
4. **Visualización**: Muestra resultados con gráficos interactivos

### API (Opcional)

```bash
# Ejecutar el servidor FastAPI
cd backend
uvicorn app.main:app --reload
```

Endpoints disponibles:
- `POST /api/ingest/mock`: Generar datos de prueba
- `POST /api/analytics/run`: Ejecutar pipeline de análisis
- `GET /api/recommendations`: Obtener todas las recomendaciones

## 📊 Modelos de Datos

- **Customer**: Información del cliente
- **Product**: Catálogo de productos con ciclos de consumo
- **Order**: Historial de pedidos
- **RFMProfile**: Métricas calculadas por cliente-producto
- **Recommendation**: Recomendaciones de contacto

## 🧪 Verificación

```bash
# Ejecutar script de verificación end-to-end
backend/venv/bin/python backend/verify_system.py
```

## 📝 Notas

- Este es un MVP diseñado para demostración
- Las explicaciones usan un generador mock (integrar Gemini API requiere clave)
- El sistema es **advisory-only**: genera recomendaciones, no automatiza acciones

## 👥 Autor

Desarrollado por Agente IA
