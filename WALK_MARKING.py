import random
import sys
import numpy as np
from disk_struct import Disk
from page_replacement_algorithm import  page_replacement_algorithm
from random_graph import Graph
from markov_matrix import Markov
from aux import *

class WALK_MARKING(page_replacement_algorithm):

    def __init__(self, N):
        self.T = Disk(N)
        self.H = Disk(N)
        self.N = N
        self.marked = set()
        self.G = {} ## local access graph

        self.is_first_request = True
        self.last_request = -1

        self.page_probability = {}

        self.fast_mode = True
        self.use_weights = False
        self.weights = {}

    def get_N(self) :
        return self.N

    def request(self,page) :
        # print('request: ', page)
        page_fault = False

        if not self.is_first_request :
            self.__add_edge(self.last_request, page)

        self.last_request = page
        self.is_first_request = False

        if page in self.T  :
            ## Mark page
            self.marked.add(page)
        else :

            if page in self.H :
                self.H.delete(page)

            # Start a new phase when all pages are marked and a page fault occurs
            # Unmark all the pages
            if len(self.marked) == self.N :
                self.marked.clear()

                if self.fast_mode is True:
                    self.page_probability = self.__calculate_prob(page)

            if self.T.size() == self.N :

                if self.fast_mode is False :
                    self.page_probability = self.__calculate_prob(page)


                ## Get the set of unmarked pages
                U = set(self.T.getData()) - self.marked
                U_list = list(U)
                U_dist = []
                for u in U_list :
                    U_dist.append(self.page_probability[u])

                page_to_evict = random_select_page(U_list, U_dist)

                ## Delete page from cache
                self.T.delete(page_to_evict)

                ## Remove least resent page from history
                if self.H.size() == self.N :
                    hist_lru = self.H.deleteFront()
                    if hist_lru is not None and hist_lru in self.G :
                        self.G.pop(hist_lru, None)

                ## Move discarted page to history
                self.H.add(page_to_evict)

            ## Mark page and add to T
            self.marked.add(page)
            self.T.add(page)

            ## Page fault is True
            page_fault = True

        return page_fault



    def __add_edge(self, u,v) :
        if u not in self.G :
            self.G[u] = {}
        if v not in self.G :
            self.G[v] = {}

        if v not in self.G[u] :
            self.G[u][v] = 0
        if u not in self.G[v] :
            self.G[v][u] = 0

        self.G[u][v] += 1
        self.G[v][u] += 1

        # self.G[u] = self.G[u] | {v}
        # self.G[v] = self.G[v] | {u}

    def get_adj_matrix(self) :
        ## Mapping
        node_id = {}
        node_name = {}
        for i,node in enumerate(self.G) :
            node_id[node] = i
            node_name[i] = node

        A = np.zeros((len(node_id),len(node_id)))
        for u in self.G :
            adj = list(self.G[u])
            for v in adj:
                if v in self.G :
                    u_id = node_id[u]
                    v_id = node_id[v]

                    if self.use_weights :
                        A[u_id,v_id] = self.G[u][v]
                        A[v_id,u_id] = self.G[u][v]
                    else :
                        A[u_id,v_id] = 1
                        A[v_id,u_id] = 1
                else :
                    self.G[u].pop(v, None)

        # print(A)
        ## Normalize
        for u in range(len(A)) :
            degree = np.sum(A[u,:])
            if degree > 0:
                A[u,:] /= degree

        return A,node_id,node_name

    def __calculate_prob(self, init_page) :
        A,node_id,node_name = self.get_adj_matrix()

        u = node_id[init_page]
        n = len(A)

        M = Markov(A)
        R = M.random_walk_distribution(u)

        # print('R = ',R)
        P = {}
        for u,p in enumerate(R) :
            # print('PR[%s] = %f' % (node_name[u], pr))
            P[node_name[u]] = p

        return P

    ######################################################################################################################################

    def page_label(self,page):
        lab = "%s(%.1f)" % (page, self.page_probability[page] if page in self.page_probability else 0)
        return lab

    def page_color(self,page) :
        if page in self.marked :
            return 1 ## Red
        else :
            return 0 # white

    def debug(self) :
        X = []
        for u in self.get_data() :
            X.append((self.P[u],u))

    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.T.get_data()]
