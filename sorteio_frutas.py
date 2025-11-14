import sqlite3
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

NOME_DB = 'sorteio.db' 
FRUTAS = [' 🍎 ', ' 🍌 ', ' 🍒 ', ' 🍇 ', ' 🍓 '] 

def conectar_db():
    """Cria a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(NOME_DB)
    return conn

def criar_tabela():
    """Cria a tabela 'jogadas' se ela ainda não existir."""
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resultado TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Executa a criação da tabela ao iniciar o programa
criar_tabela() 

def inserir_jogada(resultado_string):
    """Insere o resultado da jogada no banco de dados (Lógica INSERT)."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Executa o INSERT
    cursor.execute("INSERT INTO jogadas (resultado) VALUES (?)", (resultado_string,))

    conn.commit()
    conn.close()

def selecionar_jogadas():
    """Consulta todas as jogadas para popular o histórico (Lógica SELECT)."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Consulta todos os dados, ordenando pelos mais recentes
    cursor.execute("SELECT id, resultado FROM jogadas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def sortear_frutas():
    """Sorteia 3 frutas e formata a string de auditoria."""
    
    # Usa random.choice para sortear 3 frutas
    f1 = random.choice(FRUTAS)
    f2 = random.choice(FRUTAS)
    f3 = random.choice(FRUTAS)
    
    # Lógica de Vitória (f1 == f2 == f3)
    venceu = (f1 == f2 == f3)
    jogada_str = f"{f1} - {f2} - {f3}"
    
    if venceu:
        resultado_auditoria = f" 🏆 VITÓRIA: {jogada_str} 🏆 " 
    else:
        resultado_auditoria = f"Jogada: {jogada_str}"

    return f1, f2, f3, resultado_auditoria, venceu


def popular_treeview():
    """Limpa o Treeview e o preenche com os dados do banco (SELECT)."""
    for item in tree.get_children():
        tree.delete(item)

    dados = selecionar_jogadas()
    for id_jogada, resultado_str in dados:
        tree.insert('', END, values=(id_jogada, resultado_str))


def executar_sorteio():
    """Função principal ativada pelo botão 'Sortear!'."""
    f1, f2, f3, resultado_auditoria, venceu = sortear_frutas()
    
    fruta_var1.set(f1)
    fruta_var2.set(f2)
    fruta_var3.set(f3)

    inserir_jogada(resultado_auditoria)
    if venceu:
        messagebox.showinfo("🎉 Parabéns!", "TRÊS IGUAIS! Você teve uma VITÓRIA!")
    popular_treeview()


# criando a tela
janela_principal = ttk.Window(themename="darkly")
janela_principal.title("🎰 Sorteio de Frutas")
janela_principal.geometry("650x700")
ttk.Label(janela_principal, text="Sorteio de Frutas", font=('Helvetica', 24, 'bold'), bootstyle="primary").pack(pady=(20, 10))

frutas_frame = ttk.Frame(janela_principal)
frutas_frame.pack(pady=40)

fruta_var1 = ttk.StringVar(value="❓")
fruta_var2 = ttk.StringVar(value="❓")
fruta_var3 = ttk.StringVar(value="❓")

fonte_frutas = ('Helvetica', 70, 'bold')

# label para exibir as frutas
ttk.Label(frutas_frame, textvariable=fruta_var1, font=fonte_frutas, bootstyle="info").pack(side=LEFT, padx=20)
ttk.Label(frutas_frame, textvariable=fruta_var2, font=fonte_frutas, bootstyle="info").pack(side=LEFT, padx=20)
ttk.Label(frutas_frame, textvariable=fruta_var3, font=fonte_frutas, bootstyle="info").pack(side=LEFT, padx=20)

#fazendo os botões

# botão para sortear
botao_sortear = ttk.Button(janela_principal, text="Sortear!", bootstyle="success", command=executar_sorteio)
botao_sortear.pack(pady=30, ipadx=40, ipady=10)

ttk.Label(janela_principal, text="Histórico de Jogadas", font=('Helvetica', 16)).pack(pady=10)

# ttk.Treeview para exibir o histórico de jogadas
colunas = ("ID", "Resultado da Jogada")
tree = ttk.Treeview(janela_principal, columns=colunas, show='headings', bootstyle="dark") 
tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Configuração das Colunas
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Resultado da Jogada", text="Resultado da Jogada", anchor=W)
tree.column("ID", width=50, anchor=CENTER, stretch=NO)
tree.column("Resultado da Jogada", width=500, anchor=W)


# fazendo código rodar
if __name__ == '__main__':
    # Popula o Treeview com dados existentes ao abrir a tela
    popular_treeview() 
    janela_principal.mainloop()