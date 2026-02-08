# The Smart Feedback API

##  Decisiones Técnicas

### Elección del modelo
Se utilizó un modelo basado en **RoBERTa** para el análisis de sentimiento debido a que:
- Es un modelo preentrenado (twitter) ampliamente utilizado en tareas de NLP.
- Presenta buen rendimiento en clasificación de texto sin necesidad de reentrenar.
- Permite obtener resultados confiables usando inferencia directa.
- Está disponible fácilmente a través de la librería `transformers` de Hugging Face.
---
### Modularizado

Las validaciones de archivos y estructura de CSV se separaron en un módulo `utils` para:

- Evitar lógica duplicada
- Mantener funciones pequeñas y reutilizables
- Mejorar la legibilidad del código principal

Esto para mantener el código más limpio y organizado.

---

### Uso de CSV como formato de entrada

Originalmente, el archivo reviews.csv que se me proporcionó parecía tener un propósito meramente ilustrativo. Por esta razón, decidí implementar una ruta que permita la carga de archivos CSV con múltiples mensajes para análisis. Esta decisión mejora la funcionalidad de la aplicación, ya que no solo permite analizar un mensaje aislado, sino que también facilita el análisis de múltiples mensajes a la vez, haciendo la aplicación más robusta y escalable.
La ruta devuelve los datos paginados junto con la cantidad de paginas y la cantidad de datos totales utilizando guardado de archivos temporales.

---

### Entorno virtual (`venv`)

Se utiliza un entorno virtual para manejar las dependencias del proyecto de forma aislada.
Esto evita problemas con librerías instaladas globalmente en la máquina.

El entorno virtual no forma parte del repositorio y debe crearse localmente.

---

## Iniciar el proyecto

Primero se recomienda crear un entorno virtual para aislar las dependencias del proyecto:
```bash
python -m venv venv
```

Activar el entorno virtual:

**En Windows:**
```bash
venv\Scripts\activate
```

**En Linux / Mac:**
```bash
source venv/bin/activate
```

Con el entorno virtual activo, instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

Una vez instaladas las dependencias, levantar el servidor con Uvicorn:
```bash
uvicorn api.main:app --reload
```

La API quedará disponible en:
```
http://127.0.0.1:8000
```