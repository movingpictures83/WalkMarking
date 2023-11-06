import random
import sys
from disk_struct import Disk
from page_replacement_algorithm import  page_replacement_algorithm
from CacheLinkedList import  CacheLinkedList
import numpy as np

import WALK_MARKING
import WALK_MARKING_SLOW

import PyIO
import PyPluMA

class WalkMarkingPlugin:
  def input(self, inputfile):
        self.parameters = PyIO.readParameters(inputfile)

  def run(self):
        pass

  def output(self, outputfile):
    n = int(self.parameters["n"])
    infile = open(PyPluMA.prefix()+"/"+self.parameters["infile"], 'r')
    kind = self.parameters["kind"]
    outfile = open(outputfile, 'w')
    outfile.write("cache size "+str(n))
    if (kind == "FAST"):
       wm = WALK_MARKING.WALK_MARKING(n)
    else:
       wm = WALK_MARKING_SLOW.WALK_MARKING_SLOW(n)
    page_fault_count = 0
    page_count = 0
    for line in infile:
        line = int(line.strip())
        outfile.write("request: "+str(line))
        if wm.request(line) :
            page_fault_count += 1
        page_count += 1

    
    outfile.write("page count = "+str(page_count))
    outfile.write("\n")
    outfile.write("page faults = "+str(page_fault_count))
    outfile.write("\n")
