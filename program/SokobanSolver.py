# author Robert Ruska
# 2017.11.3

import  text2dimacs

class SokobanSolver():

    def __init__(self, filename, states):
        self.map = []
        self.states = states
        self.player = []
        self.boxesstart = []
        self.boxesgoal = []

        with open(filename,'r') as file:
            for line in file:
                self.map.append(list(line[:len(line)-1]))

        self.map[len(self.map)-1] = ''.join(self.map[len(self.map)-1])
        player = self.map[len(self.map)-1].split(" ")

        self.player.append(int(player[0]))
        self.player.append(int(player[1]))
        self.map.pop(len(self.map)-1)



        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "o":
                    self.boxesstart.append([i,j])
                elif self.map[i][j] == "_":
                    self.boxesgoal.append([i,j])

    def get_map(self):
        return self.map

    def get_stats(self):
        return self.states

    def solve(self):
        self.generate_minisat_input()

    def generate_minisat_input(self):
        with open("output", 'w') as out:
            self.generate_initial_state(out)
            self.generate_goal_state(out)
            self.generate_actions(out)
            self.generate_exclusuivity(out)
            self.generate_background_kwn(out)
            self.generaete_frame_probme(out)

    def generate_initial_state(self, out):
        # initial state
        out.write("c INITIAL STATE\n")
        out.write("\n")

        # player at start
        out.write("c player at start\n")
        out.write("at(p,{},{},0)".format(self.player[0], self.player[1]))
        out.write("\n")

        # boxes at start
        out.write("\n")
        out.write("c boxes at start\n")
        for i in self.boxesstart:
            out.write("at(b,{},{},0)".format( i[0], i[1]))
            out.write("\n")


        # player not at start
        out.write("\n")
        out.write("c player not at start\n")
        for i in range(1, len(self.map) - 1):
            for j in range(1, len(self.map[i]) - 1):
                if (self.map[i][j] != "x"):
                    if not (i == self.player[0] and j == self.player[1]):
                        out.write("-at(p,{},{},0)".format(i, j))
                        out.write("\n")

        # boxes not at start
        out.write("\n")
        out.write("c boxes not at start\n")
        for box in self.boxesstart:
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if (self.map[i][j] != "x" and self.map[i][j] != "o"):
                        out.write("-at(b,{},{},0)".format(i, j))
                        out.write("\n")


        out.write("\n")


    def generate_goal_state(self, out):
        # goal state
        out.write("c GOAL STATE\n")
        out.write("\n")

        # boxes at goal
        out.write("\n")
        out.write("c boxes at goal\n")
        for i in self.boxesgoal:
                out.write("at(b,{},{},{})".format( i[0], i[1], self.states))
                out.write("\n")

        # player not at goal
        out.write("\n")
        out.write("c player not at goal\n")
        for i in self.boxesgoal:
            out.write("-at(p,{},{},{})".format(i[0], i[1], self.states))
            out.write("\n")

        #boxes not at goal
        out.write("\n")
        out.write("c boxes not at goal\n")
        out.write("\n")
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if(self.map[i][j] != "x" and self.map[i][j]  != "_" ):
                    out.write("-at(b,{},{},{})".format( i, j, self.states))
                    out.write("\n")
        out.write("\n")

    def generate_actions(self, out):
        out.write("\n")
        out.write("c ACTIONS")
        out.write("\n")

        #player moves to all places, preconds and effects

        #precond player not at next place at state 0
        #precond player at old place at state 0
        #efect player at next place at state 1
        #effect player not at old place at state 1

        out.write("c player moves to all places")
        out.write("\n")
        for n in range(1,self.states+1):
            for i in range(1,len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] !="x":
                        for s in 'udlr':
                            if s == "u" and self.map[i-1][j] != "x" :
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i - 1, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i - 1, j, n-1))
                            elif s == "d" and self.map[i+1][j] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i,j,i+1,j,n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i + 1, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i+1 ,j ,n-1))
                            elif s == "l" and self.map[i][j-1] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j-1, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i ,j-1 ,n-1))
                            elif s == "r" and self.map[i][j+1] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1,n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j+1, n ))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))

                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i , j+1, n-1))

        #move box to all places
        #precond move player at same state to old box position
        #precond not box at next place at state 0
        #effect  box at next place state 1
        #effect not box at old place before state 1

        out.write("\n")
        out.write("c move box to all places")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] != "x":
                        for s in 'udlr':
                            if s == "u" and self .map[i - 1][j] != "x" and i+1 < len(self.map) and self.map[i+1][j] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("move(p,{},{},{},{},{})\n".format(i+1,j,i,j,n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i - 1, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i - 1, j, n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))

                            elif s == "d" and i+1 < len(self.map)-1 and self.map[i + 1][j] != "x" and self.map[i-1][j] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("move(p,{},{},{},{},{})\n".format(i-1,j,i,j,n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i + 1, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i+1, j, n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i , j, n))

                            elif s == "l" and self.map[i][j - 1] != "x" and j+1 < len(self.map[i]) and self.map[i][j+1] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j, i , j-1, n))
                                out.write(" v ")
                                out.write("move(p,{},{},{},{},{})\n".format(i,j+1,i,j,n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j - 1, n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j - 1, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j , n))
                            elif s == "r" and j+1 < len(self.map[i]) and self.map[i][j + 1] != "x" and self.map[i][j-1] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("move(p,{},{},{},{},{})\n".format(i,j-1,i,j,n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j+1, n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j, n-1))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))

                                out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j + 1, n-1))


    def generate_exclusuivity(self,out):
        out.write("\n")
        out.write("c EXCLUSIVITY")
        out.write("\n")

        # player at only one place/state
        out.write("\n")
        out.write("c player at only one place/state")
        out.write("\n")
        for n in range(1, self.states+1):
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] != "x":
                        for k in range(len(self.map)):
                            for l in range(len(self.map[k])):
                                    if self.map[k][l] != "x":
                                        if i!=k or j!= l:
                                            out.write("-at(p,{},{},{}) v -at(p,{},{},{})\n".format(i,j,n,k,l,n))
        out.write("\n")

        #one from player,box,empty at place/state
        out.write("\n")
        out.write("c player or box only one place/state")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] != "x":
                        out.write("-at(b,{},{},{}) v -at(p,{},{},{})\n".format(i,j,n,i,j,n))
        out.write("\n")


        #player moves exlusvity
        out.write("\n")

        out.write("c player moves exlusivity")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if self.map[i][j] != "x":
                        way = []
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                            elif s == "d" and self.map[i + 1][j] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))

                            elif s == "l" and self.map[i][j - 1] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))

                            elif s == "r" and self.map[i][j + 1] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                        for s1 in way:
                            for s2 in way:
                                if s1 != s2:
                                    out.write(s1 + " v " + s2 + "\n")

        out.write("\n")
        #box moves exlusivity
        out.write("c box moves exclusivity")
        out.write("\n")

        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] != "x":
                        way = []
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                            elif s == "d" and self.map[i + 1][j] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))

                            elif s == "l" and self.map[i][j - 1] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))

                            elif s == "r" and self.map[i][j + 1] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                        for s1 in way:
                            for s2 in way:
                                if s1 != s2:
                                    out.write(s1 + " v " + s2 + "\n")

        out.write("\n")


    def generate_background_kwn(self,out):
        #player must move at every state once
        out.write("c BACKGROUND KNOWLEDGE")
        out.write("\n")
        out.write("\n")
        out.write("c player moves")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if self.map[i][j] != "x":
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x":
                                out.write("move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                            elif s == "d" and self.map[i + 1][j] != "x":
                                out.write("move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                            elif s == "l" and self.map[i][j - 1] != "x":
                                out.write("move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                            elif s == "r" and self.map[i][j + 1] != "x":
                                out.write("move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                            else:
                                continue
            out.write("\n")

        #if player move and box is there box must move too
        out.write("\n")
        out.write("c player moves and box is there box must moove too")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if self.map[i][j] != "x":
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x" and i-2 > 0 and self.map[i-2] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})".format(i-1,j,n-1))
                                out.write(" v ")
                                out.write("move(b,{},{},{},{},{})\n".format(i-1,j,i-2,j,n))
                            elif s == "d" and self.map[i + 1][j] != "x" and i+2 < len(self.map) and self.map[i+2][j] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})".format(i +1, j, n-1))
                                out.write(" v ")
                                out.write("move(b,{},{},{},{},{})\n".format(i + 1, j, i + 2, j, n))
                            elif s == "l" and self.map[i][j - 1] != "x" and j-2 > 0 and self.map[i][j-2] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})".format(i, j-1, n-1))
                                out.write(" v ")
                                out.write("move(b,{},{},{},{},{})\n".format(i, j-1, i, j-2, n))
                            elif s == "r" and self.map[i][j + 1] != "x" and j+2 < len(self.map[i]) and self.map[i][j+2] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})".format(i, j+1, n-1))
                                out.write(" v ")
                                out.write("move(b,{},{},{},{},{})\n".format(i, j+1, i, j+2, n))
                            else:
                                continue
            out.write("\n")

            # cannot move from corners
            # place bordered with 2 walls next to each other
            out.write("\n")
            out.write("c cannot move from corners")
            out.write("\n")
            for n in range(1, self.states + 1):
                for i in range(1, len(self.map) - 1):
                    for j in range(1, len(self.map[i]) - 1):
                        if self.map[i][j] != "x":
                            for s in 'udlr':
                                if s == "u" and i - 1 > 0 and self.map[i - 1][j] != "x":
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                    out.write(" v ")
                                    out.write("at(b,{},{},{})\n".format(i - 1, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                    out.write(" v ")
                                    out.write("-at(b,{},{},{})\n".format(i, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                elif s == "d" and i + 1 < len(self.map) - 1 and self.map[i + 1][j] != "x":
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                    out.write(" v ")
                                    out.write("at(b,{},{},{})\n".format(i + 1, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                    out.write(" v ")
                                    out.write("-at(b,{},{},{})\n".format(i, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                elif s == "l" and j - 1 > 0 and self.map[i][j - 1] != "x":
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                    out.write(" v ")
                                    out.write("at(b,{},{},{})\n".format(i, j - 1, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                    out.write(" v ")
                                    out.write("-at(b,{},{},{})\n".format(i, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j - 1, n))
                                elif s == "r" and j + 1 < len(self.map[i]) - 1 and self.map[i][j + 1] != "x":
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                    out.write(" v ")
                                    out.write("at(b,{},{},{})\n".format(i, j + 1, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                    out.write(" v ")
                                    out.write("-at(b,{},{},{})\n".format(i, j, n))
                                    out.write("-move(b,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                else:
                                    continue
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j, n - 1))

            #box cannot move back to old place at next state
            out.write("\n")
            out.write("c box cannot move back to old place at next state")
            out.write("\n")
            for n in range(1, self.states):
                for i in range(1, len(self.map) - 1):
                    for j in range(1, len(self.map[i]) - 1):
                        if self.map[i][j] != "x":
                            for s in 'udlr':
                                if s == "u" and i - 1 > 0 and self.map[i - 1][j] != "x":
                                    out.write("-move(b,{},{},{},{},{}) v ".format(i, j, i - 1, j, n))
                                    out.write("-move(b,{},{},{},{},{})\n".format(i - 1, j, i, j, n + 1))
                                elif s == "d" and i + 1 < len(self.map) - 1 and self.map[i + 1][j] != "x":
                                    out.write("-move(b,{},{},{},{},{}) v ".format(i, j, i + 1, j, n))
                                    out.write("-move(b,{},{},{},{},{})\n".format(i + 1, j, i, j, n + 1))
                                elif s == "l" and j - 1 > 0 and self.map[i][j - 1] != "x":
                                    out.write("-move(b,{},{},{},{},{}) v ".format(i, j, i, j - 1, n))
                                    out.write("-move(b,{},{},{},{},{}) v \n".format(i, j - 1, i, j, n + 1))
                                elif s == "r" and j + 1 < len(self.map[i]) - 1 and self.map[i][j + 1] != "x":
                                    out.write("-move(b,{},{},{},{},{}) v ".format(i, j, i, j + 1, n))
                                    out.write("-move(b,{},{},{},{},{}) v \n".format(i, j + 1, i, j, n + 1))


            #player and box cannot swap positions
            out.write("\n")
            out.write("c player and box cannot swap positions")
            out.write("\n")
            for n in range(1, self.states-1):
                for i in range(1, len(self.map) - 1):
                    for j in range(1, len(self.map[i]) - 1):
                        if self.map[i][j] != "x":
                            for s in 'udlr':
                                if s == "u" and i - 1 > 0 and self.map[i - 1][j] != "x":
                                    out.write("-b({},{},{}) v -p({},{},{}) v -b({},{},{})\n".format(i,j,n,i-1,j,n,i-1,j,n+1))
                                elif s == "d" and i + 1 < len(self.map) - 1 and self.map[i + 1][j] != "x":
                                    out.write(
                                        "-b({},{},{}) v -p({},{},{}) v -b({},{},{})\n".format(i, j, n, i + 1, j, n, i + 1,j, n + 1))
                                elif s == "l" and j - 1 > 0 and self.map[i][j - 1] != "x":
                                    out.write("-b({},{},{}) v -p({},{},{}) v -b({},{},{})\n".format(i, j, n, i, j-1, n, i,j-1, n + 1))

                                elif s == "r" and j + 1 < len(self.map[i]) - 1 and self.map[i][j + 1] != "x":
                                    out.write("-b({},{},{}) v -p({},{},{}) v -b({},{},{})\n".format(i, j, n, i, j + 1, n, i,j + 1, n + 1))


    def generaete_frame_probme(self,out):
        out.write("c FRAME PROBLEM\n")
        out.write("\n")

        #player frame problem
        out.write("c player frame problem")
        out.write("\n")
        for n in range(1, self.states+1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] != "x":
                        c = 0
                        if self.map[i-1][j] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i-1,j,i,j,n))
                            c+=1
                        if i+1 < len(self.map)-1 and self.map[i + 1][j] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i + 1, j, i, j, n))
                            c += 1
                        if self.map[i][j-1] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i , j-1, i, j, n))
                            c += 1
                        if j+1 < len(self.map[i]) and self.map[i][j+1] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i , j + 1, i, j, n))
                            c += 1
                        if c > 0:
                            out.write("at(p,{},{},{}) v ".format(i, j, n - 1))
                            out.write("-at(p,{},{},{}) v ".format(i, j, n))

                        out.write("\n")

        out.write("\n")

        #box frame problem
        out.write("c box frame problem")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] != "x":
                        out.write("at(b,{},{},{}) v ".format(i, j, n - 1))
                        out.write("-at(b,{},{},{}) v ".format(i, j, n))
                        if self.map[i - 1][j] != "x":
                            out.write("move(b,{},{},{},{},{}) v ".format(i - 1, j, i, j, n))
                        if i + 1 < len(self.map)- 1 and self.map[i + 1][j] != "x":
                            out.write("move(b,{},{},{},{},{}) v ".format(i + 1, j, i, j, n))
                        if self.map[i][j - 1] != "x":
                            out.write("move(b,{},{},{},{},{}) v ".format(i, j - 1, i, j, n))
                        if self.map[i][j + 1] != "x":
                            out.write("move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                        out.write("\n")

        out.write("\n")

        #box and player frame problem
        out.write("c box and player frame problem")
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i]) ):
                    if self.map[i][j] != "x":
                        out.write("at(b,{},{},{}) v ".format(i, j, n - 1))
                        out.write("-at(b,{},{},{}) v ".format(i, j, n))
                        if i - 2 > 0 and self.map[i - 2][j] != "x" and self.map[i-1][j] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i - 2, j, i - 1, j, n))
                        if i + 2 < len(self.map) - 1 and self.map[i + 2][j] != "x" and self.map[i+1][j] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i + 2, j, i + 1, j, n))
                        if j - 2 > 0 and self.map[i][j - 2] != "x" and self.map[i][j-1] != "x":
                            out.write("move(p,{},{},{},{},{}) v ".format(i, j - 2, i, j - 1, n))
                        if j + 2 < len(self.map[i]) and self.map[i][j + 2] != "x" and self.map[i][j+1] != "x":
                            out.write("move(p,{},{},{},{},{})".format(i, j + 2, i, j + 1, n))
                        out.write("\n")

        out.write("\n")

        # box and player frame problem
        #if player moves to place where is no box other boxes should stay
        out.write("\n")
        for n in range(1, self.states + 1):
            for i in range(1, len(self.map)):
                for j in range(1, len(self.map[i])):
                    if self.map[i][j] != "x":
                        for k in range(1, len(self.map)):
                            for l in range(1, len(self.map[i])):
                                if self.map[k][l] != "x":
                                    for s in 'udlr':
                                        if s == "u" and self.map[i - 1][j] != "x":
                                            out.write("-move(p,{},{},{},{},{})".format(i, j, i - 1, j, n))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(i-1,j,n-1))
                                            out.write(" v ")
                                            out.write("-at(b,{},{},{})".format(k, l, n - 1))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(k, l, n))
                                        elif s == "d" and self.map[i + 1][j] != "x":
                                            out.write("-move(p,{},{},{},{},{})".format(i, j, i + 1, j, n))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(i + 1, j, n - 1))
                                            out.write(" v ")
                                            out.write("-at(b,{},{},{})".format(k, l, n - 1))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(k, l, n))

                                        elif s == "l" and self.map[i][j - 1] != "x":
                                            out.write("-move(p,{},{},{},{},{})".format(i, j, i, j-1, n))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(i, j-1, n - 1))
                                            out.write(" v ")
                                            out.write("-at(b,{},{},{})".format(k, l, n - 1))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(k, l, n))

                                        elif s == "r" and self.map[i][j + 1] != "x":
                                            out.write("-move(p,{},{},{},{},{})".format(i, j, i, j + 1, n))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(i, j + 1, n - 1))
                                            out.write(" v ")
                                            out.write("-at(b,{},{},{})".format(k, l, n - 1))
                                            out.write(" v ")
                                            out.write("at(b,{},{},{})".format(k, l, n))

                                        out.write("\n")



        out.write("\n")




if __name__ == '__main__':

    import sys

    inp =  sys.stdin
    filename = sys.argv[1]
    states = sys.argv[2]

    print filename
    print states

    try:
        print states
        Sokoban = SokobanSolver(filename, int(states))
        Sokoban.solve()

        print "..Generating input for Minisat.."

        inf = open('output', 'r')

        outf = sys.stdout
        outf = open('outsat', 'w')

        print "..Converting output for minisat.."
        text2dimacs.translate(inf,outf)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        if 'No such file or directory' in message:
            print 'No such file or directory'
        elif 'index' in message:
            'Map description is not correct'
        else:
            print message

        raise ex

    # import sys

    # Socoban = SocobanSolver("test", 3)
    # Socoban.generate_minisat_input()
    #
    # inf = open('output', 'r')
    #
    # outf = sys.stdout
    # outf = open('outsat', 'w')
    #
    # text2dimacs.translate(inf, outf)


