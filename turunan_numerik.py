import tkinter as tk
import sympy as sp
from tkinter import ttk

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 800  
window_height = 700  
x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
window.configure(bg="#6994A8")
window.title("Turunan Numerik - Kelompok 4")

# frame
input_frame = ttk.Frame(window)
input_frame.pack(padx=30, pady=30, fill="x", expand=True)

# fungsi untuk perhitungan
def hitung_turunan(x, h, method, f):
    if method == "maju":
        return (f(x + h) - f(x)) / h
    elif method == "pusat":
        return (f(x + h) - f(x - h)) / (2 * h)
    elif method == "mundur":
        return (f(x) - f(x - h)) / h
    else:
        return (hitung_turunan(x, h, "pusat", f) + (hitung_turunan(x, h, "pusat", f) - hitung_turunan(x, 2*h, "pusat", f)) / 3)

def turunan_sejati(expr, x):
    x_symbolic = sp.symbols('x')
    derivative = sp.diff(expr, x_symbolic)
    return derivative.subs(x_symbolic, x)

def tampil_tabel(results, options, expr_turunan_sejati):
    global tree
    tree = ttk.Treeview(input_frame)
    tree["columns"] = ("x", *options, "turunan sejati")
    tree.heading("#0", text="")
    tree.column("#0", width=0)

    for col in tree["columns"]:
        tree.heading(col, text=col, anchor="center") 
        tree.column(col, width=100, anchor="center")

    for i, row in enumerate(results, 1):
        x = row[0]
        nilai_turunan_sejati = turunan_sejati(expr_turunan_sejati, x)
        tree.insert("", i,text="", values=row + [f"{nilai_turunan_sejati:.5f}"])

    tree.pack(padx=30, pady=10, fill="both", expand=True)

def reset():
    global tree
    input_a.delete(0, 'end')
    input_b.delete(0, 'end') 
    input_h.delete(0, 'end')
    input_persamaan.delete(0, 'end')
    label_turunan_sejati["text"] = ""
    try:
        tree.destroy()
        tree.pack_forget()
    except:
        pass
    
    global results
    results = []

def hitung():
    global results
    str_a = input_a.get()
    nilai_b = float(input_b.get())
    if str_a:
        nilai_a = float(str_a)
    else:
        nilai_a = nilai_b
    h = float(input_h.get())
    persamaan = input_persamaan.get()

    persamaan = persamaan.replace('^', '**')
    x_symbolic = sp.symbols('x')
    expr = sp.sympify(persamaan)

    results = []

    if nilai_a == nilai_b:
        x = nilai_b
        row_results = [round(x, 2)] 
        for metode in options:
            nilai = hitung_turunan(x, h, metode, lambda x: expr.subs(x_symbolic, x))
            row_results.append(f"{nilai:.5f}")
        results.append(row_results)

    else:
        x = nilai_a
        while x <= nilai_b:
            row_results = [round(x, 2)]
            for metode in options:
                nilai = hitung_turunan(x, h, metode, lambda x: expr.subs(x_symbolic, x))
                row_results.append(f"{nilai:.5f}")
            results.append(row_results)
            x += h

    tampil_tabel(results, options, expr)

    label_turunan_sejati["text"] = f"Turunan dari persamaan: {sp.diff(expr, x_symbolic)}"


label_judul = ttk.Label(input_frame, text="Aplikasi Perhitungan Turunan Numerik", font=('Arial', 16), anchor="w")
label_judul.pack(padx=30, pady=10, fill="x", expand=True)

label_subjudul = ttk.Label(input_frame, text="1.Metode Selisih Maju", anchor="w")  
label_subjudul.pack(padx=30, fill="x", expand=True)

label_subjudul2 = ttk.Label(input_frame, text="2.Metode Selisih Pusat", anchor="w")  
label_subjudul2.pack(padx=30, fill="x", expand=True)

label_subjudul3 = ttk.Label(input_frame, text="3.Metode Selisih Mundur", anchor="w")  
label_subjudul3.pack(padx=30, fill="x", expand=True)

label_subjudul4 = ttk.Label(input_frame, text="4.Metode Ekstrapolasi Richardson", anchor="w")  
label_subjudul4.pack(padx=30, pady=(0,20), fill="x", expand=True)

# 1. nilai awal (a)
label_a = ttk.Label(input_frame, text="Masukkan nilai awal (a) :")
label_a.pack(padx=30, fill="x", expand=True)

input_a = ttk.Entry(input_frame)
input_a.pack(padx=30, fill="x", expand=True)

# 2. nilai akhir (b)
label_b = ttk.Label(input_frame, text="Masukkan nilai akhir (b) :")
label_b.pack(padx=30, fill="x", expand=True)

input_b = ttk.Entry(input_frame)
input_b.pack(padx=30, fill="x", expand=True)

# 3. nilai selisih (h)
label_h = ttk.Label(input_frame, text="Masukkan nilai selang (h) :")
label_h.pack(padx=30, fill="x", expand=True)

input_h = ttk.Entry(input_frame)
input_h.pack(padx=30, fill="x", expand=True)

# 4. persamaan
label_persamaan = ttk.Label(input_frame, text="Masukkan Persamaan dengan x sebagai variabel :")
label_persamaan.pack(padx=30, fill="x", expand=True)

input_persamaan = ttk.Entry(input_frame)
input_persamaan.pack(padx=30, fill="x", expand=True)

# 5. tombol hitung 
tombol_hitung = ttk.Button(input_frame, text="Hitung", command=hitung)
tombol_hitung.pack(fill="x", expand=True, padx=30, pady=10)

# 6. tombol reset
tombol_reset = ttk.Button(input_frame, text="Reset", command=reset)
tombol_reset.pack(fill="x", expand=True, padx=30)

# 7. turunan f'(x) sejati
label_turunan_sejati = ttk.Label(input_frame, text="")
label_turunan_sejati.pack(padx=30, fill="x", expand=True)

# 8. opsi metode
options = ["maju", "pusat", "mundur", "ekstrapolasi"]
method = tk.StringVar(window)
method.set(options[0])
optionmenu = tk.OptionMenu(input_frame, method, *options)

window.mainloop()