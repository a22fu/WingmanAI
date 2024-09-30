TABLE_DETAILS = {
    "customers": "Customers purchase products from employees",
    "employees": "Employees sell products to customers",
    "orders": "Events of customers purchasing from employees",
    "products": "Products are supplied by vendors. Products belong to subcategories",
    "vendors": "Vendors supply products",
    "vendorproduct": "Use this table exclusively when joining with the 'vendors' table. Avoid using it in any other scenarios.",
    "productcategories": "Product categories are made up of multiple product subcategories",
    "productsubcategories": "Each product belongs to a product subcategory",
}

SQL_TEMPLATE_STR = """
Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist.
Qualify column names with the table name when needed.

If a column name contains a space, always wrap the column name in double quotes.

You are required to use the following format, each taking one line:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use tables listed below.
{schema}

Do not under any circumstance use SELECT * in your query.

Here are some useful examples:
{few_shot_examples}

Question: {query_str}\nSQLQuery: """

RESPONSE_TEMPLATE_STR = """If the <SQL Response> below contains data, then given an input question, synthesize a response from the query results.
    If the <SQL Response> is empty, then you should not synthesize a response and instead respond that no data was found for the quesiton..\n

    \nQuery: {query_str}\nSQL: {sql_query}\n<SQL Response>: {context_str}\n</SQL Response>\n

    Do not make any mention of queries or databases in your response, instead you can say 'according to the latest information' .\n\n
    Please make sure to mention any additional details from the context supporting your response.
    If the final answer contains <dollar_sign>$</dollar_sign>, ADD '\' ahead of each <dollar_sign>$</dollar_sign>.

    Response: """

FILTER_INPUT_TEMPLATE_STR = """You are a model in charge of categorizing inputs for a Valorant llm team building app. 
You are a model to determine which of 4 categories an input falls into. For context, the existing team is [dummy test team, ignore for now],
there is a change that it is empty.
1. Create a team prompt: Where the user asks to create a team given a set of criteria
Examples:
2. Edit an existing team prompt: Where the user asks to edit, add, remove or alter an existing team.
Examples:
3. General Valorant news/stats question: Where the user asks for general valorant news questions or statistics question.
Examples:
4. Other: Every other input that cannot be ascribed to one of the prior inputs.
Your output should only be the corresponding number from 1-4 for which you can best describe the input and nothing else.
"""

CREATE_TEAM_TEMPLATE_STR = """The following region values apply:
- "amer": The Americas, any mention of America, NA (North America), or SA (South America)
- "emea": Europe, Middle East, and Africa
- "cn": China
- "ap": Asia-Pacific region, including Oceania (excluding China)

League values are shown below:
- "gc": Game Changers League (for underrepresented groups)
- "international": International League (tier 1 teams, pro players, VCT international)
- "challengers": Tier 2 teams and below

A player object follows the template: 
{"player": "elfie", "org": "MKS", 
"agents": ["reyna", "raze", "omen"], 
"rounds_played": 310.0, "rating": 1.27, 
"average_combat_score": 260.7, 
"kill_deaths": 1.21, 
"kill_assists_survived_traded": 78.0, 
"average_damage_per_round": 169.8, 
"kills_per_round": 0.9, 
"assists_per_round": 0.31, 
"first_kills_per_round": 0.13, 
"first_deaths_per_round": 0.12, 
"headshot_percentage": 26.0, 
"clutch_success_percentage": 23.0, 
"region": "ap", "league": "gc", 
"zscore": 13.748756060196289},
where zscore is a general "goodness" measure for how well the player performs overall

When asking for aggressive playstyle, look for high first_kills_per_round, average_damage_per_round and kills_per_round
When asking for defensive playstyles, look for low first_deaths_per_round, high assists_per_round

Given a request to create a Valorant team:

You are a valorant team creator help bot that creates a Valorant team based on user input, using the genetic_alg_tool, which expects 2 strings, filter_string and constraint_string,  and returns a valorant team based on user input recommendations and constraints. Before you use the tool, 
you first must create the two strings. Each string contains the code for a function respectively:

1. filter_dataset(data): which takes an array of players and returns a filtered dataset. The use of this function should be to remove
players that we know can't go into our requested team. Only filter out options if it applies to every player on the team. If asking for good players in general, without mention of a specific stat, you can filter if they are below average zscore (0.46).
2. satisfies_constraints(team): which takes an array of five player objects and returns if the team satisfies the constraints mentioned in the request.

You must create the two strings and then use the tool to generate the team with the two strings as inputs for the tool
The output should a string of only the return of the genetic_alg_tool and nothing else.

Examples:
create a valorant team with only gamechangers players and 3 from china with tenZ on the team. There has to be an omen player and the one of the chinese players must be the star player
Example for the two strings:
["def filter_dataset(data):
    for x in data:
        if x["league"] == "gc":
            filtered_data.append(x)
    return filtered_data"
,"def satisfies_constraints(team):
    gc_count = sum(1 for player in team if player["league"] == "gc")
    cn_count = sum(1 for player in team if player["region"] == "cn")
    tenZ_count = sum(1 for player in team if player["player"] == "tenZ")

    
    # Check Best player is chinese
    star_player = max(team, key=lambda x: x["zscore"])
    if star_player["region"] != "cn":
        return False
    
    all_agents = []

    for player in team:
        all_agents.extend(player['agents'])
    if "omen" not in all_agents:
        return False
    return (
        cn_count >= 3 and 
        gc_count >= 5 and
        tenZ_count >= 1
    )"]

The average value for each stat is {'rounds_played': 380, 'rating': 1, 'average_combat_score': 200, 'kill_deaths': 1, 'kill_assists_survived_traded': 70, 'average_damage_per_round': 131, 'kills_per_round': 0.7, 'assists_per_round': 0.29, 'first_kills_per_round': 0.1, 'first_deaths_per_round': 0.1, 'headshot_percentage': 27, 'clutch_success_percentage': 14, 'zscore': 0.46}
Which can be used to filter based on above/below average stats or constraints based on above average stats

Try your best to create functions that correctly satisfies all constraints and filters, using any means.

Your output should on tool use should not contain any other output other than the two function strings"""
