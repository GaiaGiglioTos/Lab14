from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getStore():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.store_id s
from stores s """

        cursor.execute(query)

        for row in cursor:
            result.append(row["s"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOrdini(id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
from orders o
where o.store_id = %s"""

        cursor.execute(query,(id,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(k,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id as id1, o2.order_id as id2
from orders o1, orders o2
where DATEDIFF(o1.order_date, o2.order_date ) < %s
and DATEDIFF(o1.order_date, o2.order_date ) > 0
and o1.order_id <> o2.order_id 
"""

        cursor.execute(query, (k,))

        for row in cursor:
            if row["id1"] in idMap and row["id2"] in idMap:
                result.append((idMap[row["id1"]], idMap[row["id2"]]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(id1, id2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select sum(oi1.quantity) + sum(oi2.quantity) as N
from order_items oi1, order_items oi2
where oi1.order_id = %s
and oi2.order_id = %s"""

        cursor.execute(query, (id1,id2))

        for row in cursor:
            result.append(row["N"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """Select DISTINCT o1.order_id as id1, o2.order_id as id2, count(oi.quantity+ oi2.quantity) as cnt
                    from orders o1, orders o2, order_items oi, order_items oi2 
                    where o1.store_id=%s
                    and o1.store_id=o2.store_id 
                    and o1.order_date > o2.order_date
                    and oi.order_id = o1.order_id
                    and oi2.order_id  = o2.order_id
                    and DATEDIFF(o1.order_Date, o2.order_date) < %s
                    group by o1.order_id, o2.order_id	"""

        cursor.execute(query, (store, k))

        for row in cursor:
            results.append((idMap[row["id1"]], idMap[row["id2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results
