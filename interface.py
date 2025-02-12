import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import webbrowser  # Importar filedialog para seleccionar archivos
from PIL import Image, ImageTk  # Importar para cargar iconos (Pillow)
from main import getContext, respuestaCompleta, getAllDB, añadirHist, obtenerHist, getContextFilter, uploadDocDB
import os  # Para ejecutar comandos del sistema

class Aplicacion:
    def __init__(self, master):
        self.master = master
        master.title("Interfaz de Consulta")
        
        # Hacer que la ventana ocupe toda la pantalla
        master.state('zoomed')

        master.columnconfigure(0, weight=3)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)

        # Crear frame_izquierdo
        self.frame_izquierdo = ttk.Frame(master)
        self.frame_izquierdo.grid(row=0, column=0, sticky="nsew")
        self.frame_izquierdo.columnconfigure(0, weight=1)
        self.frame_izquierdo.rowconfigure(3, weight=1)

        # Crear frame_derecho
        self.frame_derecho = ttk.Frame(master)
        self.frame_derecho.grid(row=0, column=1, sticky="nsew")
        self.frame_derecho.columnconfigure(0, weight=1)
        self.frame_derecho.rowconfigure(1, weight=1)

        # Configurar widgets en frame_derecho
        self.titulo_checkboxes = ttk.Label(self.frame_derecho, text="Opciones")
        self.titulo_checkboxes.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Barra de búsqueda para el checkboxlist
        self.barra_busqueda = ttk.Entry(self.frame_derecho, width=40)
        self.barra_busqueda.grid(row=1, column=0, padx=10, pady=(10), sticky="ew")  # Reducir padding vertical
        self.barra_busqueda.bind("<KeyRelease>", self.filtrar_documentos)  # Actualiza al escribir

        # Botón de cargar archivo con ícono
        # self.icono_upload = Image.open("upload.png")  # Asegúrate de que el archivo de imagen esté en el directorio correcto
        # self.icono_upload = self.icono_upload.resize((20, 20))  # Ajustar tamaño
        # self.icono_upload = ImageTk.PhotoImage(self.icono_upload)  # Convertir imagen a formato Tkinter

        self.boton_cargar = ttk.Button(self.frame_derecho,text="Cargar archivo", command=self.cargar_archivo)
        self.boton_cargar.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        # Botón de actualizar (refresh) con ícono
        self.boton_actualizar = tk.Button(self.frame_derecho, command=self.actualizar, width=20, height=20)  # Ajusta width y height
        self.boton_actualizar.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        # Cargar el ícono de refresh
        self.icono_refresh = Image.open("refresh_icon.png")  # Asegúrate de que el archivo de imagen esté en el directorio correcto
        self.icono_refresh = self.icono_refresh.resize((20, 20))  # Ajustar tamaño
        self.icono_refresh = ImageTk.PhotoImage(self.icono_refresh)  # Convertir imagen a formato Tkinter
        self.boton_actualizar.config(image=self.icono_refresh, compound="center") 

        # Crear un canvas con scrollbar para los checkboxes
        self.canvas_checkboxes = tk.Canvas(self.frame_derecho)
        self.scrollbar_checkboxes = ttk.Scrollbar(self.frame_derecho, orient="vertical", command=self.canvas_checkboxes.yview)
        self.frame_checkboxes = ttk.Frame(self.canvas_checkboxes)

        self.frame_checkboxes.bind(
            "<Configure>",
            lambda e: self.canvas_checkboxes.configure(
                scrollregion=self.canvas_checkboxes.bbox("all")
            )
        )

        self.canvas_checkboxes.create_window((0, 0), window=self.frame_checkboxes, anchor="nw")
        self.canvas_checkboxes.configure(yscrollcommand=self.scrollbar_checkboxes.set)

        self.canvas_checkboxes.grid(row=2, column=0, sticky="nsew", padx=(10, 0), pady=10)
        self.scrollbar_checkboxes.grid(row=2, column=2, sticky="ns", pady=10)

        # **Ajustamos el peso de las filas para dar más espacio al checkboxlist**
        self.frame_derecho.rowconfigure(1, weight=0)  # Reducimos el peso de la fila de la barra de búsqueda
        self.frame_derecho.rowconfigure(2, weight=3)  # Aumentamos el peso de la fila de los checkboxes

        # Widgets en frame_izquierdo
        self.entrada = tk.Text(self.frame_izquierdo, height=5, width=30, wrap=tk.WORD)
        self.entrada.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Frame para K y botón de enviar
        self.frame_k_enviar = ttk.Frame(self.frame_izquierdo)
        self.frame_k_enviar.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.frame_k_enviar.columnconfigure(3, weight=1)  # Ajustar el botón de enviar, cargar archivo, y filtro

        self.label_k = ttk.Label(self.frame_k_enviar, text="Cantidad de referencias:")
        self.label_k.grid(row=0, column=0, padx=(0, 5))

        self.entrada_k = ttk.Entry(self.frame_k_enviar, width=5)
        self.entrada_k.grid(row=0, column=1, padx=(0, 10))
        self.entrada_k.insert(0, "2")  # Valor predeterminado

        self.boton_enviar = ttk.Button(self.frame_k_enviar, text="Buscar", command=self.enviar)
        self.boton_enviar.grid(row=0, column=3, sticky="e")

        self.boton_filtrado = ttk.Button(self.frame_k_enviar, text="Buscar Filtrado", command=self.SearchFiltred)
        self.boton_filtrado.grid(row=0, column=4, sticky="e")

        self.boton_nuevo = ttk.Button(self.frame_izquierdo, text="Ver registro de consultas", command=self.nuevo)
        self.boton_nuevo.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Aumentar el tamaño de la ventana de respuesta
        self.respuesta = tk.Text(self.frame_izquierdo, wrap=tk.WORD, height=20)
        self.respuesta.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Variables para checkboxes
        self.check_vars = {}

        # Configurar frame_documentos
        self.frame_documentos = ttk.Frame(self.frame_izquierdo)
        self.frame_documentos.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.frame_izquierdo.rowconfigure(4, weight=1)

        # Configurar canvas y scrollbar para documentos
        self.canvas = tk.Canvas(self.frame_documentos)
        self.scrollbar = ttk.Scrollbar(self.frame_documentos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.documentos = []
        self.cargar_documentos_iniciales()

    def actualizar(self):
        try:
            self.documentos = getAllDB()
            self.actualizar_checkboxes(self.documentos)
        except Exception as e:
            print(f"Error al cargar documentos iniciales: {e}")

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if archivo:
            try:
                # Asume que uploadDocDB es la función que sube el archivo y retorna un response
                response = uploadDocDB(archivo)

                try:
                    self.documentos = getAllDB()
                    self.actualizar_checkboxes(self.documentos)
                except Exception as e:
                    print(f"Error al cargar documentos iniciales: {e}")

                # Si el archivo se carga correctamente, muestra un cuadro de diálogo con el resultado
                messagebox.showinfo("Carga Exitosa", f"El archivo '{archivo}' se ha cargado correctamente.\nRespuesta: {response}")
            
            except Exception as e:
                # Si ocurre un error, muestra un cuadro de diálogo con el mensaje de error
                messagebox.showerror("Error al cargar archivo", f"Ocurrió un error al cargar el archivo:\n{str(e)}")


    def SearchFiltred(self):
        # Obtener documentos seleccionados
        try:
            lstDocs = [doc for doc, var in self.check_vars.items() if var.get()]

            # Obtener el valor de K
            try:
                k = int(self.entrada_k.get())
            except ValueError:
                self.respuesta.delete(1.0, tk.END)
                self.respuesta.insert(tk.END, "Error: K debe ser un número entero válido.")
                return

            # Obtener el texto del input
            pregunta = self.entrada.get("1.0", tk.END).strip()

            # Llamar a la función getContextFilter con los parámetros
            context = getContextFilter(lstDocs, pregunta, k)
            response = respuestaCompleta(pregunta, context=context)

            añadirHist(pregunta, response.content)

            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, response.content)


            self.cargar_documentos_lista(context)

        except ValueError:
            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, "Error: K debe ser un número entero válido.")
        except Exception as e:
            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, f"Error: {str(e)}")

    def filtrar_documentos(self, event=None):
        """Filtra los documentos basados en el texto ingresado en la barra de búsqueda."""
        texto_busqueda = self.barra_busqueda.get().lower()
        
        # Filtrar los documentos que contienen el texto de búsqueda en su nombre
        documentos_filtrados = [
            doc for doc in self.documentos
            if texto_busqueda in doc['metadata'].get('nombre_archivo', '').lower()
        ]
        
        # Actualizar los checkboxes con los documentos filtrados
        self.actualizar_checkboxes(documentos_filtrados)

    def cargar_documentos_iniciales(self):
        try:
            self.documentos = getAllDB()
            self.actualizar_checkboxes(self.documentos)
        except Exception as e:
            print(f"Error al cargar documentos iniciales: {e}")

    def actualizar_checkboxes(self, documentos):
        """Actualiza la lista de checkboxes según los documentos proporcionados."""
        for widget in self.frame_checkboxes.winfo_children():
            widget.destroy()

        if not documentos:
            label = ttk.Label(self.frame_checkboxes, text="No hay documentos disponibles")
            label.pack(padx=5, pady=2, anchor="w")
        else:
            archivos_unicos = set()
            for doc in documentos:
                nombre_archivo = doc['metadata'].get('nombre_archivo', 'Referencia sin nombre')
                archivos_unicos.add(nombre_archivo)

            for i, nombre_archivo in enumerate(sorted(archivos_unicos)):
                frame = ttk.Frame(self.frame_checkboxes)
                frame.pack(fill="x", padx=5, pady=2)

                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(frame, text=nombre_archivo, variable=var)
                checkbox.pack(side="left")

                self.check_vars[nombre_archivo] = var

        self.canvas_checkboxes.update_idletasks()
        self.canvas_checkboxes.configure(scrollregion=self.canvas_checkboxes.bbox("all"))

    def enviar(self):
        try:
            pregunta = self.entrada.get("1.0", tk.END).strip()  # Obtener todo el texto del widget Text
            k = int(self.entrada_k.get())  # Obtener el valor de K
            context = getContext(pregunta, k=k)  # Usar el valor de K
            response = respuestaCompleta(pregunta, context=context)

            añadirHist(pregunta, response.content)

            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, response.content)

            self.cargar_documentos_lista(context)

        except ValueError:
            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, "Error: K debe ser un número entero válido.")
        except Exception as e:
            self.respuesta.delete(1.0, tk.END)
            self.respuesta.insert(tk.END, f"Error: {str(e)}")

    def nuevo(self):
        historial = obtenerHist()
        self.mostrar_historial_popup(historial)

    def mostrar_historial_popup(self, historial):
        ventana_historial = tk.Toplevel(self.master)
        ventana_historial.title("Registro de Consultas")
        ventana_historial.geometry("600x400")

        # Crear un widget Text para mostrar el historial
        texto_historial = tk.Text(ventana_historial, wrap=tk.WORD)
        texto_historial.pack(expand=True, fill="both", padx=10, pady=10)

        # Agregar una barra de desplazamiento
        scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=texto_historial.yview)
        scrollbar.pack(side="right", fill="y")
        texto_historial.configure(yscrollcommand=scrollbar.set)

        # Insertar el historial en el widget Text
        for entrada in historial:
            texto_historial.insert(tk.END, f"Usuario: {entrada['User']}\n\n")
            texto_historial.insert(tk.END, f"Sistema: {entrada['Sistem']}\n\n")
            texto_historial.insert(tk.END, "-" * 50 + "\n\n")

        # Hacer el widget Text de solo lectura
        texto_historial.config(state=tk.DISABLED)

    def abrir_pdf(self, nombre_pdf):
        """Abrir el archivo PDF en el visor predeterminado del sistema."""
        # Verificamos si el archivo ya tiene la extensión .pdf, si no la tiene, la agregamos
        if not nombre_pdf.lower().endswith(".pdf"):
            nombre_pdf += ".pdf"

        ruta_pdf = f"pdfs/{nombre_pdf}"
        
        # Aseguramos que la ruta esté entre comillas si contiene espacios
        ruta_pdf_escapada = f'{ruta_pdf}'            

        ruta_absoluta = os.path.abspath(ruta_pdf_escapada)

        print(ruta_absoluta)
    
        # Verificar si el archivo existe
        if os.path.exists(ruta_absoluta):
            # Abrir el PDF en el navegador predeterminado
            webbrowser.open('file://' + ruta_absoluta)
        else:
            messagebox.showerror("Error", f"No se encontró el archivo PDF: {ruta_pdf_escapada}")

    def cargar_documentos_lista(self, documentos):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not documentos:
            label = ttk.Label(self.scrollable_frame, text="No hay documentos disponibles")
            label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        else:
            for i, doc in enumerate(documentos):
                frame = ttk.Frame(self.scrollable_frame)
                frame.grid(row=i, column=0, padx=5, pady=2, sticky="w")

                label = ttk.Label(frame, text=f"Referencia {i+1}", font=("Default", 14, "bold"))
                label.grid(row=0, column=0, sticky="w")

                boton_ver = ttk.Button(frame, text="Ver", command=lambda d=doc: self.ver_documento(d))  
                boton_ver.grid(row=0, column=1, padx=5, sticky="e")

                # Botón para abrir el archivo PDF
                boton_pdf = ttk.Button(frame, text="Abrir PDF", command=lambda d=doc: self.abrir_pdf(d['metadata'].get('nombre_archivo', '')))
                boton_pdf.grid(row=0, column=2, padx=5, sticky="e")

                for j, (key, value) in enumerate(doc['metadata'].items()):
                    metadata_label = ttk.Label(frame, text=f"{key}: {value}", font=("Default", 11))
                    metadata_label.grid(row=j+1, column=0, columnspan=2, sticky="w")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def ver_documento(self, documento):
        ventana_detalles = tk.Toplevel(self.master)
        ventana_detalles.title("Detalles del Documento")

        ttk.Label(ventana_detalles, text="Metadata:").pack(anchor="w")
        for key, value in documento['metadata'].items():
            ttk.Label(ventana_detalles, text=f"{key}: {value}").pack(anchor="w")

        ttk.Label(ventana_detalles, text="Contenido:").pack(anchor="w")
        texto_contenido = tk.Text(ventana_detalles, wrap=tk.WORD, height=10, width=50)
        texto_contenido.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        texto_contenido.insert(tk.END, documento['content'])
        texto_contenido.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()