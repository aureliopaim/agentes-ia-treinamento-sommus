from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agente_sofia = Agent(
    name="Sofia",
    instructions="Você é a Sofia, uma assistente de IA especializada em informações sobre a empresa Sommus Sistemas.",
    model="gpt-4.1-nano",
)

result = Runner.run_sync(agente_sofia, "Quem é você?")
print(result.final_output)
