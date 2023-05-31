import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('bolsas.db')
c = conn.cursor()

#Tabela de funcionários
c.execute('''CREATE TABLE IF NOT EXISTS funcionarios
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               email TEXT NOT NULL,
               codigo INTEGER UNIQUE NOT NULL,
               senha INTEGER NOT NULL,
               privacidade TEXT NOT NULL)''')

#Tabela de bolsas
c.execute('''CREATE TABLE IF NOT EXISTS bolsas
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               codigo TEXT UNIQUE NOT NULL,
               imagem TEXT,
               preco REAL)''')

#Mostrar POP-UP de mensagens
def show_success_message(message):
    messagebox.showinfo("Sucesso", message)

def show_error_message(message):
    messagebox.showerror("Erro", message)

def validate_login(codigo, senha):
    c.execute("SELECT privacidade FROM funcionarios WHERE codigo=? AND senha=?", (codigo, senha))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

#Tela de login
def show_login_screen():
    def login():
        codigo = codigo_entry.get()
        senha = senha_entry.get()
        privacidade = validate_login(codigo, senha)

        if privacidade == 'COMUM':
            show_comum_menu()
        elif privacidade == 'ADM':
            show_adm_menu()
        else:
            show_error_message("Código ou senha inválidos")

    login_window = tk.Tk()
    login_window.title("Login de Funcionários")

    codigo_label = tk.Label(login_window, text="Código:")
    codigo_label.pack()
    codigo_entry = tk.Entry(login_window)
    codigo_entry.pack()

    senha_label = tk.Label(login_window, text="Senha:")
    senha_label.pack()
    senha_entry = tk.Entry(login_window, show="*")
    senha_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack()

    login_window.mainloop()

#Tela de menu inicial
imagem_path = ""

def show_menu_screen(privacidade):
    def logout():
        show_login_screen()
        menu_window.destroy()

    menu_window = tk.Tk()
    menu_window.title("Menu Inicial")

    if privacidade == 'ADM':
        cadastro_func_button = tk.Button(menu_window, text="Cadastro de Funcionários", command=show_cadastro_funcionarios_screen)
        cadastro_func_button.pack()

        visualizacao_func_button = tk.Button(menu_window, text="Visualização de Funcionários", command=show_visualizacao_funcionarios_screen)
        visualizacao_func_button.pack()

        cadastro_bolsas_button = tk.Button(menu_window, text="Cadastro de Bolsas", command=show_cadastro_bolsas_screen)
        cadastro_bolsas_button.pack()

    visualizacao_bolsas_button = tk.Button(menu_window, text="Visualização do Catálogo de Bolsas", command=show_visualizacao_bolsas_screen)
    visualizacao_bolsas_button.pack()

    logout_button = tk.Button(menu_window, text="Encerrar Sessão", command=logout)
    logout_button.pack()

    menu_window.mainloop()

#Tela de cadastro de funcionários
def show_cadastro_funcionarios_screen():
    def save_funcionario():
        nome = nome_entry.get()
        email = email_entry.get()
        codigo = codigo_entry.get()
        senha = senha_entry.get()
        privacidade = privacidade_combobox.get()

        try:
            c.execute("INSERT INTO funcionarios (nome, email, codigo, senha, privacidade) VALUES (?, ?, ?, ?, ?)",
                      (nome, email, codigo, senha, privacidade))
            conn.commit()
            show_success_message("Funcionário cadastrado/atualizado com sucesso")
            cadastro_funcionarios_window.destroy()
        except sqlite3.Error as error:
            show_error_message("Erro ao cadastrar/atualizar o funcionário: " + str(error))

    cadastro_funcionarios_window = tk.Tk()
    cadastro_funcionarios_window.title("Cadastro de Funcionários")

    pesquisa_label = tk.Label(cadastro_funcionarios_window, text="Pesquisa:")
    pesquisa_label.pack()
    pesquisa_entry = tk.Entry(cadastro_funcionarios_window)
    pesquisa_entry.pack()

    nome_label = tk.Label(cadastro_funcionarios_window, text="Nome:")
    nome_label.pack()
    nome_entry = tk.Entry(cadastro_funcionarios_window)
    nome_entry.pack()

    email_label = tk.Label(cadastro_funcionarios_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(cadastro_funcionarios_window)
    email_entry.pack()

    codigo_label = tk.Label(cadastro_funcionarios_window, text="Código:")
    codigo_label.pack()
    codigo_entry = tk.Entry(cadastro_funcionarios_window)
    codigo_entry.pack()

    senha_label = tk.Label(cadastro_funcionarios_window, text="Senha:")
    senha_label.pack()
    senha_entry = tk.Entry(cadastro_funcionarios_window)
    senha_entry.pack()

    privacidade_label = tk.Label(cadastro_funcionarios_window, text="Privacidade:")
    privacidade_label.pack()
    privacidade_combobox = ttk.Combobox(cadastro_funcionarios_window, values=["COMUM", "ADM"])
    privacidade_combobox.pack()

    save_button = tk.Button(cadastro_funcionarios_window, text="Salvar/Atualizar", command=save_funcionario)
    save_button.pack()

    cadastro_funcionarios_window.mainloop()

#Tela de visualização de funcionários
def show_visualizacao_funcionarios_screen():
    global pesquisa_entry
    def search_funcionarios():
        pesquisa = pesquisa_entry.get()
        c.execute("SELECT * FROM funcionarios WHERE codigo=?", (pesquisa,))
        rows = c.fetchall()
        funcionarios_tree.delete(*funcionarios_tree.get_children())
        for row in rows:
            funcionarios_tree.insert("", tk.END, values=row)

    visualizacao_funcionarios_window = tk.Tk()
    visualizacao_funcionarios_window.title("Visualização de Funcionários")

    pesquisa_label = tk.Label(visualizacao_funcionarios_window, text="Pesquisa:")
    pesquisa_label.pack()
    pesquisa_entry = tk.Entry(visualizacao_funcionarios_window)
    pesquisa_entry.pack()

    search_button = tk.Button(visualizacao_funcionarios_window, text="Buscar", command=search_funcionarios)
    search_button.pack()

    funcionarios_tree = ttk.Treeview(visualizacao_funcionarios_window)
    funcionarios_tree["columns"] = ("Nome", "Email", "Código", "Senha", "Privacidade")
    funcionarios_tree.heading("#0", text="")
    funcionarios_tree.column("#0", width=0, stretch=tk.NO)
    funcionarios_tree.heading("Nome", text="Nome")
    funcionarios_tree.column("Nome", width=150, anchor=tk.W)
    funcionarios_tree.heading("Email", text="Email")
    funcionarios_tree.column("Email", width=200, anchor=tk.W)
    funcionarios_tree.heading("Código", text="Código")
    funcionarios_tree.column("Código", width=50, anchor=tk.CENTER)
    funcionarios_tree.heading("Senha", text="Senha")
    funcionarios_tree.column("Senha", width=50, anchor=tk.CENTER)
    funcionarios_tree.heading("Privacidade", text="Privacidade")
    funcionarios_tree.column("Privacidade", width=100, anchor=tk.CENTER)
    funcionarios_tree.pack()

    delete_button = tk.Button(visualizacao_funcionarios_window, text="Excluir", command=delete_funcionario)
    delete_button.pack()

    visualizacao_funcionarios_window.mainloop()

#Tela de visualização do catálogo de bolsas
pesquisa_entry = None

def show_visualizacao_bolsas_screen():
    global pesquisa_entry
    def search_bolsas():
        pesquisa = pesquisa_entry.get()
        c.execute("SELECT codigo, imagem, preco FROM bolsas WHERE codigo=?", (pesquisa,))
        rows = c.fetchall()
        bolsas_tree.delete(*bolsas_tree.get_children())
        for row in rows:
            bolsas_tree.insert("", tk.END, values=row)

    visualizacao_bolsas_window = tk.Tk()
    visualizacao_bolsas_window.title("Visualização do Catálogo de Bolsas")

    pesquisa_label = tk.Label(visualizacao_bolsas_window, text="Pesquisa:")
    pesquisa_label.pack()
    pesquisa_entry = tk.Entry(visualizacao_bolsas_window)
    pesquisa_entry.pack()

    search_button = tk.Button(visualizacao_bolsas_window, text="Buscar", command=search_bolsas)
    search_button.pack()

    bolsas_tree = ttk.Treeview(visualizacao_bolsas_window)
    bolsas_tree["columns"] = ("Código", "Imagem", "Preço")
    bolsas_tree.heading("#0", text="")
    bolsas_tree.column("#0", width=0, stretch=tk.NO)
    bolsas_tree.heading("Código", text="Código")
    bolsas_tree.column("Código", width=100, anchor=tk.CENTER)
    bolsas_tree.heading("Imagem", text="Imagem")
    bolsas_tree.column("Imagem", width=150, anchor=tk.CENTER)
    bolsas_tree.heading("Preço", text="Preço")
    bolsas_tree.column("Preço", width=100, anchor=tk.CENTER)
    bolsas_tree.pack()

    delete_button = tk.Button(visualizacao_bolsas_window, text="Excluir", command=delete_bolsa)
    delete_button.pack()

    visualizacao_bolsas_window.mainloop()

#Tela de cadastro de bolsas
def show_cadastro_bolsas_screen():
    def save_bolsa():
        codigo = codigo_entry.get()
        preco = preco_entry.get()

        try:
            c.execute("INSERT INTO bolsas (codigo, preco, imagem) VALUES (?, ?, ?)",
                      (codigo, preco, imagem_path))
            conn.commit()
            show_success_message("Bolsa cadastrada/atualizada com sucesso")
            cadastro_bolsas_window.destroy()
        except sqlite3.Error as error:
            show_error_message("Erro ao cadastrar/atualizar a bolsa: " + str(error))

    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.jpeg;*.png")])
        if file_path:
            global imagem_path
            imagem_path = file_path
            image = Image.open(file_path)
            image.thumbnail((150, 150))  # Redimensionar a imagem para uma visualização menor
            photo = ImageTk.PhotoImage(image)
            imagem_label.configure(image=photo)
            imagem_label.image = photo  # Manter uma referência para a imagem exibida

    cadastro_bolsas_window = tk.Tk()
    cadastro_bolsas_window.title("Cadastro de Bolsas")

    pesquisa_label = tk.Label(cadastro_bolsas_window, text="Pesquisa:")
    pesquisa_label.pack()
    pesquisa_entry = tk.Entry(cadastro_bolsas_window)
    pesquisa_entry.pack()

    codigo_label = tk.Label(cadastro_bolsas_window, text="Código:")
    codigo_label.pack()
    codigo_entry = tk.Entry(cadastro_bolsas_window)
    codigo_entry.pack()

    imagem_label = tk.Label(cadastro_bolsas_window, text="Imagem:")
    imagem_label.pack()

    upload_button = tk.Button(cadastro_bolsas_window, text="Upload de Imagem", command=upload_image)
    upload_button.pack()

    preco_label = tk.Label(cadastro_bolsas_window, text="Preço:")
    preco_label.pack()
    preco_entry = tk.Entry(cadastro_bolsas_window)
    preco_entry.pack()

    save_button = tk.Button(cadastro_bolsas_window, text="Salvar/Atualizar", command=save_bolsa)
    save_button.pack()

    cadastro_bolsas_window.mainloop()

# Função para excluir uma bolsa pelo código
def delete_bolsa():
    codigo = pesquisa_entry.get()

    try:
        c.execute("DELETE FROM bolsas WHERE codigo=?", (codigo,))
        conn.commit()
        show_success_message("Bolsa excluída com sucesso")
        visualizacao_bolsas_window.destroy()
        show_visualizacao_bolsas_screen()
    except sqlite3.Error as error:
        show_error_message("Erro ao excluir a bolsa: " + str(error))

# Função para excluir um funcionário pelo código
def delete_funcionario():
    codigo = pesquisa_entry.get()

    try:
        c.execute("DELETE FROM funcionarios WHERE codigo=?", (codigo,))
        conn.commit()
        show_success_message("Funcionário excluído com sucesso")
        visualizacao_funcionarios_window.destroy()
        show_visualizacao_funcionarios_screen()
    except sqlite3.Error as error:
        show_error_message("Erro ao excluir o funcionário: " + str(error))


#Tela de menu para o usuário COMUM
def show_comum_menu():
    menu_window = tk.Tk()
    menu_window.title("Menu Inicial - COMUM")

    visualizacao_bolsas_button = tk.Button(menu_window, text="Visualização do Catálogo de Bolsas", command=show_visualizacao_bolsas_screen)
    visualizacao_bolsas_button.pack()

    logout_button = tk.Button(menu_window, text="Encerrar Sessão", command=show_login_screen)
    logout_button.pack()

    menu_window.mainloop()

#Tela de menu para o usuário ADM
def show_adm_menu():
    menu_window = tk.Tk()
    menu_window.title("Menu Inicial - ADM")

    cadastro_func_button = tk.Button(menu_window, text="Cadastro de Funcionários", command=show_cadastro_funcionarios_screen)
    cadastro_func_button.pack()

    visualizacao_func_button = tk.Button(menu_window, text="Visualização de Funcionários", command=show_visualizacao_funcionarios_screen)
    visualizacao_func_button.pack()

    cadastro_bolsas_button = tk.Button(menu_window, text="Cadastro de Bolsas", command=show_cadastro_bolsas_screen)
    cadastro_bolsas_button.pack()

    visualizacao_bolsas_button = tk.Button(menu_window, text="Visualização do Catálogo de Bolsas", command=show_visualizacao_bolsas_screen)
    visualizacao_bolsas_button.pack()

    logout_button = tk.Button(menu_window, text="Encerrar Sessão", command=show_login_screen)
    logout_button.pack()

    menu_window.mainloop()

show_login_screen()

conn.close()
