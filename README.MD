# 🏥 TraceMed – Sistema de Rastreabilidade de Materiais Hospitalares

Sistema para controle de usuários, materiais e processos de esterilização, com rastreabilidade completa e geração de relatórios em PDF e XLSX.

---

## ⚙️ Requisitos

- **Python 3.11+**
- **Node.js 18+**
- **MySQL**
- **pip**
- **Yarn** ou **npm**

---

## 📁 Instalação do Backend

1. Clone o repositório:
```bash
git clone https://github.com/GabrielDomingoss/TraceMed.git
cd TraceMed/cme-back
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados MySQL e edite a string de conexão no arquivo `database.py`.

5. Popule o banco com dados de exemplo:
```bash
python seed.py
```

6. Inicie o servidor:
```bash
uvicorn main:app --reload
```

---

## 💡 Documentação Swagger

Acesse via navegador:

📄 [`http://localhost:8000/api/docs`](http://localhost:8000/api/docs)

---

## 💼 Coleção Postman

Importe no Postman para testar os endpoints:

📥 [traceMed.postman_collection.json](./traceMed.postman_collection.json)

---

## 💻 Instalação do Frontend

1. Vá para a pasta do frontend:
```bash
cd ../cme-front
```

2. Instale as dependências:
```bash
yarn install
# ou
npm install
```

3. Inicie o projeto:
```bash
yarn dev
# ou
npm run dev
# ou
npm start
```

---

## ✅ Funcionalidades

- ✅ Autenticação JWT
- ✅ Controle de usuários (admin, técnico, enfermeiro)
- ✅ Cadastro e listagem de materiais
- ✅ Registro de processos por etapas: recebimento, lavagem, esterilização e distribuição
- ✅ Registro de falhas (com criticidade)
- ✅ Relatórios PDF e XLSX
- ✅ Interface clean, responsiva e moderna com Material UI + Framer Motion

---

## 🚀 Acesso Rápido

- **Frontend**: [`http://localhost:5173`](http://localhost:5173)
- **Backend API**: [`http://localhost:8000`](http://localhost:8000)
- **Swagger**: [`http://localhost:8000/api/docs`](http://localhost:8000/api/docs)
---

## 👤 Desenvolvido por

Gabriel Domingos