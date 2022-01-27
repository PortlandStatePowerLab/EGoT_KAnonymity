from treelib import Node, Tree
import numpy as np
import pandas as pd


class Dist:
    def __init__(self,root_name='substation',max_size=100000):
        # generate new tree
        self.tree = Tree()
        self.id = 0 # will be increment counter that used for ids
        # create root feeder
        root_id = f'{root_name}{self.id}'
        self.tree.create_node(root_name,root_id)
        self.current_lvl = [root_id]
        self.max_cap = max_size
        self.current_cap = 0
        self.lvl_names = [root_name]
        self.leaves = 0
        pass
    def __repr__(self):
        # prints the tree
        self.tree.show()
        return '-'*50
    def add_level(self,lvl_name,k=1,leave=False,lvls=None,id_range=None):
        '''
            Add a level to the current level of the tree. 
            It randomly picks which node to 
            lvl_name: name used to prefix the level
            k: number of instances to generate
        '''
        lvl = []
        current_lvl = self.current_lvl.copy() if lvls==None else lvls
        # print('current level: ',current_lvl)
        r = list(range(k)) if id_range == None else id_range
        if not lvl_name.lower() in self.lvl_names:
            self.lvl_names.append(lvl_name.lower())
        for parent in current_lvl:
            for i in r:
                if leave:
                    name = f'{parent}-{lvl_name}{self.leaves}'
                    self.leaves += 1
                else:
                    name = f'{parent}-{lvl_name}{i}' #if not leave else f'{parent}-{lvl_name}{self.leave}'
                # randomly pick which node to add the new node to
                # parent = np.random.choice(current_lvl)
                # parent = current_lvl
                self.tree.create_node(name,name,parent)
                lvl.append(name)
                self.current_cap += 1
                assert self.current_cap <= self.max_cap, 'Exceeding max number of nodes threshold'
        # use the newly added lvl as the current lvl
        # old_lvl = self.current_lvl
        self.current_lvl = lvl
        return (True,lvl)
    def add_level_rand(self,lvl_name,k=1,leave=False,id_range=None):
        '''
            Add a level to the current level of the tree. 
            It randomly picks which node to 
            lvl_name: name used to prefix the level
            k: number of instances to generate
        '''
        lvl = []
        current_lvl = self.current_lvl.copy() 
        # print('current level: ',current_lvl)
        if not lvl_name.lower() in self.lvl_names:
            self.lvl_names.append(lvl_name.lower())
        for i in range(k):
            # randomly pick which node to add the new node to
            parent = np.random.choice(current_lvl)
            if len(current_lvl) > 1:
                current_lvl.remove(parent)
            if leave:
                name = f'{parent}-{lvl_name}{self.leaves}'
                self.leaves += 1
            else:
                name = f'{parent}-{lvl_name}{i}' #if not leave else f'{parent}-{lvl_name}{self.leave}'
            self.tree.create_node(name,name,parent)
            lvl.append(name)
            self.current_cap += 1
            assert self.current_cap <= self.max_cap, 'Exceeding max number of nodes threshold'
        self.current_lvl = lvl
        return (True,lvl)
    def drop_childless(self):
        '''
            Cleans the tree from unused paths (balances the tree so that all leaves on the same level).
            It also renumbers the remaining levels.
        '''
        # self.tree = self.tree.filter_nodes(lambda x: x.is)
        pass
    def export_to_df(self):
        '''
            Performs depth first traversal to get the a representation of the tree.
            It exports the rep. tree into a df with given headers.
            * Headers: desired header names (must be equal to the tree depth)
            NOTE: It drops anything that isn't on the same level (i.e. only the balanced parts )
        '''
        # assert len(headers) == self.tree.depth, 'Incompatible '
        depth = self.tree.depth() + 1 # including the root
        tree = self.tree.paths_to_leaves()
        tree = list(filter(lambda x: len(x) == depth,tree))
        df = pd.DataFrame(tree,columns = self.lvl_names)
        return df
    def drop_subtrees(self,trees):
        '''
            drops the subtrees given in the args
        '''
        for i in trees:
            for c in self.tree.get_node(i).children():
                self.tree.remove_subtree()
        return True