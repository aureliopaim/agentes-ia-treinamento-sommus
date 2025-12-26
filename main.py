from agents import Agent, Runner, GuardrailFunctionOutput, RunHooks, function_tool
from dotenv import load_dotenv
import logging
import mysql.connector
import os

load_dotenv()


logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)
logging.getLogger("httpx").setLevel(logging.WARNING)


#-------- Tools --------#

@function_tool
def consultar_catagoria() -> list[str]:
    """Consulta o banco MySQL e retorna as categorias"""
    
    conn = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port=int(os.getenv("PORT")),
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            descricao
        FROM solicitacao_categoria
        ORDER BY solicitacao_categoria_id
        """
    )
    categorias = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return categorias


#-------- Hooks --------#

class TerminalHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        logging.info(f"[Agente] {agent.name}")

    async def on_handoff(self, context, from_agent, to_agent):
        logging.info(f"[Handoff] {from_agent.name} -> {to_agent.name}")

    async def on_agent_end(self, context, agent, output):
        logging.info(f"[Agente] {agent.name} finalizou")


#-------- Agentes --------#

def escritor_instructions(context, agent):
    return (
        "Você é o agente especializado em redação técnica. "
        "Sua tarefa é redigir respostas técnicas detalhadas para solicitações de clientes, "
        "baseando-se nas descrições fornecidas pelo AgenteTriagem. "
    )


agente_escritor = Agent(
    name="AgenteEscritor",
    instructions=escritor_instructions,
    model="gpt-4.1-mini",
    handoff_description="Agente escritor de solicitação",
)


def classificador_instructions(context, agent):
    return (
        "Você é o agente especializado em classificação de solicitações. "
        "Use a tool `consultar_catagoria` para obter as categorias disponíveis. "
        "Depois, classifique a solicitação em 1 das categorias retornadas e explique o motivo. "
        "Deve obrigatoriamente usar as categorias retornadas pela tool. "
        "Formatar em Markdown."
    )

agente_classificador = Agent(
    name="AgenteClassificador",
    instructions=classificador_instructions,
    model="gpt-4.1-mini",
    tools=[consultar_catagoria],
    handoff_description="Agente classificador de solicitação",
)


def triagem_instructions(context, agent):
    return (
        "Você é a Sofia, uma assistente de IA. "
        "Sua tarefa é receber solicitações de clientes e encaminhá-las para o agente mais adequado: "
        "Analise cuidadosamente cada solicitação e decida qual agente é o mais apropriado para lidar com ela. "
        "Se a solicitação envolver redação técnica detalhada, transfira para o `AgenteEscritor`. "
        "Se a solicitação envolver classificação, transfira para o `AgenteClassificador`."
        "Se a solicitação pedir para consultar uma solicitação por número, transfira para o `AgenteConsultaSolicitacao`. "
    )        

agente_triagem = Agent(
    name="AgenteTriagem",
    instructions=triagem_instructions,
    model="gpt-4.1-nano",
    handoffs=[agente_escritor, agente_classificador],
)

print("Por favor, insira a solicitação do cliente:")
user_input = input()

result = Runner.run_sync(
    agente_triagem, 
    user_input, 
    hooks=TerminalHooks()
)

print(result.final_output)

