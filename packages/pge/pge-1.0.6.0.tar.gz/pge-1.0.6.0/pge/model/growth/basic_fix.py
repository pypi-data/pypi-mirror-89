import numpy as np
import networkx as nx

from pge.model.growth.basic import BasicGrowth


class FixGrowth(BasicGrowth):
    def __init__(self, graph, deg, typ):
        super().__init__(graph, deg)
        self.typ = typ

    def proceed(self, n, save, attr="cnt"):
        nw_graph = self.gr.clean_copy()
        for node in nw_graph.get_ids():
            nw_graph.set_attr(node, attr, -1)
        nw_graph = self.prep(nw_graph)

        count = self.gr.size()
        for _ in np.arange(n):
            print(_)
            if self.deg[0] == "const":
                nodes = self.choice(nw_graph, self.deg[1])
            else:
                nodes = self.choice(nw_graph, self.deg[0](self.deg[1]))

            for node in nodes:
                nw_graph.add_edge(str(count), node)
            nw_graph.set_attr(str(count), attr, _)
            count += 1

            if nw_graph.size() > self.gr.size():
                if self.typ == "un":
                    del_node = np.random.choice(nw_graph.get_ids(stable=True))
                else:
                    ids = nw_graph.get_ids(stable=True)
                    vals = nw_graph.get_attributes(attr)
                    del_node = np.random.choice(ids[vals == np.min(vals)])
                nw_graph.del_node(del_node)
                nw_graph = self.clean(nw_graph)
            else:
                nw_graph = self.prep(nw_graph)
            nx.write_graphml(nw_graph.get_nx_graph(), save + str(_) + ".graphml")

    def prep(self, graph):
        return graph

    def clean(self, graph):
        return graph
