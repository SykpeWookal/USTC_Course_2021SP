import util

"""
Data sturctures we will use are stack, queue and priority queue.

Stack: first in last out
Queue: first in first out
    collection.push(element): insert element
    element = collection.pop() get and remove element from collection

Priority queue:
    pq.update('eat', 2)
    pq.update('study', 1)
    pq.update('sleep', 3)
pq.pop() will return 'study' because it has highest priority 1.

"""

"""
problem is a object has 3 methods related to search state:

problem.getStartState()
Returns the start state for the search problem.

problem.isGoalState(state)
Returns True if and only if the state is a valid goal state.

problem.getChildren(state)
For a given state, this should return a list of tuples, (next_state,
step_cost), where 'next_state' is a child to the current state, 
and 'step_cost' is the incremental cost of expanding to that child.

"""
def myDepthFirstSearch(problem):
    visited = {}
    frontier = util.Stack()

    frontier.push((problem.getStartState(), None))

    while not frontier.isEmpty():
        state, prev_state = frontier.pop()

        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]                
        
        if state not in visited:
            visited[state] = prev_state

            for next_state, step_cost in problem.getChildren(state):
                frontier.push((next_state, state))

    return []


def myBreadthFirstSearch(problem):
    # YOUR CODE HERE
    visited = {}    #存储访问过的节点
    frontier = util.Queue() #队列结构存储待访问节点

    frontier.push((problem.getStartState(), None))

    while not frontier.isEmpty():#还有待访问节点时继续
        #取出下一步访问的节点，判断是否为目标节点，返回或扩展
        state, prev_state = frontier.pop()

        if problem.isGoalState(state): #找到目标节点，返回
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]

        if state not in visited:    #在BFS下，拓展该节点
            visited[state] = prev_state
            for next_state, step_cost in problem.getChildren(state):
                frontier.push((next_state, state))
    return []



def myAStarSearch(problem, heuristic):
    # YOUR CODE HERE
    visited = {} #已访问节点列表
    frontier = util.PriorityQueue() #优先队列存储待访问节点
    frontier.__init__()
    #优先队列结构：同时插入状态与权值，权值为 g+h，初始节点 g=0
    frontier.push(((problem.getStartState(),0), (None,0)), 0 + heuristic(problem.getStartState()))

    while not frontier.isEmpty():
        (state,g), (prev_state,prev_g) = frontier.pop()
        #与BFS类似，从优先队列中取出下个待访问的节点，判断是否为目标，返回或扩展它
        if problem.isGoalState(state):
            solution = [state]
            while prev_state != None:
                solution.append(prev_state)
                prev_state = visited[prev_state]
            return solution[::-1]

        #扩展节点，同时将 gn 值赋予即将插入优先队列的待访问节点
        if state not in visited:
            visited[state] = prev_state
            for next_state, step_cost in problem.getChildren(state):
                next_g = g + step_cost
                frontier.push(((next_state,next_g), (state,g)), next_g + heuristic(next_state))
    return []

"""
Game state has 4 methods we can use.

state.isTerminated()
Return True if the state is terminated. We should not continue to search if the state is terminated.

state.isMe()
Return True if it's time for the desired agent to take action. We should check this function to determine whether an agent should maximum or minimum the score.

state.getChildren()
Returns a list of legal state after an agent takes an action.

state.evaluateScore()
Return the score of the state. We should maximum the score for the desired agent.

"""



class MyMinimaxAgent():

    def __init__(self, depth):
        self.depth = depth

    #用于选择使用MAX方案还是MIN方案
    def minimax(self, state, depth):
        if state.isMe():
            return self.maxv(state,depth)
        return self.minv(state,depth)

    #MAX节点操作
    def maxv(self,state,depth):
        beststate = None
        bestv = -float('inf')
        if state.isTerminated():
            return None, state.evaluateScore()
        if depth == 0:
            return state, state.evaluateScore()

        for child in state.getChildren():
            st,sc = self.minimax(child, depth-1)
            if sc >= bestv:
                bestv = sc
                beststate = child
        return beststate,bestv

    #MIN节点的操作
    def minv(self,state,depth):
        beststate = None
        bestv = float('inf')
        if state.isTerminated():
            return None, state.evaluateScore()
        for child in state.getChildren():
            st,sc = self.minimax(child, depth)
            if sc <= bestv:
                bestv = sc
                beststate = child
        return beststate,bestv

    #外部调用的接口，输入当前状态返回下一步的最佳行动状态
    def getNextState(self, state):
        best_state, _ = self.minimax(state, self.depth)
        return best_state


class MyAlphaBetaAgent():

    def __init__(self, depth):
        self.depth = depth

    def getNextState(self, state):
        # YOUR CODE HERE
        #util.raiseNotDefined()
        best_state, _ = self.alpha_beta_cut(state, self.depth, -float('inf'), float('inf'))
        return best_state

    def alpha_beta_cut(self, state, depth, alpha, beta):
        if state.isMe():
            return self.alpha_beta_cutmaxv(state,depth, alpha, beta)
        return self.alpha_beta_cutminv(state,depth, alpha, beta)


    def alpha_beta_cutmaxv(self,state,depth, alpha, beta):
        beststate = None
        bestv = -float('inf')
        if state.isTerminated():
            return None, state.evaluateScore()
        if depth == 0:
            return state, state.evaluateScore()

        for child in state.getChildren():
            st,sc = self.alpha_beta_cut(child, depth-1, alpha, beta)
            if sc > bestv:
                bestv = sc
                beststate = child
            if bestv > beta:
                return beststate,bestv
            alpha = max(alpha, bestv)
        return beststate,bestv


    def alpha_beta_cutminv(self,state,depth, alpha, beta):
        beststate = None
        bestv = float('inf')
        if state.isTerminated():
            return None, state.evaluateScore()
        for child in state.getChildren():
            st,sc = self.alpha_beta_cut(child, depth, alpha, beta)
            if sc < bestv:
                bestv = sc
                beststate = child
            if bestv < alpha:
                return beststate,bestv
            beta = min(beta, bestv)
        return beststate,bestv
