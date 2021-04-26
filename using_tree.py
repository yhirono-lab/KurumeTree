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
    def __init__(self, max_depth=None):
        print('max_depth', max_depth)
        self.root = None
        self.max_depth = max_depth
        self.root_analysis = TreeAnalysis()

    def fit(self, data, label, label_names, annotation):
        print(f'predict_data:{data.shape}/disease:{label_names.shape}')

        node_id = np.zeros(1)
        self.root = Node(self.max_depth)
        self.leaf_num = self.root.split_node(sample=data, target=label, depth=0, node_id=node_id, leaf_num=0, annotation=annotation)
        
        feature_importances = self.root_analysis.get_feature_importances(self.root, data.shape[1])
        self.feature_importances = {}
        for idx, value in enumerate(feature_importances):
            self.feature_importances[feature_names[idx]] = value
        
        self.leaf_hist = self.root_analysis.get_leaf_probability(self.root, self.leaf_num, label_names)
        self.predict(data, label, label_names)

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

    def get_feature_importances(self, node, num_features, normalize=True):
        self.importances = np.zeros(num_features)

        self.compute_feature_importances(node)
        self.importances /=  node.num_samples

        if normalize:
            normalizer = np.sum(self.importances)
            if normalizer > 0.0:
                self.importances /= normalizer

        return self.importances
    
    def compute_feature_importances(self, node):
        if node.leaf_id is not None:
            return

        self.importances[node.feature] += node.info_gain * node.num_samples

        self.compute_feature_importances(node.left)
        self.compute_feature_importances(node.right)

    def get_leaf_probability(self, node, leaf_num, label_names):
        self.probabilities = np.zeros((leaf_num, len(label_names)))
        self.search_leaf(node)
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
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
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
        
        # 設定した深さになったら終了
        if depth == self.max_depth:
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
        self.left = Node(self.max_depth)
        leaf_num = self.left.split_node(sample_l, target_l, depth+1, node_id, leaf_num, annotation_l)

        sample_r = sample[sample[:, self.feature] == 1]
        target_r = target[sample[:, self.feature] == 1]
        annotation_r = annotation[sample[:, self.feature] == 1]
        self.right = Node(self.max_depth)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use/not use による決定木の作成')
    parser.add_argument('--mode', help='choose disease name mode (Simple or Full)', choices=['Simple','Full'], default='Simple')
    parser.add_argument('--depth', help='input tree depth', default=3, type=int)
    args = parser.parse_args()

    # 学習データの読み込み
    output = f'result/{args.mode}/'
    data, label, feature_names, label_names, annotation = utils.readCSV(f'./data', args.mode)
    max_depth = args.depth
            
    for depth in np.array(range(max_depth))+1:
        
        tree = UsingTree(max_depth=depth)
        tree.fit(data, label, label_names, annotation)
        
        outputdir = f'{output}/unu_depth{depth}'
        utils.makeCSV2(tree.pred, outputdir, 'Ptable_unu.csv')
        utils.makeCSV2(tree.leaf_hist, outputdir, 'hist_unu.csv')
        utils.makeCSV2(tree.leaf_data, outputdir, 'leaf_list_unu.csv')
        utils.makeCSV2(list(tree.feature_importances.items()), outputdir, 'feature_importance.csv')
 
        gv.GraphViz(tree, feature_names, depth, f'{output}/tree', label_names)
