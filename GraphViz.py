from graphviz import Digraph
import numpy as np
import os

class GraphViz(object):
    def __init__(self, tree, feature_names, search, dirname, depth=None, option=None):
        self.feature_names = feature_names
        self.depth = depth
        self.dirname = dirname
        self.tree = tree
        self.search = search
        self.option = option
        
        self.makeGraph()
        
    def makeGraph(self):
        if not os.path.isdir(self.dirname):
            os.makedirs(self.dirname)
            
        G = Digraph(format='png')
        G.attr('node', shape='rect', fontsize='30')

        n = self.tree.root
        self.makeGraph_add_Node(G, n)
        self.makeGraph_add_edge(G, n)

        if self.option is 1:
            G.render(f'{self.dirname}/mytree{self.depth}_normalize')
        else:
            G.render(f'{self.dirname}/mytree{self.depth}')



    def makeGraph_add_Node(self, G, n):
        if n.leaf_id is None:
            # G.node(str(n.id), str(n.mensen) + "\n{0:.4}".format(n.entropy_b) + "\n{0:.4}".format(n.entropy) + "\n" + str(n.count_pm) + "/" + str(n.num_all), shape='circle')
            G.node(str(n.node_id), str(self.feature_names[n.feature]), shape='ellipse')
            if n.left is not None:
                self.makeGraph_add_Node(G, n.left)
            if n.right is not None:
                self.makeGraph_add_Node(G, n.right)
        elif n.leaf_id is not None:
            data_str = ''
            sort_idx = np.argsort(-n.target_count) 
            for i,idx in enumerate(sort_idx):
                if n.target_count[idx] > 0:
                    if i > 0:
                        data_str += "\n"
                    data_str += f'{self.search[idx]}:{n.target_count[idx]}'
                if i >= 8:
                    break
            # G.node(str(n.id), data_str + str(n.num_all) + "\n" + str(n.num_dis), color='cyan', )
            G.node(str(n.node_id), data_str, color='cyan')
        return


    def makeGraph_add_edge(self, G, n):
        if n.left is not None:
            G.edge(str(n.node_id), str(n.left.node_id), label='not use')
            self.makeGraph_add_edge(G, n.left)
        if n.right is not None:
            G.edge(str(n.node_id), str(n.right.node_id), label='use')
            self.makeGraph_add_edge(G, n.right)
        return

class GraphViz_teacher(object):
    def __init__(self, tree, feature_names, search, dirname):
        self.feature_names = feature_names
        self.dirname = dirname
        self.tree = tree
        self.search = search
        
        self.makeGraph()
        
    def makeGraph(self):
        if not os.path.isdir(self.dirname):
            os.makedirs(self.dirname)
            
        G = Digraph(format='png')
        G.attr('node', shape='rect', fontsize='18')

        n = self.tree.root
        self.makeGraph_add_Node(G, n)
        self.makeGraph_add_edge(G, n)

        G.render(f'{self.dirname}/mytree')


    def makeGraph_add_Node(self, G, n):
        if n.sub_node:
            data_str = ''
            sort_idx = np.argsort(-n.target_count) 
            for i,idx in enumerate(sort_idx):
                if n.target_count[idx] > 0:
                    if i > 0:
                        data_str += "\n"
                    data_str += f'{self.search[idx]}:{n.target_count[idx]}'
                if i >= 5:
                    break
            data_str += f'\ntotal:{n.num_samples}/types:{len(np.unique(n.label))}'
            # G.node(str(n.id), data_str + str(n.num_all) + "\n" + str(n.num_dis), color='cyan', )
            G.node(str(n.node_id), data_str, color='cyan')
            if n.left is not None:
                self.makeGraph_add_Node(G, n.left)
            if n.right is not None:
                self.makeGraph_add_Node(G, n.right)

        elif n.leaf_id is None:
            feature_name = ''
            for f in n.feature:
                feature_name = feature_name + self.feature_names[f] + '\n'
            G.node(str(n.node_id), str(feature_name), shape='ellipse')
            if n.left is not None:
                self.makeGraph_add_Node(G, n.left)
            if n.right is not None:
                self.makeGraph_add_Node(G, n.right)

        elif n.leaf_id is not None:
            data_str = ''
            sort_idx = np.argsort(-n.target_count) 
            for i,idx in enumerate(sort_idx):
                if n.target_count[idx] > 0:
                    if i > 0:
                        data_str += "\n"
                    data_str += f'{self.search[idx]}:{n.target_count[idx]}'
                if i >= 5:
                    break
            data_str += f'\ntotal:{n.num_samples}/types:{len(np.unique(n.label))}'
            # G.node(str(n.id), data_str + str(n.num_all) + "\n" + str(n.num_dis), color='cyan', )
            G.node(str(n.node_id), data_str, color='cyan')
        return


    def makeGraph_add_edge(self, G, n):
        print(n.node_id)
        if n.left is not None:
            G.edge(str(n.node_id), str(n.left.node_id), label=n.edge_left)
            self.makeGraph_add_edge(G, n.left)
        if n.right is not None:
            G.edge(str(n.node_id), str(n.right.node_id), label=n.edge_right)
            self.makeGraph_add_edge(G, n.right)
        return