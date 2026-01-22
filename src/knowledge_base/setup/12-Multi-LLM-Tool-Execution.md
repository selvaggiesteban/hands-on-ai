# 12. GuÃ­a de EjecuciÃ³n de Herramientas Multi-LLM

Este documento detalla la arquitectura del sistema para soportar mÃºltiples proveedores de Modelos de Lenguaje Grandes (LLM) y garantizar que cada uno pueda ejecutar herramientas de forma autÃ³noma.

## 1. Arquitectura y DiseÃ±o

El sistema estÃ¡ construido sobre una capa de abstracciÃ³n (`BaseProvider`) que normaliza la interacciÃ³n con diferentes APIs de LLM. El `MultiModelProcessor` actÃºa como un orquestador que selecciona el proveedor configurado y le delega las tareas.

- **`BaseProvider`**: Define un contrato comÃºn con mÃ©todos como `generate`, `validate_key` y `calculate_cost`.
- **Proveedores EspecÃ­ficos**: (`OpenAIProvider`, `GeminiProvider`, `AnthropicProvider`) implementan `BaseProvider` y traducen las llamadas normalizadas a las solicitudes especÃ­ficas de su API.
- **`.env`**: La configuraciÃ³n en este archivo (`AI_PROVIDER`, `AI_MODEL`, `AI_API_KEY`) determina quÃ© proveedor se utiliza en tiempo de ejecuciÃ³n.

## 2. Soporte para EjecuciÃ³n de Herramientas (Tool Calling)

La capacidad de los LLM para solicitar la ejecuciÃ³n de una herramienta (tambiÃ©n conocido como "function calling") es fundamental para la autonomÃ­a. AsÃ­ es como se soporta para cada proveedor:

### a. OpenAI (GPT-4o, o1, etc.)

- **API**: Utiliza el parÃ¡metro `tools` en las llamadas a la API de Chat Completions.
- **ImplementaciÃ³n**: `OpenAIProvider` debe formatear las herramientas disponibles en el formato JSON Schema que OpenAI espera y procesar la respuesta `tool_calls` para invocar la herramienta correspondiente.
- **Estado**: Totalmente soportado y estable.

### b. Google Gemini (Gemini 1.5 Pro, Flash, etc.)

- **API**: Soporta "Function Calling" nativo a travÃ©s del parÃ¡metro `tools`. Es muy similar a la implementaciÃ³n de OpenAI.
- **ImplementaciÃ³n**: `GeminiProvider` se encarga de definir las `FunctionDeclarations` y de interpretar la `FunctionCall` en la respuesta del modelo para su ejecuciÃ³n.
- **Estado**: Totalmente soportado y estable.

### c. Anthropic Claude (Claude 3.5 Sonnet, Opus, etc.)

- **API**: Claude utiliza un sistema basado en XML para el uso de herramientas. Las herramientas se describen en un bloque `<tools>` y el modelo responde con un bloque `<invoke>` cuando desea ejecutar una.
- **ImplementaciÃ³n**: `AnthropicProvider` debe construir el prompt del sistema con las definiciones de herramientas en formato XML y parsear la respuesta para detectar las invocaciones.
- **Estado**: Soportado, aunque la sintaxis puede evolucionar al ser una caracterÃ­stica mÃ¡s reciente en comparaciÃ³n con otros proveedores.

## 3. Flujo de Trabajo AutÃ³nomo

1. **ConfiguraciÃ³n**: Un desarrollador o un pipeline de CI/CD configura el proveedor deseado en el archivo `.env`.
2. **DefiniciÃ³n de Herramientas**: Las herramientas disponibles (ej: `run_shell_command`, `read_file`) se definen en un formato agnÃ³stico.
3. **Llamada al Orquestador**: El sistema (ej: `Orchestrator`) llama a `MultiModelProcessor`.
4. **TraducciÃ³n**: El proveedor especÃ­fico (ej: `GeminiProvider`) traduce la definiciÃ³n de herramientas al formato que su API requiere.
5. **Inferencia del LLM**: El LLM recibe el prompt y las herramientas. Decide si debe responder con texto o invocar una herramienta.
6. **EjecuciÃ³n**: Si el LLM solicita una herramienta, el proveedor decodifica la solicitud, el sistema ejecuta la herramienta localmente y envÃ­a el resultado de vuelta al LLM para que continÃºe su razonamiento.

Este diseÃ±o garantiza que el resto del sistema pueda operar sin conocer los detalles de implementaciÃ³n de cada API, logrando una verdadera autonomÃ­a multi-proveedor.

