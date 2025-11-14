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

# Executa a criação da tabela ao iniciar o programa (Estrutura do BD)
criar_tabela() 

def inserir_jogada(resultado_string):
    """Insere o resultado da jogada no banco de dados (Lógica INSERT)."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Requisito: O clique do botão executa corretamente o INSERT
    cursor.execute("INSERT INTO jogadas (resultado) VALUES (?)", (resultado_string,))
    
    # Requisito: Uso correto de conn.commit()
    conn.commit()
    conn.close()

def selecionar_jogadas():
    """Consulta todas as jogadas para popular o histórico (Lógica SELECT)."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Requisito: Consultar todos os dados da tabela jogadas (SELECT id, resultado FROM jogadas ORDER BY id DESC)
    cursor.execute("SELECT id, resultado FROM jogadas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def sortear_frutas():
    """Sorteia 3 frutas e formata a string de auditoria."""
    
    # Requisito: Usar random.choice para sortear 3 frutas
    f1 = random.choice(FRUTAS)
    f2 = random.choice(FRUTAS)
    f3 = random.choice(FRUTAS)
    
    # Requisito: Lógica de Vitória (if f1 == f2 == f3)
    venceu = (f1 == f2 == f3)
    jogada_str = f"{f1} - {f2} - {f3}"
    
    # Requisito: Formatar a string única para auditoria
    if venceu:
        # Formato de string para Vencedor
        resultado_auditoria = f" 🏆 VITÓRIA: {jogada_str} 🏆 " 
    else:
        # Formato de string para Perdedor
        resultado_auditoria = f"Jogada: {jogada_str}"

    return f1, f2, f3, resultado_auditoria, venceu

def popular_treeview():
    """Limpa o Treeview e o preenche com os dados do banco (SELECT)."""
    
    # Requisito: Limpar o Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Requisito: Populando o Treeview com dados do SELECT
    dados = selecionar_jogadas()
    for id_jogada, resultado_str in dados:
        tree.insert('', END, values=(id_jogada, resultado_str))


def executar_sorteio():
    """Função principal ativada pelo botão 'Sortear!'."""
    
    # 1. Lógica: Sortear e verificar
    f1, f2, f3, resultado_auditoria, venceu = sortear_frutas()
    
    # 2. Frontend: Atualizar as Labels de frutas
    fruta_var1.set(f1)
    fruta_var2.set(f2)
    fruta_var3.set(f3)

    # 3. Backend: INSERT da string de auditoria
    inserir_jogada(resultado_auditoria)
    
    # 4. Frontend: Feedback de vitória com messagebox (apenas se venceu)
    if venceu:
        messagebox.showinfo("🎉 Parabéns!", "TRÊS IGUAIS! Você teve uma VITÓRIA!")
        
    # 5. Frontend: Atualizar o histórico após o INSERT (RF-03)
    popular_treeview