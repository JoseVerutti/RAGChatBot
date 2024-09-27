
def get_answer(pregunta, contexto, client, model:str = "gpt-3.5-turbo-16k", max_tokens :int = 800):

    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
                    {"role": "system", "content": f""" Como asistente de investigación doctoral. 
                Tu tarea es responder al usuario teniendo en cuenta las consideraciones del tag consideraciones para ayudar al estudiante de doctorado a redactar secciones de sus tesis utilizando el contexto del tag documents_context.

                <consideraciones>
                1. Analiza cuidadosamente el contexto proporcionado.
                2. Para cada fragmento de texto que generes, referencia el título del documento del que te basaste para redactarlo. Referéncialo con el siguiente formato extraido del metadata: [nombre_archivo, pagina]
                3. Estructura tu respuesta de manera lógica, utilizando párrafos bien organizados y, cuando sea apropiado, subtítulos.
                4. Utiliza un lenguaje académico y técnico adecuado para el nivel de doctorado.
                5. Si el tag documents_context no proporciona suficiente información para responder completamente, indícalo claramente.
                6. Response solo con información que esté respaldada por el tag documents_context.
                7. Si es relevante, sugiere conexiones o implicaciones basadas en la información del tag documents_context, pero distingue claramente entre hechos establecidos y posibles interpretaciones.
                </consideraciones>

                     
                ´´´
                {contexto}
                ´´´

                """},
                    {"role": "user", "content": f"{pregunta}. Recuerda citar la información"}
                ]
    )
    return completion.choices[0].message