# Seguridad y Protección de Datos

Este documento describe brevemente los riesgos potenciales asociados con la
aplicación de la prueba técnica y propone medidas de mitigación. Aunque el
proyecto maneja datos públicos y no tiene por qué almacenar información
sensible, adoptar buenas prácticas de seguridad es fundamental.

## Riesgos Identificados

1. **Exposición de datos sensibles**  
   Aunque las fuentes públicas suelen contener datos no sensibles, es posible
   que algunos registros incluyan nombres, direcciones de correo electrónico o
   identificadores únicos. Almacenar tales datos sin control puede suponer un
   riesgo de reidentificación o de uso indebido.

2. **Acceso no autorizado al endpoint de refresco**  
   El endpoint `/admin/refresh` permite re‑ejecutar el proceso ETL y, en
   entornos productivos, podría desencadenar cargas elevadas o ser un vector de
   ataque de denegación de servicio si no se protege adecuadamente.

3. **Filtrado inadecuado en la API**  
   Las consultas de búsqueda que no escaparan correctamente las cadenas
   introducidas por el usuario podrían dar lugar a ataques de inyección de SQL
   si se usaran construcciones de bajo nivel. En este proyecto se utilizan
   expresiones de SQLAlchemy que mitigan este riesgo.

4. **Exposición de secretos en el repositorio**  
   Variables como `API_KEY` u `OPENAI_API_KEY` no deben incluirse en el
   código fuente ni en los commits. Compartir el repositorio sin filtrar los
   secretos podría comprometer servicios externos.

## Medidas de Mitigación

1. **Minimización y anonimización**  
   Se evita almacenar datos personales que no sean necesarios para los
   objetivos del proyecto. Si se identifican campos sensibles en los datos de
   origen, pueden anonimizarse (p. ej., ofuscando parcialmente nombres o
   direcciones).

2. **Protección del endpoint de refresco**  
   El endpoint `/admin/refresh` requiere un encabezado `X-API-KEY` cuyo valor
   se define en la variable de entorno `API_KEY`. Para mayor robustez en
   entornos reales, conviene limitar la frecuencia de llamadas y registrar
   intentos fallidos para detectar ataques.

3. **Uso de ORMs y consultas parametrizadas**  
   Todas las interacciones con la base de datos se realizan mediante SQLAlchemy,
   que construye consultas parametrizadas y evita la inyección de SQL. No se
   interpolan cadenas directamente en sentencias SQL.

4. **Gestión de secretos**  
   Las claves y credenciales se definen en un archivo `.env` (no incluido en
   el repositorio) y se cargan a través de variables de entorno. Esto permite
   que cada entorno tenga sus propios secretos sin exponerlos públicamente.

5. **CORS y restricciones de origen**  
   En caso de desplegar la API en internet, se debe configurar CORS para
   permitir únicamente solicitudes desde dominios autorizados. Esto reduce el
   riesgo de que aplicaciones externas abusen de la API.

6. **Registro y monitorización**  
   Implementar un sistema de logs centralizado que registre accesos,
   parámetros de consulta y errores ayuda a detectar comportamientos anómalos
   y a responder rápidamente ante incidentes.

7. **Pruebas y actualización periódica**  
   Revisar periódicamente las dependencias y aplicar actualizaciones de
   seguridad. Incluir pruebas automatizadas que validen los controles de
   acceso y la sanitización de entradas.