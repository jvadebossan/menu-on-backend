# Menu-On Backend

O backend do **Menu-On** é construído utilizando **Python**, **FastAPI**, e **MongoDB**. A aplicação fornece um serviço de **cardápio digital** com a opção de realizar pedidos online, facilitando a gestão dos pedidos e da interação entre os clientes e o estabelecimento.

## Tecnologias Utilizadas

- **Python** 3.9+
- **FastAPI**: Framework moderno e rápido para construção de APIs.
- **MongoDB**: Banco de dados NoSQL para armazenar dados de pedidos, usuários e cardápios.
- **Swagger UI**: Para documentação interativa da API.
- **JWT (JSON Web Tokens)**: Para autenticação de usuários.

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/menu-on-backend.git
cd menu-on-backend
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts ctivate     # Para Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Defina as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com a seguinte variável:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
MONGODB_DB_NAME="<dbname>"
SECRET_KEY="SECRET HERE"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
ENVIRONMENT="development"
VERSION="1.0.0"
```

Substitua os valores de `<username>`, `<password>`, `<cluster-url>`, e `<dbname>` pela sua string de conexão do MongoDB Atlas.

### 5. Execute a aplicação
```bash
uvicorn app.main:app --reload
```

Isso iniciará o servidor localmente em `http://127.0.0.1:8000`.

## Como Usar

### Documentação da API

A documentação da API pode ser acessada diretamente pelo Swagger UI:

```
http://127.0.0.1:8000/docs
```

Swagger fornecerá uma interface interativa para testar as rotas da API diretamente.

### Rotas Principais

#### **Autenticação**
- **POST /auth/register**: Registra um novo usuário.
- **POST /auth/login**: Faz o login e retorna um JWT de autenticação.

#### **Outras rotas em desenvolvimento**

### Exemplo de Uso (futuramente)

#### 1. Criar um Pedido
Envia uma requisição `POST` para `/orders/new-order` com o seguinte corpo JSON:
```json
{
  "establishment_id": "123",
  "table_number": 5,
  "customer_name": "João Silva",
  "customer_phone": "11999999999",
  "items": [
    {
      "name": "Hambúrguer",
      "quantity": 2,
      "price": 25.90
    },
    {
      "name": "Refrigerante",
      "quantity": 1,
      "price": 5.50
    }
  ],
  "total_price": 57.30
}
```

#### 2. Consultar o Status de um Pedido
Faça uma requisição `GET` para `/orders/status/{id}`.

#### 3. Atualizar o Status de um Pedido
Faça uma requisição `PUT` para `/orders/status/{id}` com o corpo:
```json
{
  "status": "delivered" // possíveis status: ["order_placed", "preparation", "finished", "delivered"]"
}
```

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autor

**Menu-On** - Desenvolvido por João Vitor de Aguiar Debossan.