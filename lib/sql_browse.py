import sqlite3

class SQL_requestions:
    """
        Маленькая либа для sql запросов
    """
    def __init__(self,path):
        """
            >>> path - путь для взаимодействия с базой данных
        """
        connect = sqlite3.connect(path)
        self.cursor = connect.cursor()
        
    def request(self,request_type:str, Table_name:str,Variable:str = None, Condition:str = None, arg:tuple = None):
        """
            >>> request_type:str - тип запроса (SELECT, INSERT INTO,..)
            >>> Table_name - имя таблицы для взаимодействия Пример: "FROM TABLE"
            >>> Variable - запрашиваемое поле таблицы
            >>> Condition - условие (напр Where)
            >>> *args - некоторые дополонительные аргументы запроса. Вводить через запятую. Напр: Num1, '=', Num2

        """
        responce_head = f"{request_type} {Variable} {Table_name} {Condition}"
        
        if Condition is not None:
            for conditions in arg:
                conditions = str(conditions)
                responce_head = responce_head +' ' + conditions
            print(responce_head)
        try:
            self.resp = self.cursor.execute(responce_head)
            _resp = self.resp.fetchall()
            self.cursor.close()
            return _resp
        except Exception as e:
            print('Ошибка Sql_request: ', e)
            

        

    
    
        