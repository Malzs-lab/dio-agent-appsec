"""
Laboratório de Segurança DIO - Código Refatorado e Protegido (Secure by Design)
Mitigações Aplicadas:
1. Consultas Parametrizadas (Prepared Statements - Imune a CWE-89)
2. Hashing Criptográfico com Salt Único (PBKDF2-HMAC-SHA256 - Imune a OWASP A02:2021)
3. Validação e Sanitização Estrita de Entrada (Whitelisting de caracteres)
4. Falha Segura (Fail-Safe Defaults)
"""

import sqlite3
import hashlib
import os
import re

def gerar_hash_senha(senha: str, salt: bytes = None) -> tuple[str, bytes]:
    """Gera um digest PBKDF2-HMAC-SHA256 seguro com 100.000 iterações e salt de 16 bytes."""
    if salt is None:
        salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=senha.encode('utf-8'),
        salt=salt,
        iterations=100_000
    )
    return hash_bytes.hex(), salt

def verificar_senha(senha_fornecida: str, hash_esperado: str, salt: bytes) -> bool:
    """Verifica se a senha fornecida coincide com o hash em tempo constante."""
    hash_calculado, _ = gerar_hash_senha(senha_fornecida, salt)
    import hmac
    return hmac.compare_digest(hash_calculado, hash_esperado)

def inicializar_banco_seguro():
    """Cria um banco SQLite com senhas armazenadas exclusivamente em formato de hash criptográfico."""
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt BLOB NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    # Criar admin e aluno com hashes protegidos
    h_admin, s_admin = gerar_hash_senha("Sup3rS3cr3tP@ss")
    h_aluno, s_aluno = gerar_hash_senha("dio2026")
    
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
        ("admin", h_admin, s_admin, "administrator")
    )
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
        ("aluno_dio", h_aluno, s_aluno, "student")
    )
    conexao.commit()
    return conexao

def validar_formato_usuario(usuario: str) -> bool:
    """Valida se o nome de usuário segue o padrão alfanumérico seguro (3 a 30 caracteres)."""
    if not isinstance(usuario, str):
        return False
    # Apenas letras, números e underline
    padrao = r'^[a-zA-Z0-9_]{3,30}$'
    return bool(re.match(padrao, usuario))

def login_seguro(conexao, usuario_input: str, senha_input: str) -> bool:
    """
    AUTENTICAÇÃO SEGURA:
    1. Validação prévia de formato do usuário (Shift-Left / Input Hygiene).
    2. Consulta parametrizada com placeholder '?' impedindo injeção SQL no motor.
    3. Verificação de senha usando PBKDF2 e comparação em tempo constante contra timing attacks.
    """
    cursor = conexao.cursor()
    
    # 1. Validação de Entrada
    if not validar_formato_usuario(usuario_input):
        print(f"[-] Entrada rejeitada pelo filtro de formato seguro: '{usuario_input}'")
        return False
    
    # 2. ✅ CONSULTA PARAMETRIZADA: O motor SQL separa dados de código
    query_parametrizada = "SELECT id, username, password_hash, salt, role FROM users WHERE username = ?"
    print(f"\n[DEBUG DA CONSULTA PREPARADA]:\n{query_parametrizada} com parâmetro: ('{usuario_input}',)")
    
    try:
        cursor.execute(query_parametrizada, (usuario_input,))
        registro = cursor.fetchone()
        
        if not registro:
            print("[-] Falha na autenticação: Usuário não localizado.")
            return False
        
        user_id, username, hash_banco, salt_banco, role = registro
        
        # 3. Verificação Criptográfica da Senha
        if verificar_senha(senha_input, hash_banco, salt_banco):
            print(f"[+] Autenticação BEM-SUCEDIDA! Logado como ID={user_id}, Usuário='{username}', Perfil='{role}'")
            return True
        else:
            print("[-] Falha na autenticação: Senha incorreta.")
            return False
            
    except sqlite3.Error as erro:
        print(f"[!] Erro operacional seguro (Falha Segura): {erro}")
        return False

if __name__ == "__main__":
    print("=" * 65)
    print("   LABORATÓRIO DE TESTE DE APPSEC: APLICAÇÃO SEGURA (DEFESA)     ")
    print("=" * 65)
    
    db = inicializar_banco_seguro()
    
    # Teste 1: Autenticação Legítima
    print("\n--- TESTE 1: Tentativa com credencial válida ---")
    login_seguro(db, "aluno_dio", "dio2026")
    
    # Teste 2: Tentativa com senha errada
    print("\n--- TESTE 2: Tentativa com senha errada ---")
    login_seguro(db, "aluno_dio", "senha_incorreta_123")
    
    # Teste 3: Tentativa de SQL Injection
    print("\n--- TESTE 3: Tentativa de Bypass com payload ' OR '1'='1 ---")
    payload_ataque = "' OR '1'='1"
    login_seguro(db, payload_ataque, "qualquer_coisa")
    
    # Teste 4: Tentativa de Bypass com comentário
    print("\n--- TESTE 4: Tentativa de Bypass direcionado ao Admin (admin' --) ---")
    payload_admin = "admin' --"
    login_seguro(db, payload_admin, "senha_ignorada")
