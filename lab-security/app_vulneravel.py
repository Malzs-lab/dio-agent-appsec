"""
Laboratório de Segurança DIO - Código Vulnerável a Injeção de SQL (CWE-89 / MITRE T1190)
Finalidade: Demonstração e estudo prático de AppSec em ambiente de laboratório isolado.
"""

import sqlite3

def inicializar_banco_lab():
    """Cria um banco SQLite em memória com tabela de usuários para teste."""
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    # Usuário de teste da aplicação
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'Sup3rS3cr3tP@ss', 'administrator')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('aluno_dio', 'dio2026', 'student')")
    conexao.commit()
    return conexao

def login_vulneravel(conexao, usuario_input, senha_input):
    """
    FALHA CRÍTICA DE APPSEC:
    Concatenação direta de variáveis externas na string de consulta SQL.
    Permite que o atacante quebre a semântica da consulta e injete instruções lógicas.
    """
    cursor = conexao.cursor()
    
    # ❌ VULNERABILIDADE: Uso de f-string montando o comando SQL
    query_insegura = f"SELECT id, username, role FROM users WHERE username = '{usuario_input}' AND password = '{senha_input}'"
    
    print(f"\n[DEBUG DA CONSULTA EXECUTADA]:\n{query_insegura}")
    
    try:
        cursor.execute(query_insegura)
        usuario = cursor.fetchone()
        if usuario:
            print(f"[+] Autenticação BEM-SUCEDIDA! Logado como ID={usuario[0]}, Usuário='{usuario[1]}', Perfil='{usuario[2]}'")
            return True
        else:
            print("[-] Falha na autenticação: Credenciais incorretas.")
            return False
    except sqlite3.OperationalError as erro:
        print(f"[!] Erro de Sintaxe SQL disparado pelo banco: {erro}")
        return False

if __name__ == "__main__":
    print("=" * 65)
    print("   LABORATÓRIO DE TESTE DE APPSEC: APLICAÇÃO VULNERÁVEL (SQLi)   ")
    print("=" * 65)
    
    db = inicializar_banco_lab()
    
    # Teste 1: Autenticação Legítima
    print("\n--- TESTE 1: Tentativa com credencial válida ---")
    login_vulneravel(db, "aluno_dio", "dio2026")
    
    # Teste 2: Tentativa com senha errada
    print("\n--- TESTE 2: Tentativa com senha errada ---")
    login_vulneravel(db, "aluno_dio", "senha_incorreta_123")
    
    # Teste 3: Ataque de SQL Injection (Bypass de Autenticação)
    print("\n--- TESTE 3: Ataque de SQL Injection (Bypass com payload ' OR '1'='1) ---")
    payload_ataque = "' OR '1'='1"
    login_vulneravel(db, payload_ataque, "qualquer_coisa")
    
    # Teste 4: Ataque com Comentário de Fim de Linha
    print("\n--- TESTE 4: Ataque de Bypass direcionado ao Admin (admin' --) ---")
    payload_admin = "admin' --"
    login_vulneravel(db, payload_admin, "senha_ignorada")
