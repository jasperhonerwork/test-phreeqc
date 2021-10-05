import sys
from file_management import Input_file
from queries_db import Db_connection, Queries

#Getting the Model Id
model_id = 1#int(sys.argv[1])

#creating input file
my_new_file = Input_file(model_id)
my_new_file.start_input_file()

#Creating connection with the database
my_connections = Db_connection()
connection = my_connections.connect()

#Rule 1
rule_name = "'Rule 1'"
query = f"select Id From [ZGM_TransactieData].[Phreeqc].[Rule] Where Name = {rule_name}"
q = Queries(connection, query)
rule_1_id = q.run_query()

#Get the positions
query = f"Select COUNT (Id) from Phreeqc.RulePosition where Ruleid = {rule_1_id}"
q = QueryDb(connection, query)
count_rul_pos = q.run_query()

#setting al the component in line for rule 1
rul_pos_counter = 1

#getting al the values for rule 1
rul_pos_counter = 1
my_new_file.db_data = "1\t"
my_new_file.writing_to_input_file()
while rul_pos_counter <= count_rul_pos:
    query = f"Select IsFixed From Phreeqc.[RulePosition] Where RuleId = {rule_1_id} and Position = {rul_pos_counter}"
    q = Queries(connection, query)
    fixed_bool = q.run_query()
    if fixed_bool == True:
        query = f"Select FixedValue From Phreeqc.[RulePosition] Where RuleId = {rule_1_id} and Position = {rul_pos_counter}"
        q = Queries(connection, query)
        value = q.run_query()
    else:
        query = f"Select Value From Phreeqc.InputValue Where RuleId = {rule_1_id} and RulePositionId = {rul_pos_counter}"
        q = Queries(connection, query)
        value = q.run_query()
    my_new_file.db_data = f"{value}\t"
    my_new_file.writing_to_input_file()
    rul_pos_counter += 1
my_new_file.db_data = '\nEND\n'
my_new_file.writing_to_input_file()

rule_counter = 2

#Get the positions
query = f"Select COUNT (Id) from [Phreeqc].[Rule] where ModelPhreeqcId = {model_id}"
q = Queries(connection, query)
amount_of_rules = q.run_query()
while rule_counter <= amount_of_rules:
    rul_pos_counter = 1

    #Which Rule
    query = f"Select COUNT (Id) from Phreeqc.RulePosition where Ruleid = {rule_counter}"
    q = Queries(connection, query)
    amount_of_positions = q.run_query()

    #TITLE
    query = f"Select Title From Phreeqc.ruleview2 Where RuleId = {rule_counter}"
    q = Queries(connection, query)
    title = q.run_query()
    my_new_file.db_data = f"TITLE\t{title}"
    my_new_file.writing_to_input_file()

    #SUB RULE
    query = f"Select SubRuleName From Phreeqc.ruleview2 Where RuleId = {rule_counter}"
    q = Queries(connection, query)
    sub_rule = q.run_query()
    if sub_rule is not None:
        my_new_file.db_data = f"\t\t{sub_rule}\n"
    else:
        my_new_file.db_data = '\n'
    my_new_file.writing_to_input_file()

    #USE SOLUTION
    query = f"Select UsedSolutionId From [Phreeqc].[Rule] Where Id = {rule_counter}"
    q = Queries(connection, query)
    use_solution = q.run_query()
    if use_solution is not None:
        my_new_file.db_data = f"\tUse solution\t{use_solution}\n"
    else:
        my_new_file.db_data = '\n'
    my_new_file.writing_to_input_file()

    #REACTION
    query = f"Select ReactionName From Phreeqc.ruleview2 Where RuleId = {rule_counter}"
    q = Queries(connection, query)
    reaction = q.run_query()
    my_new_file.db_data = f"\t{reaction}\n"
    my_new_file.writing_to_input_file()

    #Going through each position and fill the value and the components
    while rul_pos_counter <= amount_of_positions:
        query = f"Select Id from Phreeqc.RulePosition where RuleId = {rule_counter} and Position = {rul_pos_counter}"
        q = Queries(connection, query)
        pos_id = q.run_query()
        query = f"Select IsMmoles from Phreeqc.RulePosition where Ruleid = {rule_counter} and Position = {rul_pos_counter}"
        q = Queries(connection, query)
        bool_mmoles = q.run_query()
        query = f"Select IsFixed From Phreeqc.RulePosition where RuleId = {rule_counter} and Position = {rul_pos_counter}"
        q = Queries(connection, query)
        bool_fixed = q.run_query()

        #getting and writing mmoles values and component
        if bool_mmoles == True:
            query = f"SELECT rc.Name FROM Phreeqc.RuleComponent AS rc LEFT JOIN Phreeqc.RulePosition AS rp ON rp.ComponentId = rc.Id WHERE rp.RuleId = {rule_counter} and rp.Position = {rul_pos_counter}"
            q = Queries(connection, query)
            component = q.run_query()
            query = f"  SELECT State FROM Phreeqc.RuleComponent AS rc LEFT JOIN Phreeqc.RulePosition AS rp ON rp.ComponentId = rc.Id WHERE rp.RuleId = {rule_counter} and rp.Position = {rul_pos_counter}"
            q = Queries(connection, query)
            component_state = q.run_query()
            if component_state == 'gas':
                component = f"{component} (g)"
            if bool_fixed == True:
                query = f"Select FixedValue From Phreeqc.RulePosition where Id = {pos_id}"
                q = Queries(connection, query)
                value = q.run_query()
            else:
                query = f"Select Value From Phreeqc.InputValue where RulePositionId = {pos_id}"
                q = Queries(connection, query)
                value = q.run_query()
                if value == 0E-7:
                    value = 0.000
            my_new_file.db_data = f"\t{value} "
            my_new_file.writing_to_input_file()
            my_new_file.db_data = f"{component}\n"
            my_new_file.writing_to_input_file()

        # getting and writing non mmoles values and component
        else:
            query = f"SELECT rc.Name FROM Phreeqc.RuleComponent AS rc LEFT JOIN Phreeqc.RulePosition AS rp ON rp.ComponentId = rc.Id WHERE rp.RuleId = {rule_counter} and rp.Position = {rul_pos_counter}"
            q = Queries(connection, query)
            component = q.run_query()
            query = f"  SELECT State FROM Phreeqc.RuleComponent AS rc LEFT JOIN Phreeqc.RulePosition AS rp ON rp.ComponentId = rc.Id WHERE rp.RuleId = {rule_counter} and rp.Position = {rul_pos_counter}"
            q = Queries(connection, query)
            component_state = q.run_query()
            if component_state == 'Gas':
                component = f"{component}(g)"
            if bool_fixed == True:
                query = f"Select FixedValue From Phreeqc.RulePosition where Id = {pos_id}"
                q = Queries(connection, query)
                value = q.run_query()
            else:
                query = f"Select Value From Phreeqc.InputValue where RulePositionId = {pos_id}"
                q = Queries(connection, query)
                value = q.run_query()
                if value == 0E-7:
                    value = 0.000
            my_new_file.db_data = f"\t{component}"
            my_new_file.writing_to_input_file()
            my_new_file.db_data = f"\t{value}\n"
            my_new_file.writing_to_input_file()
        rul_pos_counter += 1
    query = f"Select SavedSolutionId From [Phreeqc].[Rule] Where Id = {rule_counter}"
    q = Queries(connection, query)
    save_solution = q.run_query()
    if save_solution is not None:
        my_new_file.db_data = f"\tSave solution\t{save_solution}\n"
    else:
        my_new_file.db_data = ''
    my_new_file.writing_to_input_file()
    my_new_file.db_data = "END\n"
    my_new_file.writing_to_input_file()
    rule_counter += 1
