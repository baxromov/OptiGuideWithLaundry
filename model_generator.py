def generate_source_code(wash_type_data):

    print("wash_type_data:", wash_type_data)
    wash_type_names = [wash_type_data[wt]["wash_type_name"] for wt in wash_type_data]
    revenues = [wash_type_data[wt]["total_revenue"] for wt in wash_type_data]

    # Build revenues dict string for code
    revenues_dict_str = "{" + ", ".join(f"'{wt}': {rev}" for wt, rev in zip(wash_type_names, revenues)) + "}"

    constraint_lines = ""
    for wt_name in wash_type_names:
        safe_name = wt_name.replace(" ", "_").lower()
        cap = wash_type_data[next(k for k in wash_type_data if wash_type_data[k]["wash_type_name"] == wt_name)][
            "capacity"]
        constraint_lines += f"m.addConstr(x['{wt_name}'] <= {cap}, 'capacity_{safe_name}')\n"

    source_code = f'''
from gurobipy import Model, GRB, quicksum

m = Model("laundry_schedule_optimization")

revenues = {revenues_dict_str}

x = m.addVars(list(revenues.keys()), vtype=GRB.INTEGER, name="x")

obj = quicksum(revenues[wt] * x[wt] for wt in revenues)
m.setObjective(obj, GRB.MAXIMIZE)

{constraint_lines}

# OPTIGUIDE DATA CODE GOES HERE

# OPTIGUIDE CONSTRAINT CODE GOES HERE

m.optimize()
'''
    return source_code
