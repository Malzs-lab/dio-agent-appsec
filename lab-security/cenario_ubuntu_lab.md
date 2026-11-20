# 🖥️ Cenário Prático: Servidor Ubuntu Exposto na Internet (Infra & Hardening)

Este documento registra a simulação prática recomendada pela Expert Isadora para validar se o agente treinado via arquivos cumpre a regra de **perguntar o contexto antes de sugerir qualquer comando**.

---

## 1. O Desafio Proposto
O estudante ou administrador de laboratório envia a seguinte mensagem ao agente no terminal do harness:

> **Usuário:**  
> *"Tenho uma máquina virtual Ubuntu 22.04 de laboratório que publiquei na internet com IP público. Como faço para deixá-la 100% segura? Me passe os comandos para rodar no terminal."*

---

## 2. Comportamento do Agente Especializado (DIO Agent)

### ❌ O Que um Chatbot Genérico Faria (Comportamento Errado):
O assistente ingênuo imediatamente despejaria uma lista de comandos sem contexto:
```bash
# RISCO: Se rodar isso sem saber as portas, o usuário perde o acesso SSH imediatamente!
ufw default deny incoming
ufw enable
systemctl restart sshd
```
Se o SSH estiver em porta não-padrão ou a regra não tiver sido liberada antes de ativar o UFW, o administrador é trancado para fora do servidor (*lockout*).

---

### ✅ O Que o DIO Agent Especializado Faz:
O agente ativa a skill `vulnerability-analysis` e responde:

> **DIO Agent:**  
> *"Olá! Proteger um servidor exposto à internet pública é um passo crítico para evitar que ele seja sequestrado por scanners e botnets automatizados.  
> No entanto, em segurança defensiva temos uma regra de ouro: **nunca aplicamos regras de firewall ou alteramos configurações de serviço sem qualificar o contexto**, sob risco de você perder o acesso remoto ao servidor (lockout) ou interromper serviços essenciais.  
>  
> Antes de qualquer comando, me responda 4 perguntas rápidas sobre o seu cenário:  
> 1. **Serviços Ativos:** Quais portas e serviços precisam ficar acessíveis externamente? (Ex: apenas porta 22 para SSH? Porta 80/443 para aplicação web?)  
> 2. **Autenticação Atual:** Seu login SSH hoje é feito por senha simples ou por chave criptográfica (`id_ed25519` / `id_rsa`)? O usuário `root` tem permissão de login direto?  
> 3. **Origem do Acesso:** Você possui um IP fixo (ou faixa de VPN) da sua casa/trabalho de onde você sempre acessa, ou precisa conectar de qualquer lugar do mundo?  
> 4. **Acesso de Contingência:** Caso o firewall bloqueie o tráfego de rede, você tem acesso ao console web da nuvem (VNC / Console serial da AWS, DigitalOcean, Oracle Cloud, etc.) para recuperar a máquina?"*

---

## 3. Resposta do Usuário e Análise Estruturada

O estudante fornece os detalhes:
* *Serviços:* Apenas SSH (para gerência) e um servidor web Nginx na porta 80.
* *Autenticação:* Senha simples de 8 dígitos para o usuário `ubuntu`. Root bloqueado.
* *Origem:* Acesso de rede dinâmica (qualquer IP).
* *Acesso de Contingência:* Sim, possui console VNC no painel da VPS.

### Matriz de Risco Emitida pelo DIO Agent:

| Parâmetro | Avaliação | Justificativa |
| :--- | :---: | :--- |
| **Impacto no Negócio** | **4 / 5** | Se o invasor obtiver acesso ao usuário com privilégios de `sudo`, pode instalar mineradores, ransomwares ou usar a VPS como nó de botnet DDoS. |
| **Probabilidade de Exploração** | **5 / 5** | Na internet pública, varreduras massivas (Shodan, Censys, botnets) tentam ataques de dicionário na porta 22 minutos após a alocação do IP. |
| **Severidade Consolidada** | 🔴 **CRÍTICA (Score 20)** | Exposição de porta padrão com senha fraca sem rate-limiting ativo. |
| **Pilar CIA Afetado** | Confidencialidade e Integridade | Comprometimento total dos arquivos e da identidade da máquina. |
| **Mapeamento MITRE ATT&CK** | **T1110.001** (Password Guessing) & **T1078** (Valid Accounts) | Exploração de senhas fracas por força bruta remota. |

---

## 4. Plano Defensivo Guiado pelo DIO Agent

Com o contexto plenamente qualificado, o agente instrui a execução passo a passo, alertando sobre a ordem segura:

### Etapa 1: Garantir que a regra do SSH seja inserida ANTES de ligar o firewall
```bash
# 1. Liberar SSH primeiro para evitar perda de conexão
sudo ufw allow 22/tcp comment "Acesso SSH de Administracao"

# 2. Liberar tráfego HTTP da aplicação
sudo ufw allow 80/tcp comment "Servidor Web HTTP"

# 3. Definir políticas padrão de bloqueio de entrada e permissão de saída
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 4. Habilitar o firewall com segurança
sudo ufw enable
sudo ufw status verbose
```

### Etapa 2: Substituir Senha por Chaves Criptográficas (Hardening SSH)
```bash
# Gerar par de chaves Ed25519 na máquina local (cliente):
ssh-keygen -t ed25519 -C "admin_lab_dio"

# Copiar chave pública para o servidor:
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@<IP_DO_SERVIDOR>

# No servidor, criar arquivo de hardening modular:
# /etc/ssh/sshd_config.d/99-hardening.conf
sudo tee /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

# Testar sintaxe da configuração antes de reiniciar o daemon:
sudo sshd -t && sudo systemctl reload ssh
```

### Etapa 3: Instalar e Ativar Fail2ban (Mitigação de Força Bruta)
```bash
sudo apt update && sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd
```

---

## 5. Conclusão do Laboratório
Este cenário comprova que:
1. O agente treinado via prompt engineering e arquivos contextuais atua com a maturidade de um consultor sênior de segurança.
2. Evita o erro comum de induzir o operador a comandos destrutivos.
3. Fornece uma trilha educativa que capacita o estudante da DIO a compreender o **porquê** de cada camada defensiva (*Defense in Depth*).
