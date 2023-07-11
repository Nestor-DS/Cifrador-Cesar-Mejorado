import tkinter as tk
from tkinter import ttk, filedialog
import unicodedata

class CriptogramaApplication:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Cifrador tipo César")
        self.ventana.geometry("500x600")

        self.desplazamiento = tk.StringVar()

        self._crear_interfaz()

    def _crear_interfaz(self):
        frame_principal = ttk.Frame(self.ventana, padding=20)
        frame_principal.pack()

# Ingresar cadena
        etiqueta_clave = ttk.Label(frame_principal, text="Cadena:", style="Estilo.TLabel")
        etiqueta_clave.grid(row=0, column=0, sticky="w")

        self.entrada_clave = ttk.Entry(frame_principal, width=20, font=("Arial", 12))
        self.entrada_clave.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Boton de buscar archivo
        boton_abrir = ttk.Button(frame_principal, text="Abrir archivo", style="Estilo.TButton",
                                        command=self.abrir_archivo)
        boton_abrir.grid(row=3, column=1, padx=10, pady=10, sticky="w")


# Ingresar contraseña
        etiqueta_contraseña = ttk.Label(frame_principal, text="Contraseña:", style="Estilo.TLabel")
        etiqueta_contraseña.grid(row=1, column=0, sticky="w")

        self.entrada_contraseña = ttk.Entry(frame_principal, width=20, font=("Arial", 12))
        self.entrada_contraseña.grid(row=1, column=1, padx=10, pady=5, sticky="w")



# Intgresar desplazamiento
        etiqueta_desplazamiento = ttk.Label(frame_principal, text="Desplazamiento:", style="Estilo.TLabel")
        etiqueta_desplazamiento.grid(row=2, column=0, sticky="w")

        self.entrada_desplazamiento = ttk.Entry(frame_principal, width=10, textvariable=self.desplazamiento,
                                                font=("Arial", 12))
        self.entrada_desplazamiento.grid(row=2, column=1, padx=10, pady=5, sticky="w")


        
# Generación de criptograma
        boton_generar = ttk.Button(frame_principal, text="Codificar criptograma", style="Estilo.TButton",
                                command=self.generar_criptograma)
        boton_generar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.texto_criptograma = tk.Text(frame_principal, width=40, height=6, font=("Arial", 12))
        self.texto_criptograma.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Boton de decodificar
        boton_comprobar = ttk.Button(frame_principal, text="Decodificar", style="Estilo.TButton",
                                    command=self.comprobar_criptograma)
        boton_comprobar.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Decodificación
        self.etiqueta_comprobacion = ttk.Label(frame_principal, text="", style="Estilo.TLabel")
        self.etiqueta_comprobacion.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.texto_decodificacion = tk.Text(frame_principal, width=40, height=6, font=("Arial", 12))
        self.texto_decodificacion.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Boton de descargar
        boton_descargar = ttk.Button(frame_principal, text="Descargar", style="Estilo.TButton",
                                    command=self.descargar_decodificacion)
        boton_descargar.grid(row=9, column=0, padx=10, pady=10, sticky="w")

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        with open(archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()
        self.entrada_clave.delete(0, tk.END)
        self.entrada_clave.insert(tk.END, contenido)

    def generar_criptograma(self):
        clave = self.entrada_clave.get().upper()
        contraseña = self.entrada_contraseña.get().upper()
        desplazamiento = int(self.desplazamiento.get())

        if not clave.strip() or not contraseña.strip() or not self.desplazamiento.get().strip():
            self.mostrar_notificacion("Rellenar todos los campos")
            return
        if not clave.strip():
            self.mostrar_notificacion("Ingresar clave")
            return
        if not contraseña.strip():
            self.mostrar_notificacion("Ingresar contraseña")
            return
        if not self.desplazamiento.get().strip():
            self.mostrar_notificacion("Ingresar desplazamiento")
            return

        criptograma = ""
        clave_idx = 0
        for letra in clave:
            if letra.isalpha():
                letra_sin_acento = self.remover_acentos(letra)
                desplazamiento_actual = (desplazamiento + clave_idx) % 26
                desplazamiento_letra = ord(contraseña[clave_idx % len(contraseña)]) - ord('A')
                desplazamiento_total = (desplazamiento_actual + desplazamiento_letra) % 26
                letra_criptograma = self.cifrar_cesar(letra_sin_acento, desplazamiento_total)
                criptograma = f"{criptograma}{letra_criptograma}"
                clave_idx += 1
            else:
                criptograma += letra
        self.texto_criptograma.delete("1.0", tk.END)
        self.texto_criptograma.insert(tk.END, criptograma)

    def comprobar_criptograma(self):
        criptograma = self.texto_criptograma.get("1.0", tk.END).strip()
        contraseña = self.entrada_contraseña.get().upper()
        desplazamiento = int(self.desplazamiento.get())

        if not criptograma.strip() or not contraseña.strip() or not self.desplazamiento.get().strip():
            self.mostrar_notificacion("Rellenar todos los campos")
            return
        if not criptograma.strip():
            self.mostrar_notificacion("Ingresar criptograma")
            return
        if not contraseña.strip():
            self.mostrar_notificacion("Ingresar contraseña")
            return
        if not self.desplazamiento.get().strip():
            self.mostrar_notificacion("Ingresar desplazamiento")
            return

        texto_original = ""
        clave_idx = 0
        for letra in criptograma:
            if letra.isalpha():
                letra_sin_acento = self.remover_acentos(letra)
                desplazamiento_actual = (desplazamiento + clave_idx) % 26
                desplazamiento_letra = ord(contraseña[clave_idx% len(contraseña)]) - ord('A')
                desplazamiento_total = (desplazamiento_actual + desplazamiento_letra) % 26
                letra_original = self.descifrar_cesar(letra_sin_acento, desplazamiento_total)
                texto_original = f"{texto_original}{letra_original}"
                clave_idx += 1
            else:
                texto_original += letra

        if texto_original == self.entrada_clave.get().upper():
            resultado = "El criptograma es correcto"
        else:
            resultado = "El criptograma es incorrecto"

        self.etiqueta_comprobacion.config(text=resultado)
        self.texto_decodificacion.delete("1.0", tk.END)
        self.texto_decodificacion.insert(tk.END, texto_original)

    def remover_acentos(self, letra):
        letra_nfd = unicodedata.normalize('NFD', letra)
        letra_sin_acento = ''.join(c for c in letra_nfd if unicodedata.category(c) != 'Mn')
        return letra_sin_acento

    def descargar_decodificacion(self):
        texto_decodificado = self.texto_decodificacion.get("1.0", tk.END)
        archivo_guardado = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if archivo_guardado is not None:
            archivo_guardado.write(texto_decodificado)
            archivo_guardado.close()

    @staticmethod
    def cifrar_cesar(letra, desplazamiento):
        if letra.isalpha():
            codigo_letra = ord(letra) - ord('A')
            codigo_cifrada = (codigo_letra + desplazamiento) % 26
            return chr(codigo_cifrada + ord('A'))
        return letra

    @staticmethod
    def descifrar_cesar(letra, desplazamiento):
        if letra.isalpha():
            codigo_letra = ord(letra) - ord('A')
            codigo_original = (codigo_letra - desplazamiento) % 26
            return chr(codigo_original + ord('A'))
        return letra

    def mostrar_notificacion(self, mensaje):
        self.etiqueta_comprobacion.config(text=mensaje)

    def run(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = CriptogramaApplication()
    app.run()
