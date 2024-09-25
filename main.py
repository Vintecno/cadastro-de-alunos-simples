import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect('database.db')

# Função para criar as abas e a treeview
def create_tab(tab_control, table_name, columns):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=table_name.capitalize())

    # Treeview
    tree = ttk.Treeview(tab, columns=columns, show="headings")
    tree.pack(expand=True, fill='both')

    for col in columns:
        tree.heading(col, text=col)

    # Botões
    if table_name == "alunos":
        ttk.Button(tab, text="Inserir", command=lambda: insert_aluno(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Editar", command=lambda: edit_aluno(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Excluir", command=lambda: delete_record(tree, "alunos")).pack(side=tk.LEFT)
    elif table_name == "cursos":
        ttk.Button(tab, text="Inserir", command=lambda: insert_curso(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Editar", command=lambda: edit_curso(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Excluir", command=lambda: delete_record(tree, "cursos")).pack(side=tk.LEFT)
    elif table_name == "matriculas":
        ttk.Button(tab, text="Inserir", command=lambda: insert_matricula(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Editar", command=lambda: edit_matricula(tree)).pack(side=tk.LEFT)
        ttk.Button(tab, text="Excluir", command=lambda: delete_record(tree, "matriculas")).pack(side=tk.LEFT)

    refresh_tree(tree, table_name)

# Função para atualizar a treeview
def refresh_tree(tree, table_name):
    for item in tree.get_children():
        tree.delete(item)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

# Funções de Inserir, Editar e Excluir para Alunos
def insert_aluno(tree):
    insert_window = tk.Toplevel(root)
    insert_window.title("Inserir Aluno")

    tk.Label(insert_window, text="CPF").grid(row=0, column=0)
    cpf_entry = tk.Entry(insert_window)
    cpf_entry.grid(row=0, column=1)

    tk.Label(insert_window, text="Nome").grid(row=1, column=0)
    nome_entry = tk.Entry(insert_window)
    nome_entry.grid(row=1, column=1)

    tk.Label(insert_window, text="Data de Nascimento").grid(row=2, column=0)
    data_nasc_entry = DateEntry(insert_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_nasc_entry.grid(row=2, column=1)

    tk.Label(insert_window, text="E-mail").grid(row=3, column=0)
    email_entry = tk.Entry(insert_window)
    email_entry.grid(row=3, column=1)

    tk.Label(insert_window, text="Endereço").grid(row=4, column=0)
    endereco_entry = tk.Entry(insert_window)
    endereco_entry.grid(row=4, column=1)

    tk.Label(insert_window, text="Telefone").grid(row=5, column=0)
    telefone_entry = tk.Entry(insert_window)
    telefone_entry.grid(row=5, column=1)

    def save_aluno():
        cpf = cpf_entry.get()
        nome = nome_entry.get()
        data_nasc = data_nasc_entry.get()
        email = email_entry.get()
        endereco = endereco_entry.get()
        telefone = telefone_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alunos (cpf, nome, data_nasc, email, endereco, telefone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cpf, nome, data_nasc, email, endereco, telefone))
        conn.commit()
        conn.close()
        insert_window.destroy()
        refresh_tree(tree, "alunos")

    tk.Button(insert_window, text="Salvar", command=save_aluno).grid(row=6, columnspan=2)

def edit_aluno(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecione", "Selecione um aluno para editar.")
        return

    item = tree.item(selected_item)
    cpf = item['values'][0]

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Aluno")

    tk.Label(edit_window, text="CPF").grid(row=0, column=0)
    cpf_entry = tk.Entry(edit_window)
    cpf_entry.insert(0, cpf)
    cpf_entry.grid(row=0, column=1)
    cpf_entry.config(state='disabled')

    tk.Label(edit_window, text="Nome").grid(row=1, column=0)
    nome_entry = tk.Entry(edit_window)
    nome_entry.insert(0, item['values'][1])
    nome_entry.grid(row=1, column=1)

    tk.Label(edit_window, text="Data de Nascimento").grid(row=2, column=0)
    data_nasc_entry = DateEntry(edit_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    data_nasc_entry.insert(0, item['values'][2])  # Ajuste para data
    data_nasc_entry.grid(row=2, column=1)

    tk.Label(edit_window, text="E-mail").grid(row=3, column=0)
    email_entry = tk.Entry(edit_window)
    email_entry.insert(0, item['values'][3])
    email_entry.grid(row=3, column=1)

    tk.Label(edit_window, text="Endereço").grid(row=4, column=0)
    endereco_entry = tk.Entry(edit_window)
    endereco_entry.insert(0, item['values'][4])
    endereco_entry.grid(row=4, column=1)

    tk.Label(edit_window, text="Telefone").grid(row=5, column=0)
    telefone_entry = tk.Entry(edit_window)
    telefone_entry.insert(0, item['values'][5])
    telefone_entry.grid(row=5, column=1)

    def save_edit_aluno():
        nome = nome_entry.get()
        data_nasc = data_nasc_entry.get()
        email = email_entry.get()
        endereco = endereco_entry.get()
        telefone = telefone_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE alunos SET nome=?, data_nasc=?, email=?, endereco=?, telefone=?
            WHERE cpf=?
        ''', (nome, data_nasc, email, endereco, telefone, cpf))
        conn.commit()
        conn.close()
        edit_window.destroy()
        refresh_tree(tree, "alunos")

    tk.Button(edit_window, text="Salvar", command=save_edit_aluno).grid(row=6, columnspan=2)

# Funções de Inserir, Editar e Excluir para Cursos
def insert_curso(tree):
    insert_window = tk.Toplevel(root)
    insert_window.title("Inserir Curso")

    tk.Label(insert_window, text="Nome").grid(row=0, column=0)
    nome_entry = tk.Entry(insert_window)
    nome_entry.grid(row=0, column=1)

    tk.Label(insert_window, text="Descrição").grid(row=1, column=0)
    descricao_entry = tk.Entry(insert_window)
    descricao_entry.grid(row=1, column=1)

    tk.Label(insert_window, text="Carga Horária").grid(row=2, column=0)
    carga_horaria_entry = tk.Entry(insert_window)
    carga_horaria_entry.grid(row=2, column=1)

    def save_curso():
        nome = nome_entry.get()
        descricao = descricao_entry.get()
        carga_horaria = carga_horaria_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cursos (nome, descricao, carga_horaria)
            VALUES (?, ?, ?)
        ''', (nome, descricao, carga_horaria))
        conn.commit()
        conn.close()
        insert_window.destroy()
        refresh_tree(tree, "cursos")

    tk.Button(insert_window, text="Salvar", command=save_curso).grid(row=3, columnspan=2)

def edit_curso(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecione", "Selecione um curso para editar.")
        return

    item = tree.item(selected_item)
    nome = item['values'][0]

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Curso")

    tk.Label(edit_window, text="Nome").grid(row=0, column=0)
    nome_entry = tk.Entry(edit_window)
    nome_entry.insert(0, nome)
    nome_entry.grid(row=0, column=1)
    nome_entry.config(state='disabled')

    tk.Label(edit_window, text="Descrição").grid(row=1, column=0)
    descricao_entry = tk.Entry(edit_window)
    descricao_entry.insert(0, item['values'][1])
    descricao_entry.grid(row=1, column=1)

    tk.Label(edit_window, text="Carga Horária").grid(row=2, column=0)
    carga_horaria_entry = tk.Entry(edit_window)
    carga_horaria_entry.insert(0, item['values'][2])
    carga_horaria_entry.grid(row=2, column=1)

    def save_edit_curso():
        descricao = descricao_entry.get()
        carga_horaria = carga_horaria_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE cursos SET descricao=?, carga_horaria=?
            WHERE nome=?
        ''', (descricao, carga_horaria, nome))
        conn.commit()
        conn.close()
        edit_window.destroy()
        refresh_tree(tree, "cursos")

    tk.Button(edit_window, text="Salvar", command=save_edit_curso).grid(row=3, columnspan=2)

# Funções de Inserir, Editar e Excluir para Matrículas
def insert_matricula(tree):
    insert_window = tk.Toplevel(root)
    insert_window.title("Inserir Matrícula")

    tk.Label(insert_window, text="CPF do Aluno").grid(row=0, column=0)
    cpf_entry = tk.Entry(insert_window)
    cpf_entry.grid(row=0, column=1)

    tk.Label(insert_window, text="Nome do Curso").grid(row=1, column=0)
    curso_entry = tk.Entry(insert_window)
    curso_entry.grid(row=1, column=1)

    def save_matricula():
        cpf = cpf_entry.get()
        curso = curso_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO matriculas (aluno_cpf, curso_nome)
            VALUES (?, ?)
        ''', (cpf, curso))
        conn.commit()
        conn.close()
        insert_window.destroy()
        refresh_tree(tree, "matriculas")

    tk.Button(insert_window, text="Salvar", command=save_matricula).grid(row=2, columnspan=2)

def edit_matricula(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecione", "Selecione uma matrícula para editar.")
        return

    item = tree.item(selected_item)

    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Matrícula")

    tk.Label(edit_window, text="CPF do Aluno").grid(row=0, column=0)
    cpf_entry = tk.Entry(edit_window)
    cpf_entry.insert(0, item['values'][1])
    cpf_entry.grid(row=0, column=1)

    tk.Label(edit_window, text="Nome do Curso").grid(row=1, column=0)
    curso_entry = tk.Entry(edit_window)
    curso_entry.insert(0, item['values'][2])
    curso_entry.grid(row=1, column=1)

    def save_edit_matricula():
        cpf = cpf_entry.get()
        curso = curso_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE matriculas SET aluno_cpf=?, curso_nome=?
            WHERE id=?
        ''', (cpf, curso, item['values'][0]))
        conn.commit()
        conn.close()
        edit_window.destroy()
        refresh_tree(tree, "matriculas")

    tk.Button(edit_window, text="Salvar", command=save_edit_matricula).grid(row=2, columnspan=2)

# Função para excluir um registro
def delete_record(tree, table_name):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selecione", "Selecione um registro para excluir.")
        return


    if not messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir este registro?"):
        return

    item = tree.item(selected_item)
    if table_name == "alunos":
        cpf = item['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alunos WHERE cpf=?", (cpf,))
        conn.commit()
        conn.close()
    elif table_name == "cursos":
        nome = item['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE nome=?", (nome,))
        conn.commit()
        conn.close()
    elif table_name == "matriculas":
        matricula_id = item['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM matriculas WHERE id=?", (matricula_id,))
        conn.commit()
        conn.close()
    
    refresh_tree(tree, table_name)

# Criação da janela principal
root = tk.Tk()
root.title("Sistema de Gerenciamento de Alunos e Cursos")

tab_control = ttk.Notebook(root)
create_tab(tab_control, "alunos", ["cpf", "nome", "data_nasc", "email", "endereco", "telefone"])
create_tab(tab_control, "cursos", ["nome", "descricao", "carga_horaria"])
create_tab(tab_control, "matriculas", ["id", "aluno_cpf", "curso_nome"])

# Alterar os nomes das colunas da aba de alunos
tab_control.tab(0, text="Alunos")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("cpf", text="CPF")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("nome", text="Nome")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("data_nasc", text="Data de Nascimento")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("email", text="E-mail")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("endereco", text="Endereço")
tab_control.nametowidget(tab_control.tabs()[0]).children["!treeview"].heading("telefone", text="Telefone")

# Alterar os nomes das colunas da aba de cursos
tab_control.tab(1, text="Cursos")
tab_control.nametowidget(tab_control.tabs()[1]).children["!treeview"].heading("nome", text="Nome")
tab_control.nametowidget(tab_control.tabs()[1]).children["!treeview"].heading("descricao", text="Descrição")
tab_control.nametowidget(tab_control.tabs()[1]).children["!treeview"].heading("carga_horaria", text="Carga Horária")

# Alterar os nomes das colunas da aba de matriculas
tab_control.tab(2, text="Matrículas")
tab_control.nametowidget(tab_control.tabs()[2]).children["!treeview"].heading("id", text="Matrícula")
tab_control.nametowidget(tab_control.tabs()[2]).children["!treeview"].heading("aluno_cpf", text="CPF")
tab_control.nametowidget(tab_control.tabs()[2]).children["!treeview"].heading("curso_nome", text="Curso")

tab_control.pack(expand=True, fill='both')

root.mainloop()
