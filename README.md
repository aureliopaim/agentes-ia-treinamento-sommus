# Agente IA

Este projeto é um **exemplo didático desenvolvido para treinamento** sobre construção de agentes de Inteligência Artificial utilizando o **OpenAI Agents SDK**.

O objetivo é demonstrar, de forma prática, conceitos como:
- Criação de agentes especializados
- Uso de tools para integração com sistemas externos
- Handoff entre agentes
- Guardrails de segurança e relevância
- Observabilidade do fluxo de execução

O projeto não tem foco em produção, mas sim em aprendizado e experimentação.

## Requisitos

- Python 3+

## Configuracao

1) Crie e ative o ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate
```

2) Instale as dependencias
```bash
pip install -r requirements.txt
```

3) Configure a chave da API
Crie um arquivo `.env` com:
```
OPENAI_API_KEY=SEU_TOKEN
```

## Executar

```bash
python main.py
```

## Referencias

- OpenAI Agents SDK (Python): https://github.com/openai/openai-agents-python
