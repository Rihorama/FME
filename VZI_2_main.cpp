#include <iostream>
#include <string>
#include <memory>
#include <limits.h>

#include "parser.h"



int main(int argc, char *argv[])
{
	GraphParser p;
	Problem_t problem;

	p.parse("test10k.map.txt", problem);
	//p.parse("test10k-dir.map", problem);

	//inicializace pomocnych promennych
	int newCost = 0;											// pro vypocitani ceny pres aktualni uzel do jeho sousedu
	int neighbrCnt = 0;											// pocet sousedu daneho uzlu
	int currNeighbr;											// cislo/index soucasne reseneho souseda daneho uzlu
	std::vector<size_t> neighbrs;								// vektor sousedu daneho uzlu
	std::vector<size_t> dist;									// vektor nejkratsich vzdalenosti
	std::vector<std::vector<size_t>> shortestPath;				// vektor vektoru uzlu, pres ktere vede nejkratsi cesta do uzlu
	shortestPath.resize(problem.dimension);						// nastavime na pocet uzlu
	int INF = UINT16_MAX;										// nase zvolene INF


	for (int v = 0; v < problem.dimension; v++) {
		dist.push_back(INF);									//inicializujeme nekonecnem
	}
	dist[0] = 0;												//vzdalenost z pocatku do pocatku je 0	


	for (int v = 0; v < problem.dimension; v++) {
		neighbrs = problem.edgeList[v];
		neighbrCnt = neighbrs.size();

		for (int i = 0; i < neighbrCnt; i++) {
			currNeighbr = int(problem.edgeList[v][i]);						//cislo uzlu-souseda, kteremu odpovidaji hodnoty s indexem i
			newCost = int(dist[v]) + int(problem.weightList[v][i]);			//cena soucasneho uzlu + cena cesty do i uzlu
			
			if (dist[currNeighbr] > newCost) {
				dist[currNeighbr] = newCost;								//pokud je cena cesty pres soucasny uzel kratsi, menime
				shortestPath[currNeighbr] = shortestPath[v];	
				shortestPath[currNeighbr].push_back(v);						//nejkratsi cesta do tohoto souseda je tedy totozna
																			//s nejkratsi cestou do soucasneho uzlu + soucasny uzel
			}
		}
	}

	std::cout << "\nShortest Path: ";
	for (int v : shortestPath[problem.dimension - 1]) {
		std::cout << v << " ";
	}
	std::cout << problem.dimension - 1 << "\n";

	std::cout << "Cost: " << dist[problem.dimension - 1] << "\n";

	system("pause");
	return 0;
}
