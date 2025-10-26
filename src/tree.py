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
            return self.searce(node.left, data_str)
        else:
            return self.search(node.right, data_str)
        
    def search_by_name(self, node, name):
        if node is None or node.player == name:
            return node
        if name < node.player:
            return self.searce(node.left, name)
        else:
            return self.search(node.right, name)
    
    def DFS(self):
        '''need to implament'''

    def BFS(self):
        '''need to implament'''

# x = Tree_node("1,Jonathan Taylor,IND,RB,26,7,7,0,0,0,0,0,131,697,5.32,10,25,23,185,8.04,1,0,0,11,1,,156,179.2,185.2,167.7,92,1,1")

# print(x.fanduel_points)
