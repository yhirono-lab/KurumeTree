import collections
import csv
import os
import numpy as np
import pandas as pd
import math
import argparse
from graphviz import Digraph
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split

import utils
import GraphViz as gv

class UsingTree(object):
    def __init__(self):
        self.root = None
        self.root_analysis = TreeAnalysis()

    def fit(self, data, label, label_names, annotation):
        print(f'predict_data:{data.shape}/disease:{label_names.shape}')

        node_id = 0
        leaf_id = 0
        self.leaf_num = 0
        
        # CD15 or CD30 or EBER or PAX5 use/not use
        self.root = Node()
        self.root.data = data
        self.root.label = label
        self.root.annotation = annotation
        self.root.node_id = node_id
        self.root.leaf_id = None
        self.root.num_samples = len(self.root.label)
        self.root.num_classes = len(np.unique(self.root.label))
        self.root.target_count = np.asarray([len(self.root.label[self.root.label == i]) for i in range(len(label_names))])
        self.root.split = np.array(
            ((self.root.data[:, 5] == '+') | (self.root.data[:, 5] == '-')) &
            ((self.root.data[:, 7] == '+') | (self.root.data[:, 7] == '-')) &
            ((self.root.data[:, 12] == '+') | (self.root.data[:, 12] == '-')) &
            ((self.root.data[:, 13] == '+') | (self.root.data[:, 13] == '-'))
        )
        self.root.feature = [5,7,12,13]
        node_id += 1

        # CD15 or CD30 or EBER or PAX5 use -> Hodgkin(?)
        self.root.left = Node()
        self.root.edge_left = 'use'
        self.node1 = self.root.left
        self.node1.data = self.root.data[self.root.split]
        self.node1.label = self.root.label[self.root.split]
        self.node1.annotation = self.root.annotation[self.root.split]
        self.node1.node_id = node_id
        self.node1.leaf_id = leaf_id
        self.leaf_num += 1
        self.node1.num_samples = len(self.node1.label)
        self.node1.num_classes = len(np.unique(self.node1.label))
        self.node1.target_count = np.asarray([len(self.node1.label[self.node1.label == i]) for i in range(len(label_names))])
        node_id += 1
        leaf_id += 1
        dirpath = f'{output}/unu_depth1/leafs_data'
        utils.save_leaf_data(self.node1.annotation, dirpath, 0)
        print(self.node1.num_samples, self.node1.target_count)

        # CD15 or CD30 or EBER or PAX5 not use -> not Hodgkin(?)
        self.root.right = Node()
        self.root.edge_right = 'not use'
        self.node2_sub = self.root.right
        self.node2_sub.sub_node = True
        self.node2_sub.data = self.root.data[~self.root.split]
        self.node2_sub.label = self.root.label[~self.root.split]
        self.node2_sub.annotation = self.root.annotation[~self.root.split]
        self.node2_sub.node_id = node_id
        self.node2_sub.leaf_id = None
        self.node2_sub.num_samples = len(self.node2_sub.label)
        self.node2_sub.num_classes = len(np.unique(self.node2_sub.label))
        self.node2_sub.target_count = np.asarray([len(self.node2_sub.label[self.node2_sub.label == i]) for i in range(len(label_names))])
        node_id += 1
        dirpath = f'{output}/unu_depth1/leafs_data'
        utils.save_leaf_data(self.node2_sub.annotation, dirpath, 1)
        print(self.node2_sub.num_samples, self.node2_sub.target_count)
        
        # CD3 +/(- or not use)
        self.node2_sub.right = Node()
        self.node2_sub.edge_right = ''
        self.node2 = self.node2_sub.right
        self.node2.data = self.node2_sub.data
        self.node2.label = self.node2_sub.label
        self.node2.annotation = self.node2_sub.annotation
        self.node2.node_id = node_id
        self.node2.leaf_id = None
        self.node2.num_samples = len(self.node2.label)
        self.node2.num_classes = len(np.unique(self.node2.label))
        self.node2.target_count = np.asarray([len(self.node2.label[self.node2.label == i]) for i in range(len(label_names))])
        self.node2.split = np.array((self.node2.data[:, 0] == '+'))
        self.node2.feature = [0]
        node_id += 1

        # CD3 + -> T-cell(?)
        self.node2.left = Node()
        self.node2.edge_left = '+'
        self.node3 = self.node2.left
        self.node3.data = self.node2.data[self.node2.split]
        self.node3.label = self.node2.label[self.node2.split]
        self.node3.annotation = self.node2.annotation[self.node2.split]
        self.node3.node_id = node_id
        self.node3.leaf_id = leaf_id
        self.leaf_num += 1
        self.node3.num_samples = len(self.node3.label)
        self.node3.num_classes = len(np.unique(self.node3.label))
        self.node3.target_count = np.asarray([len(self.node3.label[self.node3.label == i]) for i in range(len(label_names))])
        node_id += 1
        leaf_id += 1
        dirpath = f'{output}/unu_depth2/leafs_data'
        utils.save_leaf_data(self.node3.annotation, dirpath, 0)
        print(self.node3.num_samples, self.node3.target_count)

        # CD3 - or not use -> not T-cell(?)
        self.node2.right = Node()
        self.node2.edge_right = '- or not use'
        self.node4_sub = self.node2.right
        self.node4_sub.sub_node = True
        self.node4_sub.data = self.node2.data[~self.node2.split]
        self.node4_sub.label = self.node2.label[~self.node2.split]
        self.node4_sub.annotation = self.node2.annotation[~self.node2.split]
        self.node4_sub.node_id = node_id
        self.node4_sub.leaf_id = None
        self.node4_sub.num_samples = len(self.node4_sub.label)
        self.node4_sub.num_classes = len(np.unique(self.node4_sub.label))
        self.node4_sub.target_count = np.asarray([len(self.node4_sub.label[self.node4_sub.label == i]) for i in range(len(label_names))])
        self.node4_sub.split = np.array((self.node4_sub.data[:, 6] == '+'))
        node_id += 1
        dirpath = f'{output}/unu_depth2/leafs_data'
        utils.save_leaf_data(self.node4_sub.annotation, dirpath, 1)
        print(self.node4_sub.num_samples, self.node4_sub.target_count)

        # CD20 +/(- or not use)
        self.node4_sub.right = Node()
        self.node4_sub.edge_right = ''
        self.node4 = self.node4_sub.right
        self.node4.data = self.node4_sub.data
        self.node4.label = self.node4_sub.label
        self.node4.annotation = self.node4_sub.annotation
        self.node4.node_id = node_id
        self.node4.leaf_id = None
        self.node4.num_samples = len(self.node4.label)
        self.node4.num_classes = len(np.unique(self.node4.label))
        self.node4.target_count = np.asarray([len(self.node4.label[self.node4.label == i]) for i in range(len(label_names))])
        self.node4.split = np.array((self.node4.data[:, 6] == '+'))
        self.node4.feature = [6]
        node_id += 1

        # CD20 - or not use -> not B-cell(?)
        self.node4.right = Node()
        self.node4.edge_right = '- or not use'
        self.node5 = self.node4.right
        self.node5.data = self.node4.data[~self.node4.split]
        self.node5.label = self.node4.label[~self.node4.split]
        self.node5.annotation = self.node4.annotation[~self.node4.split]
        self.node5.node_id = node_id
        self.node5.leaf_id = leaf_id
        self.leaf_num += 1
        self.node5.num_samples = len(self.node5.label)
        self.node5.num_classes = len(np.unique(self.node5.label))
        self.node5.target_count = np.asarray([len(self.node5.label[self.node5.label == i]) for i in range(len(label_names))])
        node_id += 1
        leaf_id += 1
        dirpath = f'{output}/unu_depth3/leafs_data'
        utils.save_leaf_data(self.node5.annotation, dirpath, 1)
        print(self.node5.num_samples, self.node5.target_count)
        
        # CD20 + -> B-cell(?)
        self.node4.left = Node()
        self.node4.edge_left = '+'
        self.node6_sub = self.node4.left
        self.node6_sub.sub_node = True
        self.node6_sub.data = self.node4.data[self.node4.split]
        self.node6_sub.label = self.node4.label[self.node4.split]
        self.node6_sub.annotation = self.node4.annotation[self.node4.split]
        self.node6_sub.node_id = node_id
        self.node6_sub.leaf_id = None
        self.leaf_num += 1
        self.node6_sub.num_samples = len(self.node6_sub.label)
        self.node6_sub.num_classes = len(np.unique(self.node6_sub.label))
        self.node6_sub.target_count = np.asarray([len(self.node6_sub.label[self.node6_sub.label == i]) for i in range(len(label_names))])
        node_id += 1
        dirpath = f'{output}/unu_depth3/leafs_data'
        utils.save_leaf_data(self.node6_sub.annotation, dirpath, 0)
        print(self.node6_sub.num_samples, self.node6_sub.target_count)

        # bcl2 & bcl6 use/not use
        self.node6_sub.right = Node()
        self.node6_sub.edge_right = ''
        self.node6 = self.node6_sub.right
        self.node6.data = self.node6_sub.data
        self.node6.label = self.node6_sub.label
        self.node6.annotation = self.node6_sub.annotation
        self.node6.node_id = node_id
        self.node6.leaf_id = None
        self.node6.num_samples = len(self.node6.label)
        self.node6.num_classes = len(np.unique(self.node6.label))
        self.node6.target_count = np.asarray([len(self.node6.label[self.node6.label == i]) for i in range(len(label_names))])
        self.node6.split = np.array(
            (self.node6.data[:, 21] == '+') #FDC
        )
        self.node6.feature = [21]
        # self.node6.split = np.array(
        #     ((self.node6.data[:, 9] == '+') | (self.node6.data[:, 9] == '-')) & #bcl2,6
        #     ((self.node6.data[:, 10] == '+') | (self.node6.data[:, 10] == '-'))
        # )
        # self.node6.feature = [9,10]
        # self.node6.split = np.array(
        #     ((self.node6.data[:, 4] == '+') | (self.node6.data[:, 4] == '-')) &
        #     ((self.node6.data[:, 6] == '+') | (self.node6.data[:, 6] == '-')) &
        #     ((self.node6.data[:, 9] == '+') | (self.node6.data[:, 9] == '-')) &
        #     ((self.node6.data[:, 10] == '+') | (self.node6.data[:, 10] == '-'))
        # )
        # self.node6.feature = [4,6,9,10]
        node_id += 1
        print(self.node6.num_samples, self.node6.target_count)

        # FDC - or not use
        self.node6.right = Node()
        self.node6.edge_right = '- or not use'
        self.node7 = self.node6.right
        self.node7.data = self.node6.data[~self.node6.split]
        self.node7.label = self.node6.label[~self.node6.split]
        self.node7.annotation = self.node6.annotation[~self.node6.split]
        self.node7.node_id = node_id
        self.node7.leaf_id = leaf_id
        self.leaf_num += 1
        self.node7.num_samples = len(self.node7.label)
        self.node7.num_classes = len(np.unique(self.node7.label))
        self.node7.target_count = np.asarray([len(self.node7.label[self.node7.label == i]) for i in range(len(label_names))])
        node_id += 1
        leaf_id += 1
        dirpath = f'{output}/unu_depth4/leafs_data'
        utils.save_leaf_data(self.node7.annotation, dirpath, 1)
        print(self.node7.num_samples, self.node7.target_count)
        
        # FDC +
        self.node6.left = Node()
        self.node6.edge_left = '+'
        self.node8_sub = self.node6.left
        self.node8_sub.sub_node = True
        self.node8_sub.data = self.node6.data[self.node6.split]
        self.node8_sub.label = self.node6.label[self.node6.split]
        self.node8_sub.annotation = self.node6.annotation[self.node6.split]
        self.node8_sub.node_id = node_id
        self.node8_sub.leaf_id = None
        self.leaf_num += 1
        self.node8_sub.num_samples = len(self.node8_sub.label)
        self.node8_sub.num_classes = len(np.unique(self.node8_sub.label))
        self.node8_sub.target_count = np.asarray([len(self.node8_sub.label[self.node8_sub.label == i]) for i in range(len(label_names))])
        node_id += 1
        dirpath = f'{output}/unu_depth4/leafs_data'
        utils.save_leaf_data(self.node8_sub.annotation, dirpath, 0)
        print(self.node8_sub.num_samples, self.node8_sub.target_count)

        # # MUM1 use/not use
        # self.node8_sub.right = Node()
        # self.node8_sub.edge_right = ''
        # self.node8 = self.node8_sub.right
        # self.node8.data = self.node8_sub.data
        # self.node8.label = self.node8_sub.label
        # self.node8.annotation = self.node8_sub.annotation
        # self.node8.node_id = node_id
        # self.node8.leaf_id = None
        # self.node8.num_samples = len(self.node8.label)
        # self.node8.num_classes = len(np.unique(self.node8.label))
        # self.node8.target_count = np.asarray([len(self.node8.label[self.node8.label == i]) for i in range(len(label_names))])
        # self.node8.split = np.array(
        #     ((self.node8.data[:, 11] == '+') | (self.node8.data[:, 11] == '-'))
        # )
        # self.node8.feature = [11]
        # node_id += 1
        # print(self.node8.num_samples, self.node8.target_count)

        # # MUM1 use
        # self.node8.left = Node()
        # self.node8.edge_left = 'use'
        # self.node9 = self.node8.left
        # self.node9.data = self.node8.data[self.node8.split]
        # self.node9.label = self.node8.label[self.node8.split]
        # self.node9.annotation = self.node8.annotation[self.node8.split]
        # self.node9.node_id = node_id
        # self.node9.leaf_id = leaf_id
        # self.leaf_num += 1
        # self.node9.num_samples = len(self.node9.label)
        # self.node9.num_classes = len(np.unique(self.node9.label))
        # self.node9.target_count = np.asarray([len(self.node9.label[self.node9.label == i]) for i in range(len(label_names))])
        # node_id += 1
        # leaf_id += 1
        # dirpath = f'{output}/unu_depth5/leafs_data'
        # utils.save_leaf_data(self.node9.annotation, dirpath, 0)
        # print(self.node9.num_samples, self.node9.target_count)

        # # MUM1 not use
        # self.node8.right = Node()
        # self.node8.edge_right = 'not use'
        # self.node10 = self.node8.right
        # self.node10.data = self.node8.data[~self.node8.split]
        # self.node10.label = self.node8.label[~self.node8.split]
        # self.node10.annotation = self.node8.annotation[~self.node8.split]
        # self.node10.node_id = node_id
        # self.node10.leaf_id = leaf_id
        # self.leaf_num += 1
        # self.node10.num_samples = len(self.node10.label)
        # self.node10.num_classes = len(np.unique(self.node10.label))
        # self.node10.target_count = np.asarray([len(self.node10.label[self.node10.label == i]) for i in range(len(label_names))])
        # node_id += 1
        # leaf_id += 1
        # dirpath = f'{output}/unu_depth5/leafs_data'
        # utils.save_leaf_data(self.node10.annotation, dirpath, 1)
        # print(self.node10.num_samples, self.node10.target_count)
        
        
        # self.leaf_hist = self.root_analysis.get_leaf_probability(self.root, self.leaf_num, label_names)
        # self.predict(data, label, label_names)

    def predict(self, data, label, label_names):
        # 入力データが到達した葉と確率の計算
        self.leaf_data = [[] for i in range(self.leaf_num)]
        self.pred = []
        for i, d in enumerate(data):
            count = np.zeros(len(label_names))
            self.root.predict(i, d, count, self.leaf_data)
            self.pred.append(count)
        self.pred = np.array(self.pred)
        self.pred = self.pred / np.sum(self.pred, 1, keepdims=True)

class TreeAnalysis(object):
    def __init__(self):
        self.importances = None
        self.probabilities = None

    def get_leaf_probability(self, node, leaf_num, label_names):
        self.probabilities = np.zeros((leaf_num, len(label_names)))
        self.search_leaf(node)
        print(self.probabilities)
        self.probabilities = self.probabilities / np.sum(self.probabilities, 1, keepdims=True)

        return self.probabilities
    
    def search_leaf(self, node):
        if node.leaf_id is not None:
            target_count = node.target_count
            self.probabilities[node.leaf_id] += target_count
            return

        self.search_leaf(node.left)
        self.search_leaf(node.right)

class Node(object):
    def __init__(self):
        self.node_id = None
        self.leaf_id = None
        self.sub_node = False
        self.left = None
        self.right = None
        self.feature = None
        self.target_count = None
        self.info_gain = None
        self.num_samples = None
        self.num_classes = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use/not use による決定木の作成')
    parser.add_argument('--mode', help='choose disease name mode (Simple or Full)', choices=['Simple','Full'], default='Simple')
    
    args = parser.parse_args()

    # 学習データの読み込み
    output = f'./result_teacher/{args.mode}'
    data, label, feature_names, label_names, annotation = utils.readCSV_svs(f'./data', args.mode, unu_flag=False)
    print(data.shape)
    
    tree = UsingTree()
    tree.fit(data, label, label_names, annotation)

    gv.GraphViz_teacher(tree, feature_names, label_names, f'{output}/tree')