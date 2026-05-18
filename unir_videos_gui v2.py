import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppEstudioEdicionClipYT(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("ClipYT - Estudio de Mezcla y Edición Avanzada (v6.0)")
        self.geometry("980x820")
        self.resizable(False, False)
        self.configure(bg="#1a1a1a")
        
        # Estructuras de datos lógicas
        self.pista_videos = []
        self.pista_audio2 = []
        self.pista_audio3 = []
        
        # Referencias a los componentes Listbox
        self.lista_v_ui = None
        self.lista_a2_ui = None
        self.lista_a3_ui = None
        
        # Variables de control para la barra de progreso interna
        self.reproduciendo = False
        self.tiempo_actual = 0.0
        self.duracion_total = 0.0
        
        # --- ENCABEZADO ---
        self.frame_header = ctk.CTkFrame(self, height=55, fg_color="#252525", corner_radius=0)
        self.frame_header.pack(fill=tk.X, side=tk.TOP)
        self.frame_header.pack_propagate(False)
        
        self.lbl_titulo = ctk.CTkLabel(
            self.frame_header, text="🎬 ClipYT Multi-Track Editor Pro", 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"), text_color="#ffffff"
        )
        self.lbl_titulo.pack(side=tk.LEFT, padx=20, pady=12)

        # --- CONTENEDOR DE PISTAS (IZQUIERDA) ---
        self.frame_pistas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_pistas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.lista_v_ui = self.crear_seccion_pista(self.frame_pistas, "🎥 PISTA DE VIDEO (Clips Secuenciales)", "video", self.pista_videos)
        self.lista_a2_ui = self.crear_seccion_pista(self.frame_pistas, "🎵 PISTA DE AUDIO 2 (Múltiples audios)", "audio2", self.pista_audio2)
        self.lista_a3_ui = self.crear_seccion_pista(self.frame_pistas, "🎵 PISTA DE AUDIO 3 (Múltiples audios)", "audio3", self.pista_audio3)

        # --- PANEL DE CONTROL Y MEZCLA (DERECHA) ---
        self.frame_mezclador = ctk.CTkFrame(self, width=320, fg_color="#222222", border_width=1, border_color="#333333")
        self.frame_mezclador.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=15)
        self.frame_mezclador.pack_propagate(False)
        
        self.lbl_mezcla_tit = ctk.CTkLabel(self.frame_mezclador, text="🎛️ CONSOLA DE MEZCLA", font=ctk.CTkFont(weight="bold", size=14))
        self.lbl_mezcla_tit.pack(pady=15)

        # CONTROLES AUDIO VIDEO ORIGINAL
        self.frame_ctrl_v = ctk.CTkFrame(self.frame_mezclador, fg_color="#2b2b2b")
        self.frame_ctrl_v.pack(fill=tk.X, padx=15, pady=5)
        self.lbl_vol_v = ctk.CTkLabel(self.frame_ctrl_v, text="Volumen Video Original: 100%", font=ctk.CTkFont(size=11))
        self.lbl_vol_v.pack(anchor=tk.W, padx=10, pady=(5,0))
        self.slider_vol_v = ctk.CTkSlider(self.frame_ctrl_v, from_=0, to=2, command=lambda v: self.lbl_vol_v.configure(text=f"Volumen Video Original: {int(float(v)*100)}%"))
        self.slider_vol_v.set(1.0)
        self.slider_vol_v.pack(fill=tk.X, padx=10, pady=(0,5))

        # CONTROLES AUDIO PISTA 2
        self.frame_ctrl_a2 = ctk.CTkFrame(self.frame_mezclador, fg_color="#2b2b2b")
        self.frame_ctrl_a2.pack(fill=tk.X, padx=15, pady=5)
        self.lbl_vol_a2 = ctk.CTkLabel(self.frame_ctrl_a2, text="Volumen Pista Audio 2: 100%", font=ctk.CTkFont(size=11))
        self.lbl_vol_a2.pack(anchor=tk.W, padx=10, pady=(5,0))
        self.slider_vol_a2 = ctk.CTkSlider(self.frame_ctrl_a2, from_=0, to=2, command=lambda v: self.lbl_vol_a2.configure(text=f"Volumen Pista Audio 2: {int(float(v)*100)}%"))
        self.slider_vol_a2.set(1.0)
        self.slider_vol_a2.pack(fill=tk.X, padx=10, pady=5)
        self.check_suave_a2 = ctk.CTkCheckBox(self.frame_ctrl_a2, text="Suavizar Transiciones (Crossfade)", font=ctk.CTkFont(size=11))
        self.check_suave_a2.pack(anchor=tk.W, padx=10, pady=(0,5))

        # CONTROLES AUDIO PISTA 3
        self.frame_ctrl_a3 = ctk.CTkFrame(self.frame_mezclador, fg_color="#2b2b2b")
        self.frame_ctrl_a3.pack(fill=tk.X, padx=15, pady=5)
        self.lbl_vol_a3 = ctk.CTkLabel(self.frame_ctrl_a3, text="Volumen Pista Audio 3: 100%", font=ctk.CTkFont(size=11))
        self.lbl_vol_a3.pack(anchor=tk.W, padx=10, pady=(5,0))
        self.slider_vol_a3 = ctk.CTkSlider(self.frame_ctrl_a3, from_=0, to=2, command=lambda v: self.lbl_vol_a3.configure(text=f"Volumen Pista Audio 3: {int(float(v)*100)}%"))
        self.slider_vol_a3.set(1.0)
        self.slider_vol_a3.pack(fill=tk.X, padx=10, pady=5)
        self.check_suave_a3 = ctk.CTkCheckBox(self.frame_ctrl_a3, text="Suavizar Transiciones (Crossfade)", font=ctk.CTkFont(size=11))
        self.check_suave_a3.pack(anchor=tk.W, padx=10, pady=(0,5))

        # --- NUEVA SECCIÓN: BARRA DE PROGRESO EN LA VENTANA PRINCIPAL ---
        self.frame_timeline_interno = ctk.CTkFrame(self.frame_mezclador, fg_color="#1a1a1a", border_width=1, border_color="#333333")
        self.frame_timeline_interno.pack(fill=tk.X, padx=15, pady=(25, 5))
        
        self.lbl_reloj_interno = ctk.CTkLabel(self.frame_timeline_interno, text="00:00 / 00:00", font=ctk.CTkFont(family="Arial", size=12, weight="bold"))
        self.lbl_reloj_interno.pack(pady=(5, 2))
        
        self.progress_timeline = ctk.CTkProgressBar(self.frame_timeline_interno, progress_color="#2ecc71", fg_color="#333333", height=10)
        self.progress_timeline.set(0.0)
        self.progress_timeline.pack(fill=tk.X, padx=15, pady=(0, 10))

        # --- BOTONERA ACCIONES DE SALIDA ---
        self.btn_preview = ctk.CTkButton(
            self.frame_mezclador, text="👁️ PREVISUALIZAR EN VIVO", fg_color="#3498db", hover_color="#2980b9",
            text_color="#ffffff", font=ctk.CTkFont(weight="bold"), height=45, command=self.previsualizar_en_vivo
        )
        self.btn_preview.pack(fill=tk.X, padx=15, pady=(15, 10))

        self.btn_guardar = ctk.CTkButton(
            self.frame_mezclador, text="💾 GUARDAR COMPILACIÓN", fg_color="#2ecc71", hover_color="#27ae60",
            text_color="#ffffff", font=ctk.CTkFont(weight="bold", size=13), height=45, command=self.guardar_render_final
        )
        self.btn_guardar.pack(fill=tk.X, padx=15, pady=5)
        
        self.btn_limpiar = ctk.CTkButton(
            self.frame_mezclador, text="LIMPIAR TODO", fg_color="#e74c3c", hover_color="#c0392b",
            text_color="#ffffff", font=ctk.CTkFont(weight="bold"), height=32, command=self.limpiar_todo
        )
        self.btn_limpiar.pack(fill=tk.X, padx=15, pady=(20, 0))

    def crear_seccion_pista(self, master, titulo, tipo, lista_datos):
        frame_contenedor = ctk.CTkFrame(master, fg_color="#222222", border_width=1, border_color="#333333")
        frame_contenedor.pack(fill=tk.BOTH, expand=True, pady=5)
        
        lbl = ctk.CTkLabel(frame_contenedor, text=titulo, font=ctk.CTkFont(size=12, weight="bold"), text_color="#aaaaaa")
        lbl.pack(anchor=tk.W, padx=12, pady=(6, 2))
        
        frame_interno = ctk.CTkFrame(frame_contenedor, fg_color="transparent")
        frame_interno.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))
        
        lista_ui = tk.Listbox(
            frame_interno, selectmode=tk.SINGLE, bg="#141414", fg="#dddddd", font=("Arial", 9),
            selectbackground="#3498db", bd=0, highlightthickness=0, height=4
        )
        lista_ui.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        frame_botones_lista = ctk.CTkFrame(frame_interno, fg_color="transparent", width=40)
        frame_botones_lista.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        
        btn_subir = ctk.CTkButton(
            frame_botones_lista, text="🔼", width=32, height=25, fg_color="#3a3a3a", hover_color="#555555",
            command=lambda: self.mover_item(lista_ui, lista_datos, -1)
        )
        btn_subir.pack(pady=1)
        
        btn_bajar = ctk.CTkButton(
            frame_botones_lista, text="🔽", width=32, height=25, fg_color="#3a3a3a", hover_color="#555555",
            command=lambda: self.mover_item(lista_ui, lista_datos, 1)
        )
        btn_bajar.pack(pady=1)
        
        btn_borrar = ctk.CTkButton(
            frame_botones_lista, text="❌", width=32, height=25, fg_color="#552222", hover_color="#992222",
            command=lambda: self.eliminar_item_pista(lista_ui, lista_datos)
        )
        btn_borrar.pack(pady=(5, 0))
        
        lista_ui.drop_target_register(DND_FILES)
        lista_ui.dnd_bind('<<Drop>>', lambda e: self.soltar_en_pista(e, tipo, lista_ui, lista_datos))
        
        return lista_ui

    def soltar_en_pista(self, event, tipo, lista_ui, lista_datos):
        datos = event.data
        if datos.startswith('{'):
            archivos = datos.strip('{}').split('} {')
        else:
            archivos = datos.split()

        for ruta in archivos:
            ruta = ruta.strip('"')
            es_video = ruta.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))
            es_audio = ruta.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg', '.aac'))
            
            if tipo == "video" and es_video:
                lista_datos.append(ruta)
                lista_ui.insert(tk.END, f" 🎞️  {os.path.basename(ruta)}")
            elif tipo.startswith("audio") and es_audio:
                lista_datos.append(ruta)
                lista_ui.insert(tk.END, f" 🎵  {os.path.basename(ruta)}")
            else:
                messagebox.showwarning("Formato incorrecto", f"El archivo {os.path.basename(ruta)} no corresponde a esta pista.")

    def mover_item(self, lista_ui, lista_datos, direccion):
        seleccion = lista_ui.curselection()
        if not seleccion:
            return
        
        idx_actual = seleccion[0]
        idx_nuevo = idx_actual + direccion
        
        if idx_nuevo < 0 or idx_nuevo >= lista_ui.size():
            return
            
        lista_datos[idx_actual], lista_datos[idx_nuevo] = lista_datos[idx_nuevo], lista_datos[idx_actual]
        
        texto_item = lista_ui.get(idx_actual)
        lista_ui.delete(idx_actual)
        lista_ui.insert(idx_nuevo, texto_item)
        
        lista_ui.select_set(idx_nuevo)
        lista_ui.activate(idx_nuevo)

    def eliminar_item_pista(self, lista_ui, lista_datos):
        seleccion = lista_ui.curselection()
        if seleccion:
            idx = seleccion[0]
            lista_ui.delete(idx)
            lista_datos.pop(idx)

    def limpiar_todo(self):
        self.pista_videos.clear()
        self.pista_audio2.clear()
        self.pista_audio3.clear()
        
        if self.lista_v_ui: self.lista_v_ui.delete(0, tk.END)
        if self.lista_a2_ui: self.lista_a2_ui.delete(0, tk.END)
        if self.lista_a3_ui: self.lista_a3_ui.delete(0, tk.END)
                                
        self.slider_vol_v.set(1.0)
        self.slider_vol_a2.set(1.0)
        self.slider_vol_a3.set(1.0)
        
        self.lbl_vol_v.configure(text="Volumen Video Original: 100%")
        self.lbl_vol_a2.configure(text="Volumen Pista Audio 2: 100%")
        self.lbl_vol_a3.configure(text="Volumen Pista Audio 3: 100%")
        
        self.check_suave_a2.deselect()
        self.check_suave_a3.deselect()
        
        # Resetear barra interna
        self.reproduciendo = False
        self.progress_timeline.set(0.0)
        self.lbl_reloj_interno.configure(text="00:00 / 00:00")
        
        messagebox.showinfo("Limpieza", "Se vaciaron todas las pistas y controles con éxito.")

    def obtener_duracion_total_videos(self):
        total_segs = 0.0
        for video in self.pista_videos:
            try:
                comando = [
                    'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1', video
                ]
                resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                dur = resultado.stdout.decode('utf-8').strip()
                if dur: total_segs += float(dur)
            except Exception:
                pass
        return total_segs if total_segs > 0 else 1.0

    # --- RELOJ INTERNO ASÍNCRONO ---
    def actualizar_barra_progreso(self):
        if not self.reproduciendo:
            return
        
        if self.tiempo_actual < self.duracion_total:
            self.tiempo_actual += 1.0
            
            # Calcular porcentaje de la barra (valor entre 0.0 y 1.0)
            porcentaje = min(self.tiempo_actual / self.duracion_total, 1.0)
            self.progress_timeline.set(porcentaje)
            
            # Formatear strings del reloj
            min_cur = int(self.tiempo_actual // 60)
            seg_cur = int(self.tiempo_actual % 60)
            min_tot = int(self.duracion_total // 60)
            seg_tot = int(self.duracion_total % 60)
            
            self.lbl_reloj_interno.configure(text=f"{min_cur:02d}:{seg_cur:02d} / {min_tot:02d}:{seg_tot:02d}")
            
            # Volver a llamarse dentro de 1000 milisegundos (1 segundo)
            self.after(1000, self.actualizar_barra_progreso)
        else:
            self.reproduciendo = False
            self.progress_timeline.set(1.0)

    def armar_filtro_complejo(self, archivo_salida, es_preview=False):
        if not self.pista_videos:
            messagebox.showwarning("Error de línea de tiempo", "La pista de video no puede estar vacía.")
            return None

        ruta_txt_videos = "temp_videos.txt"
        with open(ruta_txt_videos, "w", encoding="utf-8") as f:
            for v in self.pista_videos:
                ruta_limpia = v.replace('\\', '/')
                f.write(f"file '{ruta_limpia}'\n")

        comando = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', ruta_txt_videos]
        
        for a2 in self.pista_audio2:
            comando += ['-i', a2]
            
        for a3 in self.pista_audio3:
            comando += ['-i', a3]

        idx_actual = 1
        filtro_pista2 = ""
        filtro_pista3 = ""
        
        if self.pista_audio2:
            inputs_a2 = "".join(f"[{i}:a]" for i in range(idx_actual, idx_actual + len(self.pista_audio2)))
            unir_tipo = "acrossfade=d=1" if self.check_suave_a2.get() and len(self.pista_audio2) > 1 else "concat=n=1:v=0:a=1"
            
            if "acrossfade" in unir_tipo:
                temp_filtro = f"[{idx_actual}:a][{idx_actual+1}:a]acrossfade=d=1[aud_out2_0];"
                for k in range(2, len(self.pista_audio2)):
                    temp_filtro += f"[aud_out2_{k-2}][{idx_actual+k}:a]acrossfade=d=1[aud_out2_{k-1}];"
                filtro_pista2 = temp_filtro.replace(f"[aud_out2_{len(self.pista_audio2)-2}]", "[pista2_cruda]")
            else:
                filtro_pista2 = f"{inputs_a2}concat=n={len(self.pista_audio2)}:v=0:a=1[pista2_cruda];"
                
            filtro_pista2 += f"[pista2_cruda]volume={self.slider_vol_a2.get()}[pista2_lista];"
            idx_actual += len(self.pista_audio2)

        if self.pista_audio3:
            inputs_a3 = "".join(f"[{i}:a]" for i in range(idx_actual, idx_actual + len(self.pista_audio3)))
            unir_tipo = "acrossfade=d=1" if self.check_suave_a3.get() and len(self.pista_audio3) > 1 else "concat=n=1:v=0:a=1"
            
            if "acrossfade" in unir_tipo:
                temp_filtro = f"[{idx_actual}:a][{idx_actual+1}:a]acrossfade=d=1[aud_out3_0];"
                for k in range(2, len(self.pista_audio3)):
                    temp_filtro += f"[aud_out3_{k-2}][{idx_actual+k}:a]acrossfade=d=1[aud_out3_{k-1}];"
                filtro_pista3 = temp_filtro.replace(f"[aud_out3_{len(self.pista_audio3)-2}]", "[pista3_cruda]")
            else:
                filtro_pista3 = f"{inputs_a3}concat=n={len(self.pista_audio3)}:v=0:a=1[pista3_cruda];"
                
            filtro_pista3 += f"[pista3_cruda]volume={self.slider_vol_a3.get()}[pista3_lista];"

        filtro_master = f"[0:a]volume={self.slider_vol_v.get()}[pista1_lista];" + filtro_pista2 + filtro_pista3
        
        inputs_amix = "[pista1_lista]"
        num_entradas = 1
        if self.pista_audio2:
            inputs_amix += "[pista2_lista]"
            num_entradas += 1
        if self.pista_audio3:
            inputs_amix += "[pista3_lista]"
            num_entradas += 1
            
        filtro_master += f"{inputs_amix}amix=inputs={num_entradas}:duration=first:dropout_transition=0[audio_master]"

        comando += ['-filter_complex', filtro_master, '-map', '0:v', '-map', '[audio_master]']
        
        if es_preview:
            comando += ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '28', '-vf', 'scale=-2:360', '-c:a', 'aac', archivo_salida]
        else:
            comando += ['-c:v', 'copy', '-c:a', 'aac', archivo_salida]
            
        return comando

    # --- PREVISUALIZACIÓN CON CONTROLES INTEGRADOS EN TU VENTANA ---
    def previsualizar_en_vivo(self):
        if not self.pista_videos:
            messagebox.showwarning("Error", "La pista de video no puede estar vacía.")
            return

        archivo_temp_preview = "temp_preview_clipyt.mp4"
        comando = self.armar_filtro_complejo(archivo_temp_preview, es_preview=True)
        if not comando: return
        
        try:
            self.config(cursor="watch")
            self.update()
            
            # 1. Generar render express
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 2. Inicializar la barra de progreso interna en la GUI
            self.duracion_total = self.obtener_duracion_total_videos()
            self.tiempo_actual = 0.0
            self.reproduciendo = True
            
            min_tot = int(self.duracion_total // 60)
            seg_tot = int(self.duracion_total % 60)
            self.lbl_reloj_interno.configure(text=f"00:00 / {min_tot:02d}:{seg_tot:02d}")
            self.progress_timeline.set(0.0)
            
            # Arrancar reloj asíncrono
            self.actualizar_barra_progreso()
            
            # 3. Lanzar FFPLAY limpio (sin barras encima del video)
            comando_play = [
                'ffplay', 
                '-autoexit', 
                '-x', '854', '-y', '480',
                '-infbuf',
                '-window_title', f'ClipYT Player | [ESPACIO = Pausa | ESC = Salir]',
                archivo_temp_preview
            ]
            subprocess.run(comando_play, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema con el reproductor.\nDetalle: {str(e)}")
        finally:
            self.config(cursor="")
            self.reproduciendo = False # Detener reloj al cerrar video
            for f in ["temp_videos.txt", archivo_temp_preview]:
                if os.path.exists(f): os.remove(f)

    def guardar_render_final(self):
        archivo_salida = filedialog.asksaveasfilename(
            defaultextension=".mp4", filetypes=[("Video MP4", "*.mp4")], title="Exportar Master Unificado..."
        )
        if not archivo_salida: return
        
        comando = self.armar_filtro_complejo(archivo_salida, es_preview=False)
        if not comando: return
        
        try:
            self.config(cursor="watch")
            self.update()
            
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("¡Éxito!", f"Render completado con éxito sin pérdida de calidad en video.\nArchivo: {archivo_salida}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error en Render FFmpeg", f"Fallo en la matriz de filtros:\n{e.stderr.decode(errors='ignore')}")
        finally:
            self.config(cursor="")
            if os.path.exists("temp_videos.txt"):
                os.remove("temp_videos.txt")

if __name__ == "__main__":
    app = AppEstudioEdicionClipYT()
    app.mainloop()