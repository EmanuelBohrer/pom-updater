# Atualizador de Dependências do Maven

Este script em Python lê um arquivo `pom.xml`, busca as versões mais recentes das dependências no **Maven Repository** e gera um novo `updated_pom.xml` com as versões atualizadas.

## 📌 Funcionalidades
✅ Carrega o `pom.xml`
✅ Extrai as dependências e suas versões
✅ Busca as versões mais recentes no **Maven Repository**
✅ Gera um `updated_pom.xml` atualizado

## 🚀 Como Usar

### 🔹 Pré-requisitos
- **Python 3+** instalado
- Biblioteca `requests` instalada:
  ```bash
  pip install requests
  ```

### 🔹 Executando o Script
1. Coloque o arquivo `pom.xml` na mesma pasta do script.
2. Execute o script com o comando:
   ```bash
   python main.py
   ```
3. O script criará um novo arquivo `updated_pom.xml` com as versões mais recentes das dependências.

## ⚙️ Funcionamento Interno
1. **Lê o `pom.xml`** e extrai as dependências (groupId, artifactId e version).
2. **Acessa o Maven Repository** para buscar as versões mais recentes.
3. **Atualiza o XML** com as novas versões e salva um novo `updated_pom.xml`.
