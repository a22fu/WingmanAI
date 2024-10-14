CATEGORIZE_TEMPLATE_STR = """
Categorize the above input into one of 4 categories:
1. A request to create a Valorant professional team, potentially given some parameters and requests
2. A request to edit, change or improve in some way a given Valorant professional team, including add X player, take out a smokes, make the team more aggressive
3. A general question related to Valorant esports or stats.
4. An unrelated input that doesn't fit any category
Your output must only contain the number of the category that you think best fits the input and nothing else.
"""

CREATE_TEAM_TEMPLATE_STR = """
Try to make the best team possible prioritizing:
1. Firstly, high ratings above 1.2 in tournaments
2. Secondly, high placements with teams in tournaments
3. Third, Having at least one of each agent role on the team, (duelist, controller, sentinel, initiator, flex(someone shown to play multiple roles)). 

you MUST return five unique players, make do if you can't find optimal choices

A team should should try to include as many of the following roles as possible and it should be considered a weakness if there isn't one
    "smokes": ["omen", "brimstone", "viper", "astra", "harbor", "clove"],
    "entry": ["reyna", "phoenix", "yoru", "iso"],
    "intel_gatherer": ["sova", "fade", "cypher","gekko","skye"],
    "lurker": ["cypher", "omen", "chamber", "yoru", "viper", "killjoy"],
    "flank_watch": ["killjoy", "cypher", "chamber","vyse"],
    "flash_initiator": ["skye", "kayo", "breach", "phoenix","reyna","gekko"],
    "movement_duelist": ["reyna", "raze", "neon", "jett", "yoru"]
    "controller": ["astra", "brimstone", "harbor", "omen", "viper", "clove"],
    "sentinel": ["chamber", "cypher", "killjoy", "sage", "vyse"],
    "duelist": ["jett", "neon", "phoenix", "raze", "reyna", "yoru", "iso"],
    "initiator": ["breach", "fade", "gekko", "kayo", "skye", "sova"]

Include a detailed explanation of each choice you made, and strengths and weaknesses of the team
do not under any circumstances mention search results or sources in the output
do not under any circumstances mention specific rating numbers or first contact per round, only say how well they are performing or their offensive vs defensive roles on the team.
"""

PARSE_CREATE_TEAM_TEMPLATE_STR = """
You will receive an output from a Valorant team creator bot that creates a team composition. Your task is to parse the output and organize the information into distinct tags for further use in a program.

If the output is for creating or editing a team composition, it will include a list of players, strengths, weaknesses, and possibly new players if the team is being edited. Separate the output into the following categories:

[players]: This should include the final team of five players.
[strengths]: A list or description of the team’s strengths.
[weaknesses]: A list or description of the team’s weaknesses.
[original_output]: The original output string from the Valorant team creator bot.

Make sure that each section is wrapped in distinct exit tags and that only relevant sections are included. For example:

[players]
Player1, Player2, Player3, Player4, Player5
[/players]

[strengths]
Strong agent synergy, High fragging power
[/strengths]

[weaknesses]
Lack of experience on certain maps
[/weaknesses]

[original_output]
<Original bot output here>
[/original_output]

If any sections (such as weaknesses) are not relevant, you can omit those sections. The input is as follows: \n
"""

EDIT_TEAM_TEMPLATE_STR = """
Try to make the best team possible prioritizing, while editing the original team.
Consider:
1. Firstly, high ratings above 1.2 in tournaments
2. Secondly, high placements with teams in tournaments
3. Third, Having at least one of each agent role on the team, (duelist, controller, sentinel, initiator, flex(someone shown to play multiple roles)). 

you MUST return five unique players, make do if you can't find optimal choices

A team should should try to include as many of the following roles as possible and it should be considered a weakness if there isn't one
    "smokes": ["omen", "brimstone", "viper", "astra", "harbor", "clove"],
    "entry": ["reyna", "phoenix", "yoru", "iso"],
    "intel_gatherer": ["sova", "fade", "cypher","gekko","skye"],
    "lurker": ["cypher", "omen", "chamber", "yoru", "viper", "killjoy"],
    "flank_watch": ["killjoy", "cypher", "chamber","vyse"],
    "flash_initiator": ["skye", "kayo", "breach", "phoenix","reyna","gekko"],
    "movement_duelist": ["reyna", "raze", "neon", "jett", "yoru"]
    "controller": ["astra", "brimstone", "harbor", "omen", "viper", "clove"],
    "sentinel": ["chamber", "cypher", "killjoy", "sage", "vyse"],
    "duelist": ["jett", "neon", "phoenix", "raze", "reyna", "yoru", "iso"],
    "initiator": ["breach", "fade", "gekko", "kayo", "skye", "sova"]

Include a detailed explanation of each choice you made, and improvements on the old team and potential weaknesses compared to the old team.
do not under any circumstances mention search results or sources in the output
do not under any circumstances mention specific rating numbers or first contact per round, only say how well they are performing or their offensive vs defensive roles on the team.
"""

PARSE_EDIT_TEAM_TEMPLATE_STR = """"
You will receive an output from a Valorant team editor bot that creates a team composition. Your task is to parse the output and organize the information into distinct tags for further use in a program.

If the output is for creating or editing a team composition, it will include a list of players, strengths, weaknesses, and possibly new players if the team is being edited. Separate the output into the following categories:

[players]: This should include the new team of five players, reflecting any edits if new players were added or swapped
[strengths]: A list or description of the team’s improvements.
[weaknesses]: A list or description of the team’s weaknesses compared to the old team.
[original_output]: The original output string from the Valorant team editor bot.

Make sure that each section is wrapped in distinct exit tags and that only relevant sections are included. For example:

[players]
Player1, Player2, Player3, Player4, Player5
[/players]

[strengths]
Strong agent synergy, High fragging power
[/strengths]

[weaknesses]
Lack of experience on certain maps
[/weaknesses]

[original_output]
<Original bot output here>
[/original_output]

If any sections (such as weaknesses) are not relevant, you can omit those sections. The input is as follows: \n
"""