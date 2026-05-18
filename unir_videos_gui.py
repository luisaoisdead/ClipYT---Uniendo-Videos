import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Configuración estética global (Estilo Dark Mode de ClipYT)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppUnirVideosClipYT(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal nativa
        self.title("Unir Videos - Estilo ClipYT")
        self.geometry("720x540")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")
        
        self.videos = []
        self.indice_arrastrado = None
        
        # --- ENCABEZADO (Estilo Barra Superior ClipYT) ---
        self.frame_header = ctk.CTkFrame(self, height=65, fg_color="#2d2d2d", corner_radius=0)
        self.frame_header.pack(fill=tk.X, side=tk.TOP)
        self.frame_header.pack_propagate(False)
        
        self.lbl_titulo = ctk.CTkLabel(
            self.frame_header, 
            text="Descargar y Recortar Videos de YouTube (Unión Directa)", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.lbl_titulo.pack(side=tk.LEFT, padx=25, pady=18)
        
        # --- CUERPO PRINCIPAL (Zona de Arrastre) ---
        self.frame_cuerpo = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0)
        self.frame_cuerpo.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        self.lbl_zona = ctk.CTkLabel(
            self.frame_cuerpo, 
            text="ZONA DE ARRASTRE", 
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color="#777777"
        )
        self.lbl_zona.pack(anchor=tk.W, pady=(0, 8))
        
        # Lista visual donde caen y se ordenan los archivos
        self.lista_UI = tk.Listbox(
            self.frame_cuerpo, 
            selectmode=tk.SINGLE, 
            bg="#161616", 
            fg="#e5e5e5", 
            font=("Arial", 11), 
            selectbackground="#2ecc71", 
            selectforeground="#ffffff",
            bd=0, 
            highlightthickness=1,
            highlightbackground="#333333",
            highlightcolor="#2ecc71",
            activestyle='none'
        )
        self.lista_UI.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Registro de eventos de Arrastrar y Soltar (Drag & Drop)
        self.lista_UI.drop_target_register(DND_FILES)
        self.lista_UI.dnd_bind('<<Drop>>', self.soltar_archivos)
        
        # Registro de eventos del Mouse para el reordenamiento manual
        self.lista_UI.bind("<ButtonPress-1>", self.iniciar_arrastre_interno)
        self.lista_UI.bind("<B1-Motion>", self.moviendo_elemento_interno)
        
        # --- CONTROL INFERIOR (Botonera) ---
        self.frame_botones = ctk.CTkFrame(self.frame_cuerpo, fg_color="transparent")
        self.frame_botones.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.btn_añadir = ctk.CTkButton(
            self.frame_botones, text="AÑADIR ARCHIVOS", fg_color="#3a3a3a", hover_color="#4a4a4a",
            text_color="#ffffff", font=ctk.CTkFont(weight="bold"), height=42, command=self.añadir_archivos_manual
        )
        self.btn_añadir.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 12))
        
        self.btn_limpiar = ctk.CTkButton(
            self.frame_botones, text="LIMPIAR LISTA", fg_color="#3a3a3a", hover_color="#c0392b",
            text_color="#ffffff", font=ctk.CTkFont(weight="bold"), height=42, command=self.limpiar_lista
        )
        self.btn_limpiar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 12))
        
        self.btn_guardar = ctk.CTkButton(
            self.frame_botones, text="GUARDAR", fg_color="#2ecc71", hover_color="#27ae60",
            text_color="#ffffff", font=ctk.CTkFont(size=14, weight="bold"), height=42, command=self.procesar_y_guardar
        )
        self.btn_guardar.pack(side=tk.LEFT, expand=True, fill=tk.X)

    # --- DRAG & DROP EXTERNO ---
    def soltar_archivos(self, event):
        datos = event.data
        if datos.startswith('{'):
            archivos = datos.strip('{}').split('} {')
        else:
            archivos = datos.split()

        for ruta in archivos:
            ruta = ruta.strip('"')
            if ruta.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                if ruta not in self.videos:
                    self.videos.append(ruta)
                    self.lista_UI.insert(tk.END, f" ⠿  {os.path.basename(ruta)}")
            else:
                messagebox.showwarning("Formato no válido", f"El archivo {os.path.basename(ruta)} no es soportado.")

    def añadir_archivos_manual(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccionar Videos",
            filetypes=[("Archivos de Video", "*.mp4 *.mkv *.avi *.mov"), ("Todos los archivos", "*.*")]
        )
        if archivos:
            for ruta in archivos:
                if ruta not in self.videos:
                    self.videos.append(ruta)
                    self.lista_UI.insert(tk.END, f" ⠿  {os.path.basename(ruta)}")

    def limpiar_lista(self):
        self.lista_UI.delete(0, tk.END)
        self.videos.clear()

    # --- REORDENAMIENTO CON EL MOUSE ---
    def iniciar_arrastre_interno(self, event):
        self.indice_arrastrado = self.lista_UI.nearest(event.y)

    def moviendo_elemento_interno(self, event):
        i = self.lista_UI.nearest(event.y)
        if i != self.indice_arrastrado and self.indice_arrastrado is not None:
            texto = self.lista_UI.get(self.indice_arrastrado)
            self.lista_UI.delete(self.indice_arrastrado)
            self.lista_UI.insert(i, texto)
            
            elemento = self.videos.pop(self.indice_arrastrado)
            self.videos.insert(i, elemento)
            
            self.indice_arrastrado = i

    # --- BACKEND REMUXING (FFMPEG CONCAT) ---
    def procesar_y_guardar(self):
        if len(self.videos) < 2:
            messagebox.showwarning("Acción Requerida", "Por favor, arrastrá al menos 2 videos para poder unirlos.")
            return

        archivo_salida = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("Video MP4", "*.mp4")],
            title="Guardar video unificado como..."
        )
        
        if not archivo_salida:
            return 
            
        ruta_txt_temporal = "lista_videos_temp.txt"
        try:
            with open(ruta_txt_temporal, "w", encoding="utf-8") as f:
                for video in self.videos:
                    ruta_limpia = video.replace("\\", "/")
                    f.write(f"file '{ruta_limpia}'\n")
            
            comando = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0', 
                '-i', ruta_txt_temporal, '-c', 'copy', archivo_salida
            ]
            
            self.config(cursor="watch")
            self.update()
            
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            messagebox.showinfo("¡Éxito!", f"Videos concatenados sin pérdida de calidad en:\n{archivo_salida}")
            self.limpiar_lista()
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors='ignore')
            messagebox.showerror("Error en Backend FFmpeg", f"No se pudo completar la unión:\n{error_msg}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un imprevisto: {str(e)}")
        finally:
            self.config(cursor="")
            if os.path.exists(ruta_txt_temporal):
                os.remove(ruta_txt_temporal)

if __name__ == "__main__":
    app = AppUnirVideosClipYT()
    app.mainloop()