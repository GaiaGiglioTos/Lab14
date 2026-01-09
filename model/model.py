import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}


    def build_graph(self, id, k):
        ordini = DAO.getOrdini(id)
        self._grafo.add_nodes_from(ordini)
        for o in ordini:
            self._idMap[o.order_id] = o

        allEdges = DAO.getEdges(id, k, self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e[0], e[1], weight=e[2])


    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getStore(self):
        return DAO.getStore()

    def getCammino(self,n):
        albero = nx.dfs_tree(self._grafo,n)

        lp = []

        for t in list(albero.nodes()):
            temp = [t]

            while temp[0] != n:
                pred = nx.predecessor(self._grafo,n,temp[0])
                temp.insert(0,pred[0])

            if len(temp) > len(lp):
                lp = copy.deepcopy(temp)

        return lp

