# Desafio Técnico | Valcann - Programa de Estágio 2025.2 (CloudOps)

## 📄 Introdução

Este repositório contém a resolução completa do Desafio Técnico para o **Programa de Estágio 2025.2 na área de CloudOps da Valcann**. O projeto demonstra habilidades em automação com Python, diagnóstico de performance de sistemas e arquitetura de pipelines de CI/CD.

As respostas detalhadas, incluindo os diagramas, estão consolidadas no documento final da avaliação:

**[VALCANN - Programa de Estágio 2025.2 (CloudOps) - Avaliação Técnica - JULYANA DOS SANTOS ALVES.pdf] (./VALCANN - Programa de Estágio 2025.2 (CloudOps) - Avaliação Técnica - JULYANA DOS SANTOS ALVES.pdf)**

## 🎯 Desafios Resolvidos

O desafio foi dividido em três problemas práticos do dia a dia de um profissional de CloudOps:

* [Problema 1: Automação de Ambientes Operacionais](#problema-1-automação-de-ambientes-operacionais)
* [Problema 2: Monitoramento e Performance](#problema-2-monitoramento-e-performance)
* [Problema 3: Aplicações e Desenvolvimento de Software (CI/CD)](#problema-3-aplicações-e-desenvolvimento-de-software-cicd)

---

### Problema 1: Automação de Ambientes Operacionais

**Resumo do Desafio:** Criar um script para automatizar uma rotina de gerenciamento de backups, incluindo listagem, limpeza de arquivos com mais de 3 dias e cópia de arquivos recentes, com a geração de logs.

**Solução Proposta:** Foi desenvolvido um script Python CLI (Command-Line Interface) robusto, modular e configurável. Ele não apenas cumpre os requisitos, mas também incorpora boas práticas de engenharia de software.

**Tecnologias:** `Python`, `argparse`, `pathlib`, `shutil`.

**Funcionalidades:**
* Interface de linha de comando para flexibilidade.
* Modo `--dry-run` para simulação segura das operações.
* Configuração via variáveis de ambiente.
* Código modular e com tipagem estática.

**Como Executar:**
(O código-fonte da solução está no arquivo `problem1.py`)
```bash
# Ver todas as opções de execução
python problem1.py --help

# Ver todas as opções de execução
python problem1.py --help

# Exemplo de execução em modo de simulação (não altera arquivos)
python problem1.py --source ./pasta_origem --dest ./pasta_destino --dry-run
```


### Problema 2: Monitoramento e Performance

**Resumo do Desafio:** Diagnosticar a causa raiz da lentidão em uma aplicação web com 4 servidores de aplicação e 2 de banco de dados, onde as métricas básicas de infraestrutura (CPU/memória) não indicam sobrecarga.


**Solução Proposta:** Uma análise estruturada (Problema > Causa > Solução) com um plano de diagnóstico end-to-end, que investiga o sistema em quatro camadas críticas para identificar gargalos sutis. A solução inclui a instrumentação da aplicação para obter visibilidade completa, visualizada em um diagrama de arquitetura detalhado.

**Conceitos e Ferramentas:**

* Análise de **Core Web Vitals** e RUM (Real User Monitoring).
* **APM (Application Performance Monitoring)** com **Distributed Tracing** para identificar latência de cauda longa (p95/p99) e queries N+1.
* Análise de **Pool de Conexões**, **Locks** e planos de execução de queries no banco de dados.
* Monitoramento de **Dependências Externas**.
* Estratégias de mitigação como **Cache (Redis)** e o padrão **Circuit Breaker**.



### Problema 3: Aplicações e Desenvolvimento de Software (CI/CD)

**Resumo do Desafio:** Automatizar o processo de deploy de uma aplicação Node.js/React, que atualmente é totalmente manual, envolvendo empacotamento, deploy em homologação, uma semana de validação, e um novo deploy manual em produção.

**Solução Proposta:** O desenho de um ecossistema de CI/CD (Continuous Integration/Continuous Deployment) completo e moderno, que aborda a solução em cinco pilares fundamentais para garantir um ciclo de entrega ágil, seguro e confiável. A solução é acompanhada por um diagrama detalhado do fluxo do pipeline.

**Pilares da Solução:**
1. **Fundação:** Pipeline de CI/CD com Git, GitHub Actions e Docker.
2. **Qualidade Automatizada:** Integração de testes, linters e análise de segurança no pipeline.
3. **Consistência de Ambientes:** Uso de Infraestrutura como Código (IaC) com Terraform/Ansible.
4. **Deploys Seguros:** Implementação de aprovação manual para produção e estratégias como Blue-Green.
5. **Gerenciamento de Banco de Dados:** Automação das migrações de schema dentro do pipeline.

## 🛠️ Tecnologias e Conceitos Abordados
* **Linguagens:** Python
* **DevOps:** CI/CD, Docker, Infraestrutura como Código (IaC), Git
* **Ferramentas:** GitHub Actions, Nginx, Terraform/Ansible, Prometheus, Grafana, Jaeger
* **Conceitos de Arquitetura:** Monitoramento, Observabilidade, APM, RUM, Caching (Redis), Padrão Circuit Breaker, Estratégias de Deploy (Blue-Green/Canary)
* **Bancos de Dados:** Análise de Performance, Migrações de Schema

## 👩‍💻 Autora
**Julyana dos Santos Alves**
* **LinkedIn:** https://www.linkedin.com/in/julyana-s-alves 
* **GitHub:** https://github.com/julyanaalves