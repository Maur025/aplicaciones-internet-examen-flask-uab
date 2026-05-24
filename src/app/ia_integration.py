import json

import requests

URL = 'http://localhost:11434'


def request_to_ia(messages):
    payload = {
        'model': 'llama3.1:8b',
        'messages': messages,
        'stream': False
    }

    response = requests.post(
        url=f'{URL}/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
        },
        data=json.dumps(payload),
        timeout=60
    )

    response_json = response.json()

    print(response_json)
    return response_json['choices'][0]['message']['content']


def request_to_ia_native(messages):
    payload = {
        'model': 'llama3.1:8b',
        'messages': messages,
        'stream': False,
        'options': {
            'temperature': 0.1,
            'top_p': 0.9
        }
    }

    response = requests.post(url=f'{URL}/api/chat', json=payload, timeout=60)

    return response.json()['message']['content']


def metrics_analyzer(user_data):
    system_instruction = """
    Eres un Ingeniero de Confiabilidad de Sitios (SRE) y experto en Auditoría de Sistemas de Infraestructura. 
    Tu tarea es analizar el string de historial de métricas que te proporcionará el usuario, identificar anomalías, diagnosticar la causa raíz probable y ofrecer recomendaciones técnicas accionables.

    Para cada servidor analizado, debes estructurar tu respuesta estrictamente en este formato Markdown:

    ### 1. Diagnóstico del Servidor: [Nombre del Servidor]
    * **Estado Actual:** (OK / Advertencia / Crítico)
    * **Anomalía Detectada:** (Describe brevemente qué métrica falló, en qué momento y si muestra un patrón correlacionado, por ejemplo: correlación entre pico de red y uso de CPU).

    ### 2. Análisis de Causa Raíz (¿Qué causó esto?)
    * Presenta una hipótesis técnica y lógica basada en los datos (ej. Fuga de memoria/Memory Leak, ataque DDoS simulado, consultas pesadas a la base de datos sin indexar, falta de espacio en disco para paginación, etc.).

    ### 3. Recomendaciones y Acciones Correctivas
    * **Inmediatas (Mitigación):** (Qué comando o acción rápida tomar. Ej: Reiniciar servicio, liberar caché, matar proceso colgado).
    * **A largo plazo (Arquitectura):** (Qué cambiar en el diseño. Ej: Implementar un pool de conexiones, escalado horizontal, cambiar políticas de retención de logs).

    Sé conciso, técnico y directo al grano. Evita introducciones innecesarias.
    MUY IMPORTANTE: Analiza cada servidor de forma independiente. No repitas las mismas causas raíces o recomendaciones en bloque a menos que las métricas sean idénticas. Si el problema es de almacenamiento, concéntrate en espacio en disco; si es de RAM, en procesos o memoria.
    """

    messages = [{'role': 'system', 'content': system_instruction}, {'role': 'user', 'content': user_data}]

    return request_to_ia_native(messages)


def enhanced_analytic_response(raw_analysis):
    system_instruction = """
        Eres un Diseñador de Interfaces UI/UX especializado en Dashboards de Monitoreo de Infraestructura.
        Tu tarea es transformar un reporte técnico de métricas de servidores en un resumen ejecutivo visualmente impactante, limpio y muy corto en formato HTML.

        REGLAS DE FORMATO ESTRICTAS:
        1. Para cada servidor, debes generar una estructura limpia utilizando etiquetas standard de HTML5 (div, span, h4, ul, li).
        2. Usa clases semánticas de CSS ficticias para los estados (ej: 'status-ok', 'status-warning', 'status-critical') para poder darles estilos luego.
        3. Sé extremadamente directo. Solo queremos: Nombre del Servidor -> Estado -> Acción Inmediata Principal.
        4. NO devuelvas bloques de código Markdown (evita usar ```html ... ```). Devuelve ÚNICAMENTE el texto HTML plano para inyectar directo en el template.
        5. No agregues introducciones ni saludos.
        6. No ignores los servidores que no tengan datos, conviertelos a la plantilla y añade que no se detectaron anomalías.
        7. No unas o fusiones los servidores, asi tengan un nombre similar como SRV 1 o Server 1, solo fusiona algo cuando el nombre sea exactamente el mismo, por que si no lo es se tratan de los datos de otro servidor.

        EJEMPLO DE LA ESTRUCTURA ESPERADA POR SERVIDOR:
        <div class="server-summary-card">
            <div class="card-header-summary">
                <h4>Server2</h4>
                <span class="status-badge status-warning">Advertencia</span>
            </div>
            <div class="card-body-summary">
                <p><strong>Problema:</strong> Almacenamiento superó el 50% (Riesgo de paginación).</p>
                <p><strong>Acción Inmediata:</strong> Liberar espacio en disco y revisar retención de logs.</p>
            </div>
        </div>
        MUY IMPORTANTE: manter el template, solo reemplaza los datos necesarios, para mantener la compatibilidad con la lista que renderiza en html y sus estilos css, no agregues notas de ningun tipo, solo enfocate en transformar correctamente los datos
        """
    messages = [{'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': f'Simplifica y convierte este análisis técnico:\n\n{raw_analysis}'}]
    return request_to_ia_native(messages)
