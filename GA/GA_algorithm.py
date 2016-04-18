#!/usr/bin/python
import GA_chromosome


class GeneticAlgorithm:
    
    def __init__(self,attr_dict):
        
        self.popul_size = attr_dict["population_size"]
        self.iter_cnt = attr_dict["iteration_cnt"]
        self.mut_prob = attr_dict["mutation_probability"]
        self.bin_len = attr_dict["bit_array_length"]
        self.dim_cnt = attr_dict["dim_cnt"]
        self.minimum = attr_dict["minimum"]
        self.maximum = attr_dict["maximum"]        
        
        self.generation = self.initializeGeneration() #list of chromosomes
        
    
    
    def initializeGeneration(self):
        
        generation = []
        GA_chromosome.Chromosome.isSet = False #manually resetting flag
        
        for i in range(0,self.popul_size):
            chromosome = GA_chromosome.Chromosome(self.dim_cnt, \
                self.bin_len, self.minimum, self.maximum)
            
            generation.append(chromosome)
            
        self.generation = generation
        
        counter = 0
        for c in self.generation:
            print "CHROMOSOME " + str(counter)
            c.printBinary()
            counter = counter + 1