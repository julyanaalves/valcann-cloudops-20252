# Desafio Técnico | Valcann - Programa de Estágio 2025.2 (CloudOps)

## 📄 Introdução

Este repositório contém a resolução completa do Desafio Técnico para o **Programa de Estágio 2025.2 na área de CloudOps da Valcann**. O projeto demonstra habilidades em automação com Python, diagnóstico de performance de sistemas e arquitetura de pipelines de CI/CD.

As respostas detalhadas, incluindo os diagramas de arquitetura, estão consolidadas no documento final da avaliação:
* **[VALCANN _ Programa de Estágio 2025.2 (CloudOps) _ Avaliação Técnica _ JULYANA DOS SANTOS ALVES.pdf](./VALCANN _ Programa de Estágio 2025.2 (CloudOps) _ Avaliação Técnica _ JULYANA DOS SANTOS ALVES.pdf)**

## 🎯 Desafios Resolvidos

O desafio foi dividido em três problemas práticos do dia a dia de um profissional de CloudOps:

* [Problema 1: Automação de Ambientes Operacionais](#problema-1-automação-de-ambientes-operacionais)
* [Problema 2: Monitoramento e Performance](#problema-2-monitoramento-e-performance)
* [Problema 3: Aplicações e Desenvolvimento de Software (CI/CD)](#problema-3-aplicações-e-desenvolvimento-de-software-cicd)

---

### Problema 1: Automação de Ambientes Operacionais

[cite_start]**Resumo do Desafio:** Criar um script para automatizar a rotina de gerenciamento de backups, incluindo listagem, limpeza de arquivos com mais de 3 dias e cópia de arquivos recentes, com a geração de logs. [cite: 46, 397]

[cite_start]**Solução Proposta:** Foi desenvolvido um script Python CLI (Command-Line Interface) robusto, modular e configurável. [cite: 45, 46, 396, 397] Ele não apenas cumpre os requisitos, mas também incorpora boas práticas de engenharia de software.

* [cite_start]**Tecnologias:** `Python` [cite: 45, 396][cite_start], `argparse` [cite: 48, 399][cite_start], `pathlib` [cite: 53, 404][cite_start], `shutil`[cite: 50, 401].
* **Funcionalidades:**
    * [cite_start]Interface de linha de comando para flexibilidade. [cite: 68, 69, 70, 415, 416]
    * [cite_start]Modo `--dry-run` para simulação segura das operações. [cite: 79, 422]
    * [cite_start]Configuração via variáveis de ambiente. [cite: 55, 57, 59, 62, 406, 407, 408, 409]
    * [cite_start]Código modular e com tipagem estática. [cite: 54, 405]

**Como Executar:**
(O código-fonte da solução está no arquivo `problem1.py`)
```bash
# Ver todas as opções de execução
python problem1.py --help

# Exemplo de execução em modo de simulação (não altera arquivos)
python problem1.py --source ./pasta_origem --dest ./pasta_destino --dry-run