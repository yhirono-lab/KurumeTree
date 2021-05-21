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

        node_id = np.zeros(1)
        self.leaf_num = 0
        
        # CD30 or EBER or PAX5 use/not use
        self.root = Node()
        self.root.data = data
        self.root.label = label
        self.root.annotation = annotation
        self.root.depth = 0
        self.root.node_id = 0
        self.root.leaf_id = None
        self.root.num_samples = len(self.root.label)
        self.root.num_classes = len(np.unique(self.root.label))
        self.root.target_count = np.asarray([len(self.root.label[self.root.label == i]) for i in range(len(label_names))])
        self.root.feature = [7,12,13]

        self.root.left = Node()
        self.root.edge_left = 'use'
        self.node1 = self.root.left
        self.node1.data = self.root.data[
            ((self.root.data[:, 7] == '+') | (self.root.data[:, 7] == '-')) &
            ((self.root.data[:, 12] == '+') | (self.root.data[:, 12] == '-')) &
            ((self.root.data[:, 13] == '+') | (self.root.data[:, 13] == '-'))
        ]
        self.node1.label = self.root.label[
            ((self.root.data[:, 7] == '+') | (self.root.data[:, 7] == '-')) &
            ((self.root.data[:, 12] == '+') | (self.root.data[:, 12] == '-')) &
            ((self.root.data[:, 13] == '+') | (self.root.data[:, 13] == '-'))
        ]

        self.node1.annotation = self.root.annotation[
            ((self.root.data[:, 7] == '+') | (self.root.data[:, 7] == '-')) &
            ((self.root.data[:, 12] == '+') | (self.root.data[:, 12] == '-')) &
            ((self.root.data[:, 13] == '+') | (self.root.data[:, 13] == '-'))
        ]
        self.node1.depth = 1
        self.node1.node_id = 1
        self.node1.leaf_id = 0
        self.leaf_num += 1
        self.node1.num_samples = len(self.node1.label)
        self.node1.num_classes = len(np.unique(self.node1.label))
        self.node1.target_count = np.asarray([len(self.node1.label[self.node1.label == i]) for i in range(len(label_names))])
        print(label_names)
        print(self.node1.num_samples, self.node1.target_count)
        
        self.root.right = Node()
        self.root.edge_right = 'not use'
        self.node2 = self.root.right
        self.node2.data = self.root.data[
            (self.root.data[:, 7] == '') |
            (self.root.data[:, 12] == '') |
            (self.root.data[:, 13] == '')
        ]
        self.node2.label = self.root.label[
            (self.root.data[:, 7] == '') |
            (self.root.data[:, 12] == '') |
            (self.root.data[:, 13] == '')
        ]
        self.node2.annotation = self.root.annotation[
            (self.root.data[:, 7] == '') |
            (self.root.data[:, 12] == '') |
            (self.root.data[:, 13] == '')
        ]
        self.node2.depth = 1
        self.node2.node_id = 2
        self.node2.leaf_id = None
        self.node2.num_samples = len(self.node2.label)
        self.node2.num_classes = len(np.unique(self.node2.label))
        self.node2.target_count = np.asarray([len(self.node2.label[self.node2.label == i]) for i in range(len(label_names))])
        self.node2.feature = [0]
        print(self.node2.num_samples, self.node2.target_count)

        self.node2.left = Node()
        self.node2.edge_left = '+'
        self.node3 = self.node2.left
        self.node3.data = self.node2.data[
            (self.node2.data[:, 0] == '+')
        ]
        self.node3.label = self.node2.label[
            (self.node2.data[:, 0] == '+')
        ]
        self.node3.annotation = self.node2.annotation[
            (self.node2.data[:, 0] == '+')
        ]
        self.node3.depth = 2
        self.node3.node_id = 3
        self.node3.leaf_id = 1
        self.leaf_num += 1
        self.node3.num_samples = len(self.node3.label)
        self.node3.num_classes = len(np.unique(self.node3.label))
        self.node3.target_count = np.asarray([len(self.node3.label[self.node3.label == i]) for i in range(len(label_names))])
        print(self.node3.num_samples, self.node3.target_count)

        self.node2.right = Node()
        self.node2.edge_right = '- or not use'
        self.node4 = self.node2.right
        self.node4.data = self.node2.data[
            (self.node2.data[:, 0] == '-') |
            (self.node2.data[:, 0] == '')
        ]
        self.node4.label = self.node2.label[
            (self.node2.data[:, 0] == '-') |
            (self.node2.data[:, 0] == '')
        ]
        self.node4.annotation = self.node2.annotation[
            (self.node2.data[:, 0] == '-') |
            (self.node2.data[:, 0] == '')
        ]
        self.node4.depth = 2
        self.node4.node_id = 4
        self.node4.leaf_id = None
        self.node4.num_samples = len(self.node4.label)
        self.node4.num_classes = len(np.unique(self.node4.label))
        self.node4.target_count = np.asarray([len(self.node4.label[self.node4.label == i]) for i in range(len(label_names))])
        self.node4.feature = [6]
        print(self.node4.num_samples, self.node4.target_count)

        self.node4.left = Node()
        self.node4.edge_left = '+'
        self.node5 = self.node4.left
        self.node5.data = self.node4.data[
            (self.node4.data[:, 6] == '+')
        ]
        self.node5.label = self.node4.label[
            (self.node4.data[:, 6] == '+')
        ]
        self.node5.annotation = self.node4.annotation[
            (self.node4.data[:, 6] == '+')
        ]
        self.node5.depth = 3
        self.node5.node_id = 5
        self.node5.leaf_id = 2
        self.leaf_num += 1
        self.node5.num_samples = len(self.node5.label)
        self.node5.num_classes = len(np.unique(self.node5.label))
        self.node5.target_count = np.asarray([len(self.node5.label[self.node5.label == i]) for i in range(len(label_names))])
        print(self.node5.num_samples, self.node5.target_count)

        self.node4.right = Node()
        self.node4.edge_right = '- or not use'
        self.node6 = self.node4.right
        self.node6.data = self.node4.data[
            (self.node4.data[:, 6] == '-') |
            (self.node4.data[:, 6] == '')
        ]
        self.node6.label = self.node4.label[
            (self.node4.data[:, 6] == '-') |
            (self.node4.data[:, 6] == '')
        ]
        self.node6.annotation = self.node4.annotation[
            (self.node4.data[:, 6] == '-') |
            (self.node4.data[:, 6] == '')
        ]
        self.node6.depth = 3
        self.node6.node_id = 6
        self.node6.leaf_id = 3
        self.leaf_num += 1
        self.node6.num_samples = len(self.node6.label)
        self.node6.num_classes = len(np.unique(self.node6.label))
        self.node6.target_count = np.asarray([len(self.node6.label[self.node6.label == i]) for i in range(len(label_names))])
        print(self.node6.num_samples, self.node6.target_count)

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
        self.depth = None
        self.node_id = None
        self.leaf_id = None
        self.left = None
        self.right = None
        self.feature = None
        self.target_count = None
        self.info_gain = None
        self.num_samples = None
        self.num_classes = None

    def split_node(self, sample, target, depth, node_id, leaf_num, annotation):
        self.depth = depth
        self.node_id = int(node_id[0])
        self.num_samples = len(target)
        self.num_classes = len(np.unique(target))
        node_id += 1
        
        # 全labelの個数をカウント
        self.target_count = np.asarray([len(target[target == i]) for i in range(len(label_names))])

        # targetが1種類になったら終了
        if len(np.unique(target)) == 1:
            self.leaf_id = leaf_num
            leaf_num += 1
            # print(leaf_num, self.target_count)
            dirpath = f'./result/{args.mode}/unu_depth{self.depth}/leafs_data'
            utils.save_leaf_data(annotation, dirpath, self.leaf_id)
            return leaf_num
        
        # 各要素で分割して獲得情報量の計算、最大値で決定木の分割
        self.info_gain = 0.0
        f_loop_order = range(sample.shape[1])
        entropy = None
        for f in f_loop_order:
            target_l = target[sample[:, f] == 0]
            target_r = target[sample[:, f] == 1]

            gain, ent = self.calc_info_gain(target, target_l, target_r)
            if self.info_gain < gain:
                self.info_gain = gain
                self.feature = f
                entropy = ent

        # 獲得情報量がゼロになったら終了
        if self.info_gain == 0.0:
            self.leaf_id = leaf_num
            leaf_num += 1
            # print(leaf_num, self.target_count)
            dirpath = f'./result/{args.mode}/unu_depth{self.depth}/leafs_data'
            utils.save_leaf_data(annotation, dirpath, self.leaf_id)
            return leaf_num

        print(self.depth, feature_names[self.feature], self.feature, entropy, entropy - self.info_gain)

        # 子ノードへ分岐
        sample_l = sample[sample[:, self.feature] == 0]
        target_l = target[sample[:, self.feature] == 0]
        annotation_l = annotation[sample[:, self.feature] == 0]
        self.left = Node()
        leaf_num = self.left.split_node(sample_l, target_l, depth+1, node_id, leaf_num, annotation_l)

        sample_r = sample[sample[:, self.feature] == 1]
        target_r = target[sample[:, self.feature] == 1]
        annotation_r = annotation[sample[:, self.feature] == 1]
        self.right = Node()
        leaf_num = self.right.split_node(sample_r, target_r, depth+1, node_id, leaf_num, annotation_r)

        return leaf_num

    def criterion_func(self, target, classes, weight):
        numdata = len(target)
        entropy = 0
        
        # データ数の正規化無し
        # if option == 0:
        if numdata != 0:
            for c in classes:
                p = float(len(target[target == c])) / numdata
                if p != 0.0:
                    entropy -= p * np.log2(p)
            
        return entropy

    def calc_info_gain(self, target_p, target_cl, target_cr):
        classes, weight = np.unique(target_p, return_counts=True)

        entropy_p = self.criterion_func(target_p, classes, weight)
        entropy_cl = self.criterion_func(target_cl, classes, weight)
        entropy_cr = self.criterion_func(target_cr, classes, weight)
        return entropy_p - len(target_cl) / float(len(target_p)) * entropy_cl - len(target_cr) / float(len(target_p)) * entropy_cr, entropy_p

    def predict(self, data_id, sample, count, leaf_data):
        if self.feature is None:
            count += self.target_count
            leaf_data[self.leaf_id].append(data_id)

        else:
            if sample[self.feature] == 0:
                self.left.predict(data_id, sample, count, leaf_data)
            if sample[self.feature] == 1:
                self.right.predict(data_id, sample, count, leaf_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use/not use による決定木の作成')
    parser.add_argument('--mode', help='choose disease name mode (Simple or Full)', choices=['Simple','Full'], default='Simple')
    
    args = parser.parse_args()

    # 学習データの読み込み
    output = f'result_teacher/{args.mode}/'
    data, label, feature_names, label_names, annotation = utils.readCSV(f'./data', args.mode, unu_flag=False)
    print(data.shape)
    
    tree = UsingTree()
    tree.fit(data, label, label_names, annotation)

    gv.GraphViz_teacher(tree, feature_names, label_names, f'{output}/tree')