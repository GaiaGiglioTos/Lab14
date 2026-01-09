import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):
        self._model._grafo.clear()
        self._model._idMap.clear()
        self._view._ddNode.options.clear()
        id = self._view._ddStore.value
        k = self._view._txtIntK.value
        self._model.build_graph(int(id), int(k))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self.fillddNodi()
        self._view.update_page()

    def handleCerca(self, e):

        n = self._model._idMap[int(self._view._ddNode.value)]
        lp = self._model.getCammino(n)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {n.order_id}"))
        for o in lp:
            self._view.txt_result.controls.append(ft.Text(o.order_id))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass

    def fillddStore(self):
        store = self._model.getStore()
        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(s))


    def fillddNodi(self):
        nodi = self._model._grafo.nodes
        for n in nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(n.order_id))
