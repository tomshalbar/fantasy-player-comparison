from collections import deque

class Tree_node:
    labels = "rk,player,tm,fantpos,age,games,games_started,passes_completed,pass_attempts,passing_yds,passing_td,passes_intercepted,rushing_att,rushing_yds,yds_rushing_att,rushing_td,targets,receptions,receiving_yds,yds_reception,receiving_td,fumbles,fumbles_lost,touchdowns,2_pt_conv_made,2_pt_conv_passes,fantasy_points,fantasy_points_ppr_,draftkings_points,fanduel_points,vbd,posrank,ovrank".split(",")

    def __init__(self, data_str):
        '''create a tree_node based on the attribute'''
        self.left = None
        self.right = None
        
        attribs = data_str.split(",")
        for i, label in enumerate(self.labels):
            setattr(self, label, attribs[i])

class Tree:
    
    def __init__(self):
        self.root = None

    def insert(self, node, data_str):
        if self.root is None:
            self.root = Tree_node(data_str)
        else:
            name = data_str.split(",", 1)[0]
            if node.player > name:
                if node.left == None:
                    node.left = Tree_node(data_str)
                else:
                    self.insert(node.left, data_str)
            else:
                if node.right == None:
                    node.right = Tree_node(data_str)
                else:
                    self.insert(node.right, data_str)
    
    def search(self, node, data_str):
        name = data_str.split(",", 1)[0]
        if node is None or node.player == name:
            return node
        if name < node.player:
            return self.search(node.left, data_str)
        else:
            return self.search(node.right, data_str)
        
    def search_by_name(self, node, name):
        if node is None or node.player == name:
            return node
        if name < node.player:
            return self.search(node.left, name)
        else:
            return self.search(node.right, name)
    
    def inorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node)
            self.inorder(node.right, result)
        return result

    def preorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            result.append(node)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def postorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node)
        return result

    def DFS(self, traversal_type='inorder'):
        """
        Perform DFS traversal of the tree
        Parameters: traversal_type: 'inorder', 'preorder', or 'postorder'
        Returns: List of Tree_node objects in the specified DFS order
        """
        if traversal_type == 'inorder':
            return self.inorder(self.root)
        elif traversal_type == 'preorder':
            return self.preorder(self.root)
        elif traversal_type == 'postorder':
            return self.postorder(self.root)

    def BFS(self):
        """
        Perform BFS traversal of the tree using a queue
        Returns: List of Tree_node objects in BFS order
        """
        if not self.root:
            return []
            
        result = []
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        return result

# x = Tree_node("1,Jonathan Taylor,IND,RB,26,7,7,0,0,0,0,0,131,697,5.32,10,25,23,185,8.04,1,0,0,11,1,,156,179.2,185.2,167.7,92,1,1")

# print(x.fanduel_points)
