---
name: consultar-cep
description: Consulta informações de endereços brasileiros a partir de um CEP usando a API ViaCEP. Use esta skill quando o usuário solicitar buscar dados de endereço, validar CEPs ou obter informações de localização.
---

# Consultar CEP

## Visão Geral

Esta skill permite consultar a API **ViaCEP** para obter informações completas de endereços brasileiros a partir de um CEP válido. Retorna dados como logradouro, bairro, cidade, UF, código IBGE e DDD.

## Quando Usar

Utilize esta skill quando:
- O usuário solicitar consulta de um CEP específico (ex: "consulte o CEP 01001-000")
- For necessário validar se um CEP existe e está ativo
- O usuário precisar de informações de endereço para preenchimento de formulários
- Houver necessidade de obter cidade/UF a partir de um CEP
- O usuário perguntar sobre localização baseada em CEP

## Formato do CEP

O CEP brasileiro possui 8 dígitos, podendo ser formatado com hífen (XXXXX-XXX) ou sem formatação (XXXXXXXX).

**Exemplos válidos:**
- `01001-000`
- `01001000`
- `20040-020`
- `80010-030`

## Fluxo de Consulta

### 1. Validação do CEP

Antes de consultar a API, valide o formato do CEP:

```typescript
function validarCEP(cep: string): string | null {
  // Remove caracteres não numéricos
  const cepLimpo = cep.replace(/\D/g, '');
  
  // Verifica se tem 8 dígitos
  if (cepLimpo.length !== 8) {
    return null;
  }
  
  return cepLimpo;
}
```

### 2. Consulta à API ViaCEP

Faça uma requisição GET para a API:

```
GET https://viacep.com.br/ws/{CEP}/json/
```

**Exemplo de requisição:**
```bash
curl https://viacep.com.br/ws/01001000/json/
```

### 3. Resposta da API

**Sucesso (CEP encontrado):**
```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "complemento": "lado ímpar",
  "unidade": "",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP",
  "estado": "São Paulo",
  "regiao": {
    "id": "2",
    "sigla": "SE",
    "nome": "Sudeste"
  },
  "ibge": "3550308",
  "gia": "1004",
  "ddd": "11",
  "siafi": "7107"
}
```

**Erro (CEP não encontrado):**
```json
{
  "erro": true
}
```

## Tratamento de Erros

| Situação | Ação |
|----------|------|
| CEP com formato inválido | Informar ao usuário que o CEP deve ter 8 dígitos |
| CEP não encontrado | Informar que o CEP não foi encontrado na base dos Correios |
| Timeout da API | Informar indisponibilidade temporária do serviço |
| Erro de conexão | Solicitar ao usuário para tentar novamente |

## Exemplos de Uso

### Exemplo 1: Consulta Simples

**Usuário:** "Consulte o CEP 01001-000"

**Resposta esperada:**
```
📬 CEP: 01001-000
📍 Endereço: Praça da Sé, Sé
🏙️ Cidade: São Paulo - SP
📞 DDD: 11
🔢 IBGE: 3550308
```

### Exemplo 2: Validação de Endereço

**Usuário:** "Esse CEP 20040-020 existe?"

**Resposta esperada:**
```
Sim, o CEP 20040-020 é válido e corresponde a:
- Logradouro: Rua do Carmo
- Bairro: Centro
- Cidade: Rio de Janeiro - RJ
```

### Exemplo 3: Múltiplos CEPs

**Usuário:** "Consulte os CEPs 01001-000 e 20040-020"

**Resposta esperada:**
Consultar cada CEP sequencialmente e apresentar resultados em formato de lista.

## Recursos

Esta skill inclui diretórios de exemplo que demonstram como organizar diferentes tipos de recursos:

### scripts/
Scripts executáveis para operações específicas relacionadas à consulta de CEP.

**Exemplos apropriados:**
- Scripts de validação de CEP em lote
- Scripts de exportação de resultados para CSV/JSON
- Scripts de integração com outras APIs

### references/
Documentação e material de referência para informar o processo do Gemini CLI.

**Exemplos apropriados:**
- Documentação da API ViaCEP
- Lista de CEPs por região/estado
- Guias de formatação de endereços

### assets/
Arquivos destinados ao uso na saída produzida pelo Gemini CLI.

**Exemplos apropriados:**
- Templates de relatórios de endereço
- Modelos de etiquetas de correspondência
- Arquivos de configuração para integração

---

## API Reference

**Endpoint:** `https://viacep.com.br/ws/{CEP}/json/`

**Método:** GET

**Headers:**
```
Accept: application/json
```

**Parâmetros:**
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| CEP | string | Sim | CEP com 8 dígitos (com ou sem hífen) |

**Códigos de Resposta:**
| Código | Significado |
|--------|-------------|
| 200 | Sucesso (pode conter erro: true se CEP não existir) |
| 400 | Requisição inválida |
| 429 | Rate limit excedido |
| 500 | Erro no servidor da API |
