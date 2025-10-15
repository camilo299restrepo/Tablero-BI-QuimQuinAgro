# BI - Tablero Financiero: QuimQuinAgro

Este proyecto desarrolla un tablero interactivo en Python para analizar la información financiera y contable de la empresa QuimQuinAgro, como parte del Reto 2 de Business Intelligence.  

El tablero permite realizar consultas dinámicas sobre las bases de datos de distintos años, facilitando la toma de decisiones mediante visualizaciones y análisis automatizados.

---

## Tecnologías utilizadas

- Python 3.13  
- Pandas — Manejo y análisis de datos  
- SQLite3 — Base de datos (contabilidad.db)  
- Matplotlib / Plotly — Visualización de datos  
- Streamlit o Dash — Interfaz del tablero  
- Jupyter o Spyder — Entorno de desarrollo  

---

## Estructura del proyecto

├── app.py # Script principal del tablero
├── contabilidad.db # Base de datos con tablas cxc2020–cxc2025
├── SQlib.py # Funciones auxiliares para consultas SQL
├── requirements.txt # Librerías necesarias
└── README.md # Descripción del proyecto


---

## Funcionalidades principales

- Consultas SQL automáticas integradas en Python  
- Visualización de indicadores por socio y año  
- Comparación de ingresos y tendencias  
- Filtros interactivos para exploración de datos  
- Exportación de resultados a CSV  
- Interfaz amigable y eficiente  

---

## Ejemplo de consultas

- **Consulta 1:** Totales de Ingresos y Egresos por Mes
- **Consulta 2:** Top 10 egresos
- **Consulta 3:** Comparativo histórico de ingresos  
- **Consulta 4:** Ingresos por Socio (CXC)

---

## Cómo ejecutar el proyecto

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/tu-usuario/BI-Reto2-QuimQuinAgro.git
2. pip install -r requirements.txt
3. Ejecutar la aplicación:
python app.py
4. Ejecutar:
streamlit run app.py

## Resultados esperados

El proyecto ofrece un tablero de control claro y funcional que:

- Centraliza información de múltiples años contables.

- Permite detectar patrones y anomalías.

- Mejora la eficiencia en la gestión de cuentas por cobrar.

- Sirve como herramienta base para decisiones financieras.

Autor

Camilo Restrepo Espinal
Proyecto académico — Reto 2: Business Intelligence - QuimQuinAgro
Octubre 2025


