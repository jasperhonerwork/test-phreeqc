import pyodbc
import numpy as np

class Db_connection:
    """Create a connection with the database"""
    def __init__(self):
        # self.server = "tcp:OBI-JASPER-LAP\JHMSSQLSERVER"
        # self.database = "ZGM_TransactieData"
        # self.username = "Depunt"
        # self.password = "P1nd4k44s"
        # self.server = "tcp:OBI-JASPER-LAP\JHMSSQLSERVER"
        # self.database = "DePuntPhreeqc"
        # self.username = "sa"
        # self.password = "Weetikniet-123"

        self.query = ''
        self.model_id = ''
        self.rule_id = ''
        self.pos = ''

    def connect(self):
        """Connect to the database"""
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:OBI-JASPER-LAP\JHMSSQLSERVER;DATABASE=ZGM_TransactieData;UID=Depunt;PWD=P1nd4k44s')
        connection.timeout = 720
        connection.autocommit = True
        cursor = connection.cursor()
        return cursor

    def run_query(self, connection, query):
        """Execute query and check for None types"""

        temp = connection.execute(query)
        temp_result = temp.fetchone()
        query_result = temp_result[0]
        # if temp_result != None:
        #     result = temp_result[0]
        #     if type(result) == str:
        #         result = result.replace('\r\n', '')
        #         return result
        #     else:
        #         return result
        # else:
        #     result = ''
        #     return result
        qc = Db_connection(query_result)
        checked_result = qc.empty_check()
        return checked_result
    # def run_query_array(self):
    #     temp = self.connection.execute(self.query)
    #     temp_result = temp.fetchone()
    #     return temp_result


    def count_rule(self):
        conn = Db_connection.connect()
        query = f"Select COUNT (Id) from [Phreeqc].[Rule] where ModelPhreeqcId = {self.model_id}"
        dbc = Db_connection.run_query(conn, query)
        return dbc

    def count_positions(self):
        query = f"Select COUNT (Id) from [Phreeqc].[RulePosition] where Ruleid = {self.rule_id}"
        q = Db_connection(self.connection, query)
        count_rul_pos = q.run_query()
        return count_rul_pos

    def first_rule_id(self):
        query = f"SELECT MIN(Id) FROM [Phreeqc].[Rule] WHERE ModelPhreeqcId = {self.model_id}"
        q = Db_connection(self.connection, query)
        first_rule_id = q.run_query()
        return first_rule_id

    def horizontal_or_vertical(self):
        if self.model_id == 1:
            fr = Db_connection(self.rule_id, self.model_id, self.connection)
            fr.horizontal()
        else:
            fr = Db_connection(self.rule_id, self.model_id)
            fr.vertical()

    def horizontal(self):
        counter = 1
        qc = Db_connection(self.connection)
        qc.rule_id = self.rule_id
        qc.model_id = self.model_id
        qc.connection = self.connection
        pos = qc.count_positions()
        while counter <= pos:

            qv = Db_connection(self.rule_id, counter, self.connection)
            qv.rule_id = self.rule_id
            qv.rule_pos_id = counter
            component = qv.get_component()
            print(f"{component}\t")

    def vertical(self):
        return

    def all_rule_ids(self):
        query = f"SELECT Id FROM [Phreeqc].[Rule] WHERE ModelPhreeqcId = {self.model_id}"
        q = Db_connection(self.connection, query)
        query_array = q.run_query_array()
        np.empty = [query_array]
        return np

    def rule_pos_id(self):
        query = f"Select Id from [Phreeqc].[RulePosition] where RuleId = {self.rule_id} and Position = {self.pos}"
        q = Db_connection(self.connection, query)
        pos_id = q.run_query()
        return pos_id

    # def get_title(self):
    #
    # def get_reaction(self):
    #
    # def get_subrule(self):
    #
    # def get_use_solution(self):
    #
    # def get_save_solution(self):

    def get_component(self):
        qid = Db_connection(self.connection)
        qid.pos = self.rule_pos
        qid.rule_id = self.rule_id
        pos_id = qid.rule_pos_id()
        query = f"SELECT rc.Name FROM [Phreeqc].[RuleComponent] AS rc LEFT JOIN [Phreeqc].[RulePosition] AS rp ON rp.ComponentId = rc.Id WHERE rp.Id = {pos_id}"
        qdb = Db_connection
        qdb.query = query
        result = qdb.run_query(self.connection)
        return result

    #def get_value(self):

    def empty_check(self):
        if self.query is not None:
            qc = Db_connection(self.query)
            query = qc.check_str()
            return query
        else:
            query = ''
            return query

    def check_str(self):
        if type(self.query) == str:
            query = Db_connection.clean_up_check()
            return query
        else:
            return self.query

    def clean_up_check(self):
        if type(self.query) == str:
            query = self.query.replace('\r\n', '')
            return query
        else:
            return self.query


# class QueryDb:
#     """Running queries"""
#     def __init__(self, connection, query):
#         self.connection = connection
#         self.query = query
#
#     def run_query(self):
#         """Execute query and check for None types"""
#
#         temp = self.connection.execute(self.query)
#         temp_result = temp.fetchone()
#         query_result = temp_result[0]
#         # if temp_result != None:
#         #     result = temp_result[0]
#         #     if type(result) == str:
#         #         result = result.replace('\r\n', '')
#         #         return result
#         #     else:
#         #         return result
#         # else:
#         #     result = ''
#         #     return result
#         qc = QueryCheck(query_result)
#         checked_result = qc.empty_check()
#         return checked_result
#     # def run_query_array(self):
#     #     temp = self.connection.execute(self.query)
#     #     temp_result = temp.fetchone()
#     #     return temp_result
#
# class QueryCount:
#     """Know how many rules and positions there are"""
#     def __init__(self, connection):
#         self.model_id = ''
#         self.rule_id = ''
#         self.connection = connection
#
#     def count_rule(self):
#         query = f"Select COUNT (Id) from [Phreeqc].[Rule] where ModelPhreeqcId = {self.model_id}"
#         q = QueryDb(self.connection, query)
#         amount_of_rules = q.run_query()
#         return amount_of_rules
#
#     def count_positions(self):
#         query = f"Select COUNT (Id) from [Phreeqc].[RulePosition] where Ruleid = {self.rule_id}"
#         q = QueryDb(self.connection, query)
#         count_rul_pos = q.run_query()
#         return count_rul_pos
#
# class QueriesId:
#     """Get the Id's for the rules and the positions"""
#     def __init__(self, connection):
#         self.model_id = ''
#         self.rule_id = ''
#         self.pos = ''
#         self.connection = connection
#
#     def first_rule_id(self):
#         query = f"SELECT MIN(Id) FROM [Phreeqc].[Rule] WHERE ModelPhreeqcId = {self.model_id}"
#         q = QueryDb(self.connection, query)
#         first_rule_id = q.run_query()
#         return first_rule_id
#
#     def all_rule_ids(self):
#         query = f"SELECT Id FROM [Phreeqc].[Rule] WHERE ModelPhreeqcId = {self.model_id}"
#         q = QueryDb(self.connection, query)
#         query_array = q.run_query_array()
#         np.empty = [query_array]
#         return np
#
#     def rule_pos_id(self):
#         query = f"Select Id from [Phreeqc].[RulePosition] where RuleId = {self.rule_id} and Position = {self.pos}"
#         q = QueryDb(self.connection, query)
#         pos_id = q.run_query()
#         return pos_id
#
# class FirstRule:
#     def __init__(self, rule_id, model_id, connection):
#         self.rule_id = rule_id
#         self.model_id = model_id
#         self.connection = connection
#
#     def horizontal_or_vertical(self):
#         if self.model_id == 1:
#             fr = FirstRule(self.rule_id, self.model_id, self.connection)
#             fr.horizontal()
#         else:
#             fr = FirstRule(self.rule_id, self.model_id)
#             fr.vertical()
#
#     def horizontal(self):
#         counter = 1
#         qc = QueryCount(self.connection)
#         qc.rule_id = self.rule_id
#         qc.model_id = self.model_id
#         qc.connection = self.connection
#         pos = qc.count_positions()
#         while counter <= pos:
#
#             qv = GetValue(self.rule_id, counter, self.connection)
#             qv.rule_id = self.rule_id
#             qv.rule_pos_id = counter
#             component = qv.get_component()
#             print(f"{component}\t")
#
#     def vertical(self):
#         return
#
#
#
#
# class GetRule:
#     def __init__(self, model_id, connection):
#         self.model_id = model_id
#         self.connection = connection
#
#     # def get_title(self):
#     #
#     # def get_reaction(self):
#     #
#     # def get_subrule(self):
#     #
#     # def get_use_solution(self):
#     #
#     # def get_save_solution(self):
#
# class GetValue:
#     def __init__(self, rule_id, rule_pos, connection):
#         self.rule_id = rule_id
#         self.rule_pos = rule_pos
#         self.connection = connection
#
#     def get_component(self):
#         qid = QueriesId(self.connection)
#         qid.pos = self.rule_pos
#         qid.rule_id = self.rule_id
#         pos_id = qid.rule_pos_id()
#         query = f"SELECT rc.Name FROM [Phreeqc].[RuleComponent] AS rc LEFT JOIN [Phreeqc].[RulePosition] AS rp ON rp.ComponentId = rc.Id WHERE rp.Id = {pos_id}"
#         qdb = QueryDb
#         qdb.query = query
#         result = qdb.run_query(self.connection)
#         return result
#
#     #def get_value(self):
#
# class QueryCheck:
#     def __init__(self, query):
#         self.query = query
#
#     def empty_check(self):
#         if self.query is not None:
#             qc = QueryCheck(self.query)
#             query = qc.check_str()
#             return query
#         else:
#             query = ''
#             return query
#
#     def check_str(self):
#         if type(self.query) == str:
#             query = QueryCheck.clean_up_check()
#             return query
#         else:
#             return self.query
#
#     def clean_up_check(self):
#         if type(self.query) == str:
#             query = self.query.replace('\r\n', '')
#             return query
#         else:
#             return self.query
