import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Criar tabela de alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            cpf INTEGER PRIMARY KEY NOT NULL,
            nome TEXT NOT NULL,
            data_nasc TEXT,
            email TEXT,
            endereco TEXT,
            telefone TEXT
        )
    ''')

    # Criar tabela de cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            nome TEXT PRIMARY KEY NOT NULL,
            descricao TEXT,
            carga_horaria INTEGER
        )
    ''')

    # Criar tabela de matriculas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_cpf INTEGER NOT NULL,
            curso_nome TEXT NOT NULL,
            FOREIGN KEY (aluno_cpf) REFERENCES alunos (cpf),
            FOREIGN KEY (curso_nome) REFERENCES cursos (nome)
        )
    ''')

    print("Tabelas criadas com sucesso")
    conn.commit()
    conn.close()

create_tables()
