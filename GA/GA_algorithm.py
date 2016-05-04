#!/usr/bin/python
import GA_chromosome, GA_functions
import random, copy


class GeneticAlgorithm:
    
    def __init__(self,attr_dict):
        
        self.popul_size = attr_dict["population_size"]
        self.iter_cnt = attr_dict["iteration_cnt"]
        self.mut_prob = attr_dict["mutation_probability"]
        self.bin_len = attr_dict["bit_array_length"]
        self.dim_cnt = attr_dict["dim_cnt"]
        self.minimum = attr_dict["minimum"]
        self.maximum = attr_dict["maximum"]
        self.fit_func_no = attr_dict["fitness"]
        
        self.initializeGeneration() #list of chromosomes
        
        self.bestList = []
        self.best = False
        
        self.cut1 = self.bin_len / 3  #cuts in thirds
        self.cut2 = self.cut1 * 2

        
    
    
    def initializeGeneration(self):
        
        generation = []
        GA_chromosome.Chromosome.mapSeeds = [] #manually resetting seed list

        for i in range(0,self.popul_size):
            chromosome = GA_chromosome.Chromosome(self.dim_cnt, \
                self.bin_len, self.minimum, self.maximum)
            
            generation.append(chromosome)
            
        self.generation = generation
        
        counter = 0
        for c in self.generation:
            counter = counter + 1
            
    
    
    #MAIN MANAGING METHOD
    def start(self):     
                
        for i in range(0,self.iter_cnt):
        
            self.evaluation()         
            selected = self.selection()        
            new_gen = self.crossover(selected)            
            self.mutation(new_gen)
            
        return [self.best,self.bestList]

        
        
        
        
        
    def evaluation(self):
        
        best = False  #variable with the best result from this run  
                
        for gene in self.generation:
            decimal = gene.getDecimal()

            fitness = GA_functions.getFitness(self.fit_func_no,decimal)

            gene.setFitness(fitness)  #saves fitness in the chromosome
            
            if best == False or fitness < best:
                best = fitness
                
        self.bestList.append(best)
        
        if self.best == False or self.best > best:
            self.best = best
            
        
    
    
    #tournament method
    def selection(self):        
        
        selected = []
        #count of good individuals that will proceed
        selected_cnt = self.popul_size / 2
        
        #rounding up so the selected_cnt is even number
        selected_cnt = selected_cnt + (selected_cnt % 2)
        

        #two random rivals
        for i in range(0,selected_cnt):
            #ran1 = random.randint(0,self.popul_size-1)
            #ran2 = random.randint(0,self.popul_size-1)
            
            ran1 = random.randint(0,len(self.generation)-1)
            ran2 = random.randint(0,len(self.generation)-1)
            rival_1 = self.generation[ran1]
            rival_2 = self.generation[ran2]

            
            #we go for minimum
            if rival_1.getFitness() < rival_2.getFitness():
                selected.append(rival_1) 
                self.generation.pop(ran1)
            else:
                selected.append(rival_2)
                self.generation.pop(ran2)
                
                
        return selected
    
    
    
    def crossover(self,parents):        
        
        #remaining size of population that is to be filled with children
        # /2 because each run produces 2 children
        size = (self.popul_size - len(parents))/2
        new_gen = copy.deepcopy(parents)
                
        for i in range(0,size):
            
            #two new chromosomes are made
            child0 = GA_chromosome.Chromosome(self.dim_cnt, \
                    self.bin_len, self.minimum, self.maximum)
            child1 = GA_chromosome.Chromosome(self.dim_cnt, \
                    self.bin_len, self.minimum, self.maximum)
            
            child0_list = []
            child1_list = []
            
            #randomly selected parents
            mommy = parents[random.randint(0,len(parents))-1]
            daddy = parents[random.randint(0,len(parents))-1]
            
            m_genes = mommy.getBinary()
            d_genes = daddy.getBinary()

            
            #for each dimension a cut is made and added to respective child binary list
            for x in range(0,len(m_genes)):
                child0_list.append(self.doCut(m_genes[x],d_genes[x],0))
                child1_list.append(self.doCut(m_genes[x],d_genes[x],1))
                
            child0.setBinary(child0_list) #gives children their new chromosomes
            child1.setBinary(child1_list)
            str(m_genes)
            
            new_gen.append(child0)
            new_gen.append(child1)
            
        return new_gen
            
            
    def mutation(self,new_gen):
        
        how_many_will_mutate = int(self.mut_prob * self.popul_size)
        how_many_genes = int(self.mut_prob * self.bin_len)
        
        #if either one is zero, there is no point to continue
        if not how_many_will_mutate and how_many_genes:
            return
        
        mutants = []
        
        for i in range(0,how_many_will_mutate):
            mutant = new_gen[random.randint(0,self.popul_size-1)]
            mutants.append(mutant)
        
        #for each of chosen mutants, each of his chromosome dimensions mutates
        #on random positions of count "how many genes"
        for mutant in mutants: 
            
            for dim_i in range(0,len(mutant.getBinary())):
                for mutating_gene in range(0,how_many_genes):                
                
                    gene_i = random.randint(0,self.bin_len-1)
                    mutant.swapGene(dim_i,gene_i,)
        
        self.generation = new_gen
        return
    
            
    #TODO - control cuts, if the bit length is too small, there could be a problem        
    #does the Cut using i dimension of mommy and daddy
    #childNo = 0 stands for child that has 1st and 3rd third from mommy
    #childNo = 1 stands for child that has 1st and 3rd third from daddy
    def doCut(self,mommy,daddy,childNo):
        
        new_gene = []
        
        if childNo == 0:
            first = mommy
            second = daddy            
        else:
            first = daddy
            second = mommy
            
        for i in range(0,self.cut1):
            new_gene.append(first[i])
            
        for i in range(self.cut1,self.cut2):
            new_gene.append(second[i])
            
        for i in range(self.cut2,self.bin_len):
            new_gene.append(first[i])
            
        return new_gene
    
    
    