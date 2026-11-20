---
name: security-test-guide
description: Guia o desenvolvimento de testes unitários e de integração focados em segurança defensiva, suites de regressão contra injeções e automação de linters SAST no fluxo de desenvolvimento (DevSecOps).
---

# 🧪 Roteiro Operacional: Testes de Segurança & Validação Automatizada (DevSecOps)

Quando o estudante ou desenvolvedor precisar comprovar que uma correção de segurança é eficaz e não reintroduzirá brechas em commits futuros, utilize este roteiro.

---

## 1. Princípios de Testes de Segurança de Aplicações
* **Testes Positivos vs. Testes Negativos:**
  - Teste positivo valida se credenciais corretas autenticam normalmente.
  - Teste negativo (foco de segurança) injeta intencionalmente payloads maliciosos (`' OR '1'='1`, `'; DROP TABLE...`, caracteres de escape) e certifica que o sistema recusa a autenticação e preserva a integridade do banco.
* **Isolamento de Estado:** Testes devem rodar em bancos efêmeros (`:memory:` no SQLite ou instâncias isoladas de teste), garantindo reprodutibilidade sem sujar dados reais.

---

## 2. Estrutura Padrão de uma Suite de Teste de Injeção SQL
Ao orientar o usuário a criar scripts de validação (ex: `test_sql_injection.py`):
1. **Configuração da Base:** Criar esquema de tabela e popular um usuário legítimo com hash seguro.
2. **Caso 1: Autenticação Válida:** Confirmar que credencial legítima retorna `True`.
3. **Caso 2: Autenticação Inválida Comum:** Confirmar que senha errada retorna `False`.
4. **Caso 3: Payload de Bypass Clássico (`' OR '1'='1`):** Deve retornar `False` na versão segura.
5. **Caso 4: Payload com Comentário de Fim de Linha (`admin' --`):** Deve retornar `False`.
6. **Caso 5: Injeção de Caracteres Especiais (`"`, `\`, `;`, `null` byte):** Deve ser tratada sem lançar erro de sintaxe SQL não tratado (Erro 500).

---

## 3. Automação SAST no Ciclo DevSecOps (Shift-Left)
Oriente a configuração de ferramentas estáticas:
* **Bandit (Python):**
  - Instalação: `pip install bandit`
  - Varredura recursiva de severidade alta: `bandit -r . -ll -ii`
* **Pip-Audit (Checagem de Dependências Vulneráveis):**
  - Instalação: `pip install pip-audit`
  - Auditoria de pacotes: `pip-audit`
