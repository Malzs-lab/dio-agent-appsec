"""
Suite de Testes Automatizados de AppSec: Validação de Mitigação de SQL Injection
Framework: unittest nativo do Python (sem dependências externas)
Objetivo:
1. Comprovar que o código vulnerável (app_vulneravel.py) falha no teste de segurança.
2. Comprovar que o código seguro (app_seguro.py) bloqueia todos os vetores de injeção.
"""

import unittest
from app_vulneravel import inicializar_banco_lab as init_vuln_db, login_vulneravel
from app_seguro import inicializar_banco_seguro as init_sec_db, login_seguro

class TesteSegurancaSQLInjection(unittest.TestCase):
    
    def setUp(self):
        """Inicializa instâncias isoladas em memória para cada teste."""
        self.db_vuln = init_vuln_db()
        self.db_sec = init_sec_db()
        
        # Payloads clássicos de injeção SQL (CWE-89 / OWASP A03 / MITRE T1190)
        self.payload_tautologia = "' OR '1'='1"
        self.payload_comentario = "admin' --"
        self.payload_union = "' UNION SELECT 99, 'hacked', 'admin' --"

    # =========================================================================
    # TESTES NO CÓDIGO VULNERÁVEL (Demonstração da Falha)
    # =========================================================================
    
    def test_vuln_login_legitimo_funciona(self):
        """Usuário legítimo deve conseguir logar."""
        resultado = login_vulneravel(self.db_vuln, "aluno_dio", "dio2026")
        self.assertTrue(resultado)

    def test_vuln_falha_de_seguranca_bypass_tautologia(self):
        """
        ALERTA DE SEGURANÇA:
        No código vulnerável, o payload "' OR '1'='1" consegue fazer login
        mesmo sem saber nenhuma senha!
        """
        resultado = login_vulneravel(self.db_vuln, self.payload_tautologia, "senha_falsa")
        # Confirma que a vulnerabilidade existe (retorna True indevidamente)
        self.assertTrue(resultado, "A vulnerabilidade de SQLi permitiu o bypass indevido no código inseguro!")

    def test_vuln_falha_de_seguranca_bypass_admin(self):
        """No código vulnerável, 'admin' -- faz login como admin sem senha."""
        resultado = login_vulneravel(self.db_vuln, self.payload_comentario, "senha_falsa")
        self.assertTrue(resultado, "A vulnerabilidade permitiu sequestro de sessão do admin!")

    # =========================================================================
    # TESTES NO CÓDIGO REFATORADO E SEGURO (Comprovação da Mitigação)
    # =========================================================================

    def test_sec_login_legitimo_funciona(self):
        """Na versão segura, usuário legítimo continua autenticando normalmente."""
        resultado = login_seguro(self.db_sec, "aluno_dio", "dio2026")
        self.assertTrue(resultado, "Login legítimo falhou no código seguro.")

    def test_sec_login_invalido_rejeitado(self):
        """Senha incorreta deve ser recusada."""
        resultado = login_seguro(self.db_sec, "aluno_dio", "senha_errada")
        self.assertFalse(resultado, "Senha incorreta foi aceita indevidamente.")

    def test_sec_bloqueio_efetivo_tautologia(self):
        """
        MITIGAÇÃO COMPROVADA:
        Na versão segura, o payload "' OR '1'='1" DEVE ser rejeitado (retornar False).
        """
        resultado = login_seguro(self.db_sec, self.payload_tautologia, "senha_falsa")
        self.assertFalse(resultado, "FALHA: O payload de injeção conseguiu burlar o código seguro!")

    def test_sec_bloqueio_efetivo_bypass_admin(self):
        """Na versão segura, o payload "admin' --" DEVE ser rejeitado."""
        resultado = login_seguro(self.db_sec, self.payload_comentario, "senha_falsa")
        self.assertFalse(resultado, "FALHA: O payload de comentário conseguiu logar como admin!")

    def test_sec_bloqueio_efetivo_union(self):
        """Na versão segura, injeção de UNION SELECT DEVE ser rejeitada."""
        resultado = login_seguro(self.db_sec, self.payload_union, "senha_falsa")
        self.assertFalse(resultado, "FALHA: O payload UNION foi executado!")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" INICIANDO EXECUÇÃO DA SUITE DE TESTES AUTOMATIZADOS DE APPSEC (DIO) ")
    print("=" * 70 + "\n")
    unittest.main(verbosity=2)
