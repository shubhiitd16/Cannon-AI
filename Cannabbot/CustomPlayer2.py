#!/usr/bin/env python
# coding: utf-8

# ## Kumar Shubham
# ### AI Assignment- Version 5

# In[ ]:


import random
import sys
import time
import json
import copy


# In[2]:


def all_canons(state,x,y):
    assert state[x][y]!=0
    out=[]
    bool1,bool2,bool3,bool4,bool5,bool6,bool7,bool8,bool9,bool10,bool11,bool12,bool13,bool14,bool15,bool16=False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
    if(x>1): bool1=state[x-2][y]==state[x][y]
    if(x>0): bool2=state[x-1][y]==state[x][y]
    if(x<7): bool3=state[x+1][y]==state[x][y]
    if(x<6): bool4=state[x+2][y]==state[x][y]
    if(y>1): bool5=state[x][y-2]==state[x][y]
    if(y>0): bool6=state[x][y-1]==state[x][y]
    if(y<7): bool7=state[x][y+1]==state[x][y]
    if(y<6): bool8=state[x][y+2]==state[x][y]
    if(y>1 and x>1): bool9=state[x-2][y-2]==state[x][y]
    if(y>0 and x>0): bool10=state[x-1][y-1]==state[x][y]
    if(y<7 and x<7): bool11=state[x+1][y+1]==state[x][y]
    if(y<6 and x<6): bool12=state[x+2][y+2]==state[x][y]   
    if(y<6 and x>0): bool13=state[x-2][y+2]==state[x][y]
    if(y<7 and x>1): bool14=state[x-1][y+1]==state[x][y]
    if(y>0 and x<7): bool15=state[x+1][y-1]==state[x][y]
    if(y>1 and x<6): bool16=state[x+2][y-2]==state[x][y]
    if (bool1 and bool2): out.append([(x-2,y),(x-1,y),(x,y)])
    if (bool2 and bool3): out.append([(x-1,y),(x,y),(x+1,y)])
    if (bool3 and bool4): out.append([(x,y),(x+1,y),(x+2,y)])
    if (bool5 and bool6): out.append([(x,y-2),(x,y-1),(x,y)])
    if (bool6 and bool7): out.append([(x,y-1),(x,y),(x,y+1)])
    if (bool7 and bool8): out.append([(x,y),(x,y+1),(x,y+2)])
    if (bool9 and bool10): out.append([(x-2,y-2),(x-1,y-1),(x,y)])
    if (bool10 and bool11): out.append([(x-1,y-1),(x,y),(x+1,y+1)])
    if (bool11 and bool12): out.append([(x,y),(x+1,y+1),(x+2,y+2)])
    if (bool13 and bool14): out.append([(x-2,y+2),(x-1,y+1),(x,y)])
    if (bool14 and bool15): out.append([(x-1,y+1),(x,y),(x+1,y-1)])
    if (bool15 and bool16): out.append([(x,y),(x+1,y-1),(x+2,y-2)])
    return out


# In[3]:


class canon:
    def __init__(self,head,centre,tail,state):
        assert head.player_id==tail.player_id and state[int((head.x+tail.x)/2)][int((head.y+tail.y)/2)]==head.player_id
        assert abs(head.y-tail.y)==2 or abs(head.x-tail.x)==2
        self.player_id=head.player_id
        self.head=head
        head.canon.append(self)
        self.centre=centre
        centre.canon.append(self)
        self.tail=tail
        tail.canon.append(self)
        self.direction=(self.head.x-self.centre.x,self.head.y-self.centre.y)
        self.canon_shots(state)
        move_x,move_y=self.head.x+self.direction[0],self.head.y+self.direction[1]
        #print(move_x,move_y)
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.forward=True
        else: self.forward=False
        move_x,move_y=self.tail.x-self.direction[0],self.tail.y-self.direction[1]
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.backward=True
        else: self.backward=False
        
    def update(self,state):
        self.direction=(self.head.x-self.centre.x,self.head.y-self.centre.y)
        self.canon_shots(state)
        move_x,move_y=self.head.x+self.direction[0],self.head.y+self.direction[1]
        #print(move_x,move_y)
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.forward=True
        else: self.forward=False
        move_x,move_y=self.tail.x-self.direction[0],self.tail.y-self.direction[1]
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.backward=True
        else: self.backward=False
            
    def canon_shots(self,state):
        attack_pos=[]
        try:
            if(state[self.head.x+self.direction[0]][self.head.y+self.direction[1]]==0):
                attack_pos.append((self.head.x+2*self.direction[0],self.head.y+2*self.direction[1]))
                if(state[self.head.x+2*self.direction[0]][self.head.y+2*self.direction[1]]==0):
                    attack_pos.append((self.head.x+3*self.direction[0],self.head.y+3*self.direction[1]))
        except:
            pass

        try:
            if(state[self.tail.x-self.direction[0]][self.tail.y-self.direction[1]]==0):
                attack_pos.append((self.tail.x-2*self.direction[0],self.tail.y-2*self.direction[1]))
                if(state[self.tail.x-2*self.direction[0]][self.tail.y-2*self.direction[1]]==0):
                    attack_pos.append((self.tail.x-3*self.direction[0],self.tail.y-3*self.direction[1]))
        except:
            pass
            
        
        self.blank_moves=list(filter(lambda x: x[0]>=0 and x[1]>=0 and x[0]<8 and x[1]<8 and state[x[0]][x[1]]==0,attack_pos))
        self.bombs=list(filter(lambda x: x[0]>=0 and x[1]>=0 and x[0]<8 and x[1]<8 and state[x[0]][x[1]]!=self.player_id and state[x[0]][x[1]]!=0,attack_pos))
    
    
    def forward_move(self,state):
        assert self.forward
        from_x,from_y=self.tail.x,self.tail.y
        state[self.tail.x][self.tail.y]=0
        self.head,self.centre,self.tail=self.tail,self.head,self.centre
        self.head.x,self.head.y=self.centre.x+self.direction[0],self.centre.y+self.direction[1]
        state[self.head.x][self.head.y]=self.player_id
        move_x,move_y=self.head.x+self.direction[0],self.head.y+self.direction[1]
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.forward=True
        else: self.forward=False
        self.backward=True
        self.canon_shots(state)
        return self.head.x,self.head.y,from_x,from_y,state
        
    def backward_move(self,state): 
        assert self.backward
        from_x,from_y=self.head.x,self.head.y
        state[self.head.x][self.head.y]=0
        self.head,self.centre,self.tail=self.centre,self.tail,self.head
        self.tail.x,self.tail.y=self.centre.x-self.direction[0],self.centre.y-self.direction[1]
        state[self.tail.x][self.tail.y]=self.player_id
        move_x,move_y=self.tail.x-self.direction[0],self.tail.y-self.direction[1]
        if move_x>=0 and move_y>=0 and move_x<8 and move_y<8 and state[move_x][move_y]==0: self.backward=True
        else: self.backward=False
        self.forward=True
        self.canon_shots(state)
        return self.tail.x,self.tail.y,from_x,from_y,state


# In[4]:



class soldier:
    def __init__(self,x,y,player_id,opponent_id,game):
        self.x=x
        self.y=y
        self.canon=[]
        self.player_id=player_id
        self.opponent_id=opponent_id
        self.danger=self.in_danger(game)
        self.allowed_movements(game)
        self.priority=None
        
    def allowed_movements(self,game):
        moves=[(self.x-1,self.y),(self.x+1,self.y),(self.x-1,self.y+self.player_id),(self.x,self.y+self.player_id),(self.x+1,self.y+self.player_id)]
        out=[]
        if self.danger:
            moves+=[(self.x-2,self.y-2*player_id),(self.x,self.y-2*player_id),(self.x+2,self.y-2*player_id)]
        #print(moves)
        for x,y in moves:
            if(x>=0 and y>=0 and x<8 and y<8):
                if game[x][y]==self.opponent_id:
                    out.append(['M',x,y])
                elif game[x][y]==0 and self.y!=y:
                    out.append(['M',x,y])
                elif self.player_id==1 and (x,y) in [(1, 7), (3, 7), (5, 7), (7, 7)]:
                    out.append(['M',x,y])
                elif self.player_id==-1 and (x,y) in [(0, 0), (2, 0), (4, 0), (6, 0)]:
                    out.append(['M',x,y])
         
        self.moves=out
        
    def in_danger(self,game): # Is Adjacent to an Enemy?
        adjacent=[(self.x-1,self.y-self.opponent_id),(self.x,self.y-self.opponent_id),(self.x+1,self.y-self.opponent_id),(self.x-1,self.y),(self.x+1,self.y)]
        #print(self.x,self.y,self.player_id,adjacent)
        danger=any(x>=0 and y>=0 and x<8 and y<8 and game[x][y]==self.opponent_id for x,y in adjacent)
        return danger
    
    def move(self,state,move_x,move_y):
        #display(state)
        #print(self.x,self.y,move_x,move_y)
        #print("Pl",self.player_id)
        state[self.x][self.y]=0
        state[move_x][move_y]=self.player_id
        #display(state)
        #self.x,self.y=move_x,move_y
        return state
    
    def evaluate(self):  #Evaluate Priority of selection for soldier moves
        if(self.priority!=None): return self.priority
        if self.player_id==1: priority=-1*(3**(self.y))*(1-self.danger)  #Distance from townhall
        else: priority=-1*(3**(7-self.y) )*(1-self.danger)     
        if(len(self.canon)>0): priority-=5
        if self.danger: priority+=500
        self.priority=priority
        return priority
    


# In[5]:


def start_game(player_id,opponent_id,n,m):
    start_state=[[1 if(i%2==1 and j<3) else -1 if (i%2==0 and j>4) else 0 for j in range(m)] for i in range(n)]
    Townhalls1=[(x,7) for x in range(1,8,2)]
    Townhalls2=[(x,0) for x in range(0,8,2)]
    if player_id==-1: turn=1 
    else: turn=0; Townhalls1,Townhalls2=Townhalls2,Townhalls1
    #To optimise
    self={'townhall':Townhalls1,
          'soldiers':[soldier(i,j,player_id,opponent_id,start_state) for j in range(m) for i in range(n) if start_state[i][j]==player_id]}
    self['canons']=[canon(self['soldiers'][k], self['soldiers'][4+k], self['soldiers'][8+k], start_state) for k in range(4)]
    
    opponent={'townhall':Townhalls2,
          'soldiers':[soldier(i,j,opponent_id,player_id,start_state) for j in range(m) for i in range(n) if start_state[i][j]==opponent_id]}
    opponent['canons']=[canon(opponent['soldiers'][k], opponent['soldiers'][4+k], opponent['soldiers'][8+k], start_state) for k in range(4)]
    
    return start_state,self,opponent,turn
    
    


# In[7]:


import math
class Game:
    def __init__(self,board,self_team,opponent_team,turn): #1-Your Turn 0-opponent's turn
        self.state=board
        self.turn=turn
        self.self_team=self_team
        self.turn_soldier=self_team['soldiers'][0].player_id
        if(self.turn==1):
            self.self_team['soldiers']=sorted(self.self_team['soldiers'],key=lambda x:x.evaluate(),reverse=True)
        self.opponent_team=opponent_team
        if(self.turn==0):
            self.opponent_team['soldiers']=sorted(self.opponent_team['soldiers'],key=lambda x:x.evaluate(),reverse=True)
        self.children=self.get_child()
        self.all_children=None
        self.solution=None
        self.scores=None
        self.order_after_move()
        self.hash={}
    
    def constraint_check(self):
        self_id=self.turn_soldier
        assert len(self.self_team['soldiers'])==sum(map(lambda x:x.count(self_id),self.state))
        for sol in self.self_team['soldiers']:
            #print(sol.x,sol.y,self.state[sol.x][sol.y],self_id)
            assert self.state[sol.x][sol.y]==self_id
        for sol in self.opponent_team['soldiers']:
            assert self.state[sol.x][sol.y]==-1*self_id
            
        
    def canon_bomb(self):
        if(self.turn==1):
            for i,canons in enumerate(self.self_team['canons']):
                    for attack_x,attack_y in canons.bombs:
                        ##print("step",1) 
                        new_state=copy.deepcopy(self.state)
                        new_state[attack_x][attack_y]=0
                        new_self={'townhall':self.self_team['townhall'],

                                  'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                                  if (abs(player.x-attack_x)<2 and abs(player.y-attack_y)<2)
                                  else player
                                  for j,player in enumerate(self.self_team['soldiers'])],

                                  'canons':self.self_team['canons']
                                 }
                        new_opponent={'townhall':self.opponent_team['townhall'],

                                  'soldiers':[player
                                  for j,player in enumerate(self.opponent_team['soldiers']) 
                                  if(attack_x,attack_y)!=(player.x,player.y)],

                                  'canons':list(filter(lambda x:(attack_x,attack_y)!=(x.head.x,x.head.y) 
                                                       and (attack_x,attack_y)!=(x.tail.x,x.tail.y)
                                                       and (attack_x,attack_y)!=(x.centre.x,x.centre.y),
                                                       copy.deepcopy(self.opponent_team['canons'])))
                                 }
                        self.opponent_team['townhall']=[th for th in self.opponent_team['townhall'] if (attack_x,attack_y)!=th]
                        yield ('S',canons.head.x,canons.head.y,'B',attack_x,attack_y,new_state,new_self,new_opponent,1-self.turn)
        else:
            for i,canons in enumerate(self.opponent_team['canons']):
                for attack_x,attack_y in canons.bombs:
                    new_state=copy.deepcopy(self.state)
                    new_state[attack_x][attack_y]=0
                    new_opponent={'townhall':self.opponent_team['townhall'],

                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-attack_x)<2 and abs(player.y-attack_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers'])],

                              'canons':self.opponent_team['canons']
                             }
                    new_self={'townhall':self.self_team['townhall'],

                              'soldiers':[player
                              for j,player in enumerate(self.self_team['soldiers']) 
                              if(attack_x,attack_y)!=(player.x,player.y)],

                              'canons':list(filter(lambda x:(attack_x,attack_y)!=(x.head.x,x.head.y) 
                                                   and (attack_x,attack_y)!=(x.tail.x,x.tail.y)
                                                   and (attack_x,attack_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    self.self_team['townhall']=[th for th in self.self_team['townhall'] if (attack_x,attack_y)!=th]
                    yield ('S',canons.head.x,canons.head.y,'B',attack_x,attack_y,new_state,new_self,new_opponent,1-self.turn)
    def get_child(self):
        if(self.turn==1):
            for i,canons in enumerate(self.self_team['canons']):
                for attack_x,attack_y in canons.bombs:
                    #print("step",1) 
                    new_state=copy.deepcopy(self.state)
                    new_state[attack_x][attack_y]=0
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-attack_x)<2 and abs(player.y-attack_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers'])],
                              
                              'canons':self.self_team['canons']
                             }
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[player
                              for j,player in enumerate(self.opponent_team['soldiers']) 
                              if(attack_x,attack_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(attack_x,attack_y)!=(x.head.x,x.head.y) 
                                                   and (attack_x,attack_y)!=(x.tail.x,x.tail.y)
                                                   and (attack_x,attack_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
                    self.opponent_team['townhall']=[th for th in self.opponent_team['townhall'] if (attack_x,attack_y)!=th]
                    yield ('S',canons.head.x,canons.head.y,'B',attack_x,attack_y,new_state,new_self,new_opponent,1-self.turn)
                    
            ##print("step",1,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))        
                    
                    
            for i,canons in enumerate(self.self_team['canons']):
                new_state=copy.deepcopy(self.state)
                new_canon=copy.deepcopy(canons)
                
                if new_canon.forward: 
                    ##print("step",2) 
                    to_x,to_y,from_x,from_y,new_state=new_canon.forward_move(new_state)
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(to_x,to_y,player.player_id,player.opponent_id,new_state) 
                                          if player.x==from_x and player.y==from_y
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(from_x,from_y)!=(x.head.x,x.head.y) 
                                                   and (from_x,from_y)!=(x.tail.x,x.tail.y)
                                                   and (from_x,from_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
        

                    for list_canons in all_canons(new_state,to_x,to_y):
               
                        head,centre,tail=list_canons
                        for sol in new_self['soldiers']:
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        assert head.x+tail.x==2*centre.x
                        new_self['canons'].append(canon(head,centre,tail,new_state))
                        
                         
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers']) 
                              if(to_x,to_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(to_x,to_y)!=(x.head.x,x.head.y) 
                                                   and (to_x,to_y)!=(x.tail.x,x.tail.y)
                                                   and (to_x,to_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
                    for c in new_opponent['canons']:c.update(new_state)
                    yield ('S',from_x,from_y,'M',to_x,to_y,new_state,new_self,new_opponent,1-self.turn)
                
                #print("step",2,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
                new_state=copy.deepcopy(self.state)
                new_canon=copy.deepcopy(canons)
                    
                if new_canon.backward: 
                    #print("step",3) 
                    to_x,to_y,from_x,from_y,new_state=new_canon.backward_move(new_state)
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(to_x,to_y,player.player_id,player.opponent_id,new_state) 
                                          if player.x==from_x and player.y==from_y
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(from_x,from_y)!=(x.head.x,x.head.y) 
                                                   and (from_x,from_y)!=(x.tail.x,x.tail.y)
                                                   and (from_x,from_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
        

                    for list_canons in all_canons(new_state,to_x,to_y):
               
                        head,centre,tail=list_canons
                        for sol in new_self['soldiers']:
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        assert head.x+tail.x==2*centre.x
                        new_self['canons'].append(canon(head,centre,tail,new_state))
                        
                         
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers']) 
                              if(to_x,to_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(to_x,to_y)!=(x.head.x,x.head.y) 
                                                   and (to_x,to_y)!=(x.tail.x,x.tail.y)
                                                   and (to_x,to_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
                    for c in new_opponent['canons']:c.update(new_state)
                    yield ('S',from_x,from_y,'M',to_x,to_y,new_state,new_self,new_opponent,1-self.turn)
                        
                    
            #print("step",3,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))          
                    
            
       
            for i,soldiers in enumerate(self.self_team['soldiers']):
     
                for _,move_x,move_y in soldiers.moves:
                    for sol in self.self_team['soldiers']:
                        #print(sol.x,sol.y,sol.player_id)
                        #sol.display_contents()
                        assert self.state[sol.x][sol.y]==sol.player_id
                    #print("step",4,"to",move_x,move_y,"from",soldiers.x,soldiers.y) 
                    #print("opp",soldiers.player_id)
                    #display(new_state)
                    new_state=soldiers.move(copy.deepcopy(self.state),move_x,move_y)
                    #print("after return")
                    #display(new_state)
                    #print((move_x,move_y,soldiers.x,soldiers.y))
                    new_self={'townhall':self.self_team['townhall'],
                              'soldiers':[soldier(move_x,move_y,player.player_id,player.opponent_id,new_state) if i==j
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                              or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(soldiers.x,soldiers.y)!=(x.head.x,x.head.y) 
                                                   and (soldiers.x,soldiers.y)!=(x.tail.x,x.tail.y)
                                                   and (soldiers.x,soldiers.y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    
                    
                    for sol in new_self['soldiers']:
                        #print(sol.x,sol.y,sol.player_id)
                        #sol.display_contents()
                        assert new_state[sol.x][sol.y]==sol.player_id
                    for list_canons in all_canons(new_state,move_x,move_y):
                        ##print("move_x",move_x,"move_y",move_y,list_canons)
                        head,centre,tail=list_canons
                        for sol in new_self['soldiers']:
                            #print(sol.x,sol.y)
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        try:
                            assert head.x+tail.x==2*centre.x
                        except:
                            #print("error",len(new_self['canons']))
                            #print(head,centre,tail,move_x,move_y)
                            #for sol1 in new_self['soldiers']:
                                #print(sol1.x,sol1.y,sol1.moves,sol1.evaluate(),len(sol1.canon))
                            #display(new_state)
                            assert 1==2
                        new_self['canons'].append(canon(head,centre,tail,new_state))
                        
                    #print(99)    
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                              or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers']) 
                              if(move_x,move_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(move_x,move_y)!=(x.head.x,x.head.y) 
                                                   and (move_x,move_y)!=(x.tail.x,x.tail.y)
                                                   and (move_x,move_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
                    
                    for c in new_opponent['canons']:c.update(new_state)
                    self.opponent_team['townhall']=[th for th in self.opponent_team['townhall'] if (move_x,move_y)!=th]
                    yield ('S',soldiers.x,soldiers.y,'M',move_x,move_y,new_state,new_self,new_opponent,1-self.turn)
                    
        else:
            #print(109)
            for i,canons in enumerate(self.opponent_team['canons']):
                for attack_x,attack_y in canons.bombs:
                    new_state=copy.deepcopy(self.state)
                    new_state[attack_x][attack_y]=0
                    new_opponent={'townhall':self.opponent_team['townhall'],

                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-attack_x)<2 and abs(player.y-attack_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers'])],

                              'canons':self.opponent_team['canons']
                             }
                    new_self={'townhall':self.self_team['townhall'],

                              'soldiers':[player
                              for j,player in enumerate(self.self_team['soldiers']) 
                              if(attack_x,attack_y)!=(player.x,player.y)],

                              'canons':list(filter(lambda x:(attack_x,attack_y)!=(x.head.x,x.head.y) 
                                                   and (attack_x,attack_y)!=(x.tail.x,x.tail.y)
                                                   and (attack_x,attack_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    self.self_team['townhall']=[th for th in self.self_team['townhall'] if (attack_x,attack_y)!=th]
                    yield ('S',canons.head.x,canons.head.y,'B',attack_x,attack_y,new_state,new_self,new_opponent,1-self.turn)
            
            #print("step",5,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
            for i,canons in enumerate(self.opponent_team['canons']):
                new_state=copy.deepcopy(self.state)
                new_canon=copy.deepcopy(canons)
                
                if new_canon.forward: 
                    to_x,to_y,from_x,from_y,new_state=new_canon.forward_move(new_state)
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(to_x,to_y,player.player_id,player.opponent_id,new_state) 
                                          if player.x==from_x and player.y==from_y
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(from_x,from_y)!=(x.head.x,x.head.y) 
                                                   and (from_x,from_y)!=(x.tail.x,x.tail.y)
                                                   and (from_x,from_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
        

                    for list_canons in all_canons(new_state,to_x,to_y):
               
                        head,centre,tail=list_canons
                        for sol in new_opponent['soldiers']:
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        assert head.x+tail.x==2*centre.x
                        new_opponent['canons'].append(canon(head,centre,tail,new_state))
                        
                         
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers']) 
                              if(to_x,to_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(to_x,to_y)!=(x.head.x,x.head.y) 
                                                   and (to_x,to_y)!=(x.tail.x,x.tail.y)
                                                   and (to_x,to_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    for c in new_self['canons']:c.update(new_state)
                    yield ('S',from_x,from_y,'M',to_x,to_y,new_state,new_self,new_opponent,1-self.turn)
                #print("step",6,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))      
                new_state=copy.deepcopy(self.state)
                new_canon=copy.deepcopy(canons)
                   
                if new_canon.backward: 
                    to_x,to_y,from_x,from_y,new_state=new_canon.backward_move(new_state)
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(to_x,to_y,player.player_id,player.opponent_id,new_state) 
                                          if player.x==from_x and player.y==from_y
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(from_x,from_y)!=(x.head.x,x.head.y) 
                                                   and (from_x,from_y)!=(x.tail.x,x.tail.y)
                                                   and (from_x,from_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
        

                    for list_canons in all_canons(new_state,to_x,to_y):
               
                        head,centre,tail=list_canons
                        for sol in new_opponent['soldiers']:
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        assert head.x+tail.x==2*centre.x
                        new_opponent['canons'].append(canon(head,centre,tail,new_state))
                        
                         
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-from_x)<2 and abs(player.y-from_y)<2) 
                              or (abs(player.x-to_x)<2 and abs(player.y-to_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers']) 
                              if(to_x,to_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(to_x,to_y)!=(x.head.x,x.head.y) 
                                                   and (to_x,to_y)!=(x.tail.x,x.tail.y)
                                                   and (to_x,to_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    for c in new_self['canons']:c.update(new_state)
                    #print("jj",'S',from_x,from_y,'M',to_x,to_y,new_self,new_opponent,1-self.turn)
                    #display(new_state)
                    #print()
                    yield ('S',from_x,from_y,'M',to_x,to_y,new_state,new_self,new_opponent,1-self.turn)
            
            


            for i,soldiers in enumerate(self.opponent_team['soldiers']):
       
                for _,move_x,move_y in soldiers.moves:
                    ##print("soldier",i,move_x,move_y)
                    new_state=soldiers.move(copy.deepcopy(self.state),move_x,move_y)
                    new_opponent={'townhall':self.opponent_team['townhall'],
                              
                              'soldiers':[soldier(move_x,move_y,player.player_id,player.opponent_id,new_state) if i==j
                              else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                              or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                              else player
                              for j,player in enumerate(self.opponent_team['soldiers'])],
                              
                              'canons':list(filter(lambda x:(soldiers.x,soldiers.y)!=(x.head.x,x.head.y) 
                                                   and (soldiers.x,soldiers.y)!=(x.tail.x,x.tail.y)
                                                   and (soldiers.x,soldiers.y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.opponent_team['canons'])))
                             }
                    #print("step",8,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
                    for list_canons in all_canons(new_state,move_x,move_y):
                        head,centre,tail=list_canons
                        for sol in new_opponent['soldiers']:
                            if (sol.x,sol.y)==head:head=sol
                            elif (sol.x,sol.y)==centre:centre=sol
                            elif (sol.x,sol.y)==tail:tail=sol
                        assert head.x+tail.x==2*centre.x
                        new_opponent['canons'].append(canon(head,centre,tail,new_state))
                    #print("step",9,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons'])))) 
                    new_self={'townhall':self.self_team['townhall'],
                              
                              'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                              if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                              or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                              else player
                              for j,player in enumerate(self.self_team['soldiers']) 
                              if(move_x,move_y)!=(player.x,player.y)],
                              
                              'canons':list(filter(lambda x:(move_x,move_y)!=(x.head.x,x.head.y) 
                                                   and (move_x,move_y)!=(x.tail.x,x.tail.y)
                                                   and (move_x,move_y)!=(x.centre.x,x.centre.y),
                                                   copy.deepcopy(self.self_team['canons'])))
                             }
                    #print("step",10,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
                    for c in new_self['canons']:c.update(new_state)
                    #print("step",11,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons'])))) 
                    self.self_team['townhall']=[th for th in self.self_team['townhall'] if (move_x,move_y)!=th]
                    yield ('S',soldiers.x,soldiers.y,'M',move_x,move_y,new_state,new_self,new_opponent,1-self.turn)
    def display_all_children(self):
        try:
            child=0
            while(1):
                A1,from_x,from_y,A2,to_x,to_y,new_state,new_self,new_opponent,turn=next(self.children)
                print("Child: ",child,"Count of self soldiers:",len(new_self['soldiers']),"Count of opponent soldiers:",len(new_opponent['soldiers']),
                     "\nCount of self canons:",len(new_self['canons']),"Count of Opponent canons:",len(new_opponent['canons']))
                child+=1
                #display(new_state)
        except StopIteration :
            #print("All children states has been displayed")
            self.children=self.get_child()
            
    def execute_move_opponent(self,string):
        #Always Opponent
        #string="S 0 1 M 1 0"
        if(string in self.hash):
            return self.hash[string]
        else:
            actions=string.split(' ')
            assert actions[0]=='S'
        x,y=int(actions[1]),int(actions[2])
        if(actions[3]=='M'):
            move_x,move_y=int(actions[4]),int(actions[5])
            soldiers=list(filter(lambda sol:sol.x==x and sol.y==y,self.opponent_team['soldiers']))[0]
            new_state=soldiers.move(copy.deepcopy(self.state),move_x,move_y)
            new_opponent={'townhall':self.opponent_team['townhall'],

                      'soldiers':[soldier(move_x,move_y,player.player_id,player.opponent_id,new_state) 
                                  if player.x==x and player.y==y
                                  else soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                                  if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                                  or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                                  else player
                                  for j,player in enumerate(self.opponent_team['soldiers'])],

                                  'canons':list(filter(lambda x:(soldiers.x,soldiers.y)!=(x.head.x,x.head.y) 
                                                       and (soldiers.x,soldiers.y)!=(x.tail.x,x.tail.y)
                                                       and (soldiers.x,soldiers.y)!=(x.centre.x,x.centre.y),
                                                       copy.deepcopy(self.opponent_team['canons'])))
                                 }
            #print("step",8,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
            for list_canons in all_canons(new_state,move_x,move_y):
                head,centre,tail=list_canons
                for sol in new_opponent['soldiers']:
                    if (sol.x,sol.y)==head:head=sol
                    elif (sol.x,sol.y)==centre:centre=sol
                    elif (sol.x,sol.y)==tail:tail=sol
                assert head.x+tail.x==2*centre.x
                new_opponent['canons'].append(canon(head,centre,tail,new_state))
            #print("step",9,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons'])))) 
            new_self={'townhall':self.self_team['townhall'],

                      'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                      if (abs(player.x-soldiers.x)<2 and abs(player.y-soldiers.y)<2) 
                      or (abs(player.x-move_x)<2 and abs(player.y-move_y)<2)
                      else player
                      for j,player in enumerate(self.self_team['soldiers']) 
                      if(move_x,move_y)!=(player.x,player.y)],

                      'canons':list(filter(lambda x:(move_x,move_y)!=(x.head.x,x.head.y) 
                                           and (move_x,move_y)!=(x.tail.x,x.tail.y)
                                           and (move_x,move_y)!=(x.centre.x,x.centre.y),
                                           copy.deepcopy(self.self_team['canons'])))
                     }
            #print("step",10,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))  
            for c in new_self['canons']:c.update(new_state)
            #print("step",11,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons'])))) 
            self.self_team['townhall']=[th for th in self.self_team['townhall'] if (move_x,move_y)!=th]
            new_g=Game(new_state,new_self,new_opponent,1-self.turn)
            return new_g
        else:
            attack_x,attack_y=int(actions[4]),int(actions[5])
            new_state=copy.deepcopy(self.state)
            new_state[attack_x][attack_y]=0
            new_opponent={'townhall':self.opponent_team['townhall'],

                      'soldiers':[soldier(player.x,player.y,player.player_id,player.opponent_id,new_state)
                      if (abs(player.x-attack_x)<2 and abs(player.y-attack_y)<2)
                      else player
                      for j,player in enumerate(self.opponent_team['soldiers'])],

                      'canons':self.opponent_team['canons']
                     }
            new_self={'townhall':self.self_team['townhall'],

                      'soldiers':[player
                      for j,player in enumerate(self.self_team['soldiers']) 
                      if(attack_x,attack_y)!=(player.x,player.y)],

                      'canons':list(filter(lambda x:(attack_x,attack_y)!=(x.head.x,x.head.y) 
                                           and (attack_x,attack_y)!=(x.tail.x,x.tail.y)
                                           and (attack_x,attack_y)!=(x.centre.x,x.centre.y),
                                           copy.deepcopy(self.self_team['canons'])))
                     }
            self.self_team['townhall']=[th for th in self.self_team['townhall'] if (attack_x,attack_y)!=th]
            new_g=Game(new_state,new_self,new_opponent,1-self.turn)
            return new_g

        
    
                
        
    def grand_child(self,max_level):
        start=time.time()
        level=0
        count=0
        solution=[]
        stack=[self]
        moves=["Start Position"]
        while(stack or level==max_level):
                try:
                    assert level<=max_level
                    A1,from_x,from_y,A2,to_x,to_y,new_state,new_self,new_opponent,turn=next(stack[-1].children)
                    moves.append(" ".join([A1,str(from_x),str(from_y),A2,str(to_x),str(to_y)])+" (turn:{}) ".format(1-turn))
                    #if moves[-1] in self.solution: 
                        #stack.append(self.solution[moves[-1]])
                    #else:
                    stack.append(Game(new_state,new_self,new_opponent,turn))
                    level+=1

                except (StopIteration,AssertionError) as e:
                    if(level==max_level):
                        count+=1
                        #print("-> ".join(moves),"Reward Gain:{}".format(stack[-1].evaluate()))
                        solution.append([stack[-1].evaluate(),stack[-1],moves])
                        #display(stack[-1].state)
                    stack.pop()
                    moves.pop()
                    level-=1
        self.children=self.get_child()
        #print("Time taken",time.time()-start)
        return count
    
    def order_after_move(self): 
        #1,4,5,7,8
        #To add- Backtreat moves
        matrix=[[4 for j in range(8)] for i in range(8)]
        if self.turn==1: team,team1=self.opponent_team,self.self_team
        else: team,team1,id_=self.self_team,self.opponent_team,1
        for soldier in team['soldiers']:
            id_=soldier.player_id
            try:matrix[soldier.x-1][soldier.y+soldier.player_id]=1 #Danger
            except: pass
            try:matrix[soldier.x][soldier.y+soldier.player_id]=1
            except: pass
            try:matrix[soldier.x+1][soldier.y+soldier.player_id]=1
            except: pass
        #4-Neutral    
        for soldier in team['soldiers']:
            if len(soldier.canon)>0:
                if(matrix[soldier.x][soldier.y]==1): matrix[soldier.x][soldier.y]=4 #Weak Attacks on canon
                else: matrix[soldier.x][soldier.y]=4  #Solid Attacking Position for canon
            else:
                if(matrix[soldier.x][soldier.y]==1): matrix[soldier.x][soldier.y]=1 #Weak Attacks on soldier
                else: matrix[soldier.x][soldier.y]=4 #Solid Attacking Position for soldier
            
        for canon1 in team['canons']:
            for x,y in canon1.bombs:
                matrix[x][y]=1 #Danger
            for x,y in canon1.blank_moves:
                matrix[x][y]=1 #Danger
            
        for x,y in team['townhall']:
            
            matrix[x][y]=8
            matrix[x][y+id_]=7
            try: 
                matrix[x+1][y+id_]=7
            except: pass
            try: 
                matrix[x-1][y+id_]=7
            except: pass
            try: 
                matrix[x+1][y]=7
            except: pass
            try: 
                matrix[x-1][y]=7
            except: pass
            
        self.dp= matrix
        
        
    def compute_child(self):
        k=0
        if(self.all_children==None):
            children=[[] for i in range(9)]
            try:
                index=0
                while(1):
                    ordering=self.dp
                    index+=1
                    A1,from_x,from_y,A2,to_x,to_y,new_state,new_self,new_opponent,turn=next(self.children)
                    id_=new_state[to_x][to_y]
                    try:

                        if id_==-1 and (to_x,to_y) in [(1, 7), (3, 7), (5, 7), (7, 7)]: raise AssertionError
                        if id_==1 and (to_x,to_y) in [(0, 0), (2, 0), (4, 0), (6, 0)]: raise AssertionError
                        move=" ".join([A1,str(from_x),str(from_y),A2,str(to_x),str(to_y)])
                        new_g=Game(new_state,new_self,new_opponent,turn)
                    
                        new_g.constraint_check()
                        k+=1
                        #if(k>30):
                            #raise StopIteration 
                        self.hash[move]=new_g
                        children[ordering[to_x][to_y]].append((new_g.evaluate(),move,new_g))
                    except:
                        pass
                        #print(move)
                        #display(self.state)
                        #print()
                        #display(new_g.state)
                        #new_g.constraint_check()
            except StopIteration:
                if self.turn==1: self.all_children=[sorted(child,reverse=True) for child in reversed(children)]
                else: self.all_children=[sorted(child) for child in children]
                ##print(len(children),"children found")
                
    def is_terminal(self):
        return len(self.self_team['townhall'])>2 and len(self.self_team['townhall'])<2
    
    def mini_max(self,cutoff,alpha=-1*float('inf'),beta=float('inf')):
        self.alpha=alpha
        self.beta=beta
        
        if cutoff==0: return (int(self.evaluate()),"",self),self.evaluate()

        if(len(self.opponent_team['soldiers'])==0 and cutoff<2):
             return (int(self.evaluate()),"",self),self.evaluate()
            
            


        if self.turn: value=-1*float('inf') #Maximising
        else: value=float('inf') #Minimising
        self.compute_child()
        last=None
        for k,children_order in enumerate(self.all_children):
            self.alpha=alpha
            self.beta=beta
            if(len(children_order)>0):
                #print("mini_max","cutoff",cutoff,"priority",8-k,"children",len(children_order))
                min_max_scores=[]
                ##print("mini_max",len(children_order))
                for index,move,child in children_order:
                    last= (index,move,child)
                    ##print(index,move,sum(list(map(lambda x:len(x.bombs),Global_Game.self_team['canons']))))
                    new_child,new_value=child.mini_max(cutoff-1,self.alpha,self.beta)
                    min_max_scores.append(new_child)
                    if self.turn:
                        value = max(value, new_value)
                        self.alpha = max(self.alpha, value)
                        ##print("turn1 :",value,new_value,self.alpha)
                        if(self.alpha>=self.beta):
                            #print("After pruning",len(min_max_scores),"node remained","from","{} nodes".format(len(children_order)))
                            #print(self.alpha,self.beta)
                            break
                    else:
                        value = min(value, new_value)
                        self.beta = min(self.beta, value)
                        if(self.alpha>=self.beta):
                            #print("After pruning",len(min_max_scores),"node remained","from","{} nodes".format(len(children_order)))
                            #print(self.alpha,self.beta)
                            break
                    
                ##print("cutoff",cutoff,min_max_scores)
                try:
                    if self.turn==1: optimal_score_index=min_max_scores.index(max(min_max_scores,key=lambda x:x[0]))
                    else: optimal_score_index=min_max_scores.index(min(min_max_scores,key=lambda x:x[0]))
                    optimal_score=int(min_max_scores[optimal_score_index][0])
                    assert optimal_score_index<len(children_order)
                    ##print("alpha-beta",self.alpha,self.beta)
                    #print("mini_max","cutoff",cutoff,"priority",8-k,"best eval",optimal_score,"player",self.turn)
                    #print(list(map(lambda x:x[0],min_max_scores)))
                    solution=(optimal_score,children_order[optimal_score_index][1],min_max_scores[optimal_score_index][2])
                    try:
                        if self.turn==1: 
                            if(optimal_score>0):
                                return solution,value
                            global_optima=max(global_optima,solution)
                        else: 
                            if(optimal_score<0):
                                return solution,value
                            global_optima=min(global_optima,solution)
                    except:
                        global_optima=solution
                except:
                    pass
        try:        
            return global_optima,value
        except:
            return self.minimax(1)

    #def iterative_deepening(self):
        
    
    def evaluate(self): #Reward (Maximise this for self, minimise this for opponent)
        #soldier_difference
        diff=len(self.self_team['soldiers'])-len(self.opponent_team['soldiers'])
        score=20*diff+30*(4**(diff))
        score-=30*(4**(-1*diff))
        #danger_difference
        score+=10*sum(map(lambda x:x.danger,self.opponent_team['soldiers']))-5*sum(map(lambda x:x.danger,self.self_team['soldiers']))
        #canon_difference
        score+=30+20*(len(self.self_team['canons'])-len(self.opponent_team['canons']))
        #Townhall_difference
        score+=500*(len(self.self_team['townhall'])-len(self.opponent_team['townhall']))
        if turn==1: id_=self.self_team['soldiers'][0].player_id
        else: id_=self.opponent_team['soldiers'][0].player_id
        ##print(id_)
        #Sum of dp matrix
        score+=4*sum(sum(j for i,j in zip(list1,list2) if i==id_) for list1,list2 in zip(self.state,self.dp))
        score+=(-1*sum(sold.evaluate() for sold in self.self_team['soldiers'])+sum(sold.evaluate() for sold in self.opponent_team['soldiers']))
        if(len(self.opponent_team['soldiers'])==0): 
            score+=30000
        if(len(self.opponent_team['townhall'])==2): 
            score+=25000

        if(len(self.opponent_team['soldiers'])<3):
            if sum(len(sol.moves) for sol in self.opponent_team['soldiers'])==0:
                score+= 15000
            
        if(len(self.self_team['soldiers'])<3):
            if sum(len(sol.moves) for sol in self.self_team['soldiers'])==0:
                score+= -15000
        if(len(self.self_team['soldiers'])==0): 
            score-=30000
        if(len(self.self_team['townhall'])==2): 
            score-=25000   


        return score
        #if self.turn==1: return score
        #else: return -1*score


# In[14]:


import sys
#S 2 7 M 2 4
text = sys.stdin.readline().strip()
#text= "0 8 8 150"
player,n,m,time_left=map(int,text.split())
if(player==1):  player_id,opponent_id=-1,1
else: player_id,opponent_id=1,-1
Global_Game,self,opponent,turn=start_game(player_id,opponent_id,n,m)
Global_Game=Game(Global_Game,self,opponent,turn)
i=player%2
while(1):
    if(i%2==0): #Opponent's turn
        
  
        move = sys.stdin.readline().strip()
        Global_Game=Global_Game.execute_move_opponent(move)
        
    else: #My turn
        
     
        solution,value=Global_Game.mini_max(2)
        score,move,game=solution    
        Global_Game=Global_Game.hash[move]
        
        #print(move)
        sys.stdout.write(move+ '\n')
        sys.stdout.flush()
    i+=1


# In[ ]:




