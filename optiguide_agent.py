import autogen
from autogen.agentchat import UserProxyAgent
from optiguide import OptiGuideAgent


def create_agent_and_user(source_code):
    config_list = autogen.config_list_from_json('OAI_CONFIG_LIST')

    example_qa = """
----------
Question: What if we increase the capacity of dry clean wash by 5?
Answer Code:
constr = m.getConstrByName("capacity_dry_clean")
current_rhs = constr.getAttr("RHS")
constr.setAttr("RHS", current_rhs + 5)
m.update()

text
----------
Question: How to reduce normal wash capacity to 8?
Answer Code:
constr = m.getConstrByName("capacity_normal")
constr.setAttr("RHS", 8)
m.update()

"""
    agent = OptiGuideAgent(
        name="LaundryOptimization",
        source_code=source_code,
        debug_times=1,
        example_qa=example_qa,
        llm_config={
            "seed": 42,
            "config_list": config_list,
        }
    )

    user = UserProxyAgent(
        "user",
        max_consecutive_auto_reply=0,
        human_input_mode="NEVER",
        code_execution_config=False
    )
    return agent, user
