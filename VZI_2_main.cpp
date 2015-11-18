#include <iostream>
#include <string>
#include <memory>
#include <limits.h>
#include <queue>
#include <set>
#include <list>
#include <Windows.h>
#include <chrono>

#include "parser.h"

using namespace std::chrono;


struct CompareCost {											//porovnani dvou pairu podle prvniho prvku
	bool operator()(std::pair<int, int> v1, std::pair<int, int> v2) {
		return v1.first > v2.first;
	}
};



int main(int argc, char *argv[])
{
	GraphParser p;
	Problem_t problem;


	high_resolution_clock::time_point t1 = high_resolution_clock::now();

	p.parse("test10k.map.txt", problem);
	//p.parse("test10k-dir.map", problem);

	//POMOCNE PROMENNE
	int newCost = 0;											// pro vypocitani ceny pres aktualni uzel do jeho sousedu
	int neighbrCnt = 0;											// pocet sousedu daneho uzlu
	int currNeighbr;											// cislo/index soucasne reseneho souseda daneho uzlu
	std::vector<size_t> neighbrs;								// vektor sousedu daneho uzlu
	std::vector<int> dist(problem.dimension);					// vektor nejkratsich vzdalenosti
	std::vector<bool> visited(problem.dimension);				// vektor navstiveno true/false pro kazdy uzel
	std::vector<int> previous(problem.dimension);				// vektor uzlu, ze kterych jsme prisli se soucasnou cenou
	std::pair<int, int> node;

	int INF = UINT16_MAX;										// nase zvolene INF

	//epicka fronta paru s epickou vlastni porovnavaci funkci, yay...
	//std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int> >, CompareCost> pQueue;
	std::set<std::pair<int, int> > pQueue;


	//INICIALIZACE
	for (int x = 0; x < problem.dimension; x++) {
		visited[x] = false;										// vsechny uzly nenavstiveny
		dist[x] = INF;											// inicializujeme nekonecnem
		previous[x] = NULL;
	}
	dist[0] = 0;												//vzdalenost z pocatku do pocatku je 0
	//pQueue.push(std::make_pair(0, 0));						
	pQueue.insert(std::make_pair(0, 0));

	high_resolution_clock::time_point t2 = high_resolution_clock::now();



	//DIJKSTRA
	while (!pQueue.empty()) {

		//node = pQueue.top();
		//pQueue.pop();

		int v = pQueue.begin()->second;							//cislo uzlu, ktery ted resime
		pQueue.erase(pQueue.begin());

		neighbrCnt = problem.edgeList[v].size();				//pocet jeho sousedu

		for (int i = 0; i < neighbrCnt; i++) {
			currNeighbr = int(problem.edgeList[v][i]);			//cislo uzlu-souseda, kteremu odpovidaji hodnoty s indexem i

			if (!visited[currNeighbr]) {
				newCost = int(dist[v]) + int(problem.weightList[v][i]);	//cena soucasneho uzlu + cena cesty do i uzlu
				if (dist[currNeighbr] > newCost) {
					dist[currNeighbr] = newCost;						//pokud je cena cesty pres soucasny uzel kratsi, menime
					//pQueue.push(std::make_pair(newCost, currNeighbr));
					pQueue.insert(std::make_pair(newCost, currNeighbr));//kombinace <cena,uzel> do fronty
					previous[currNeighbr] = v;							//za predchudce dame soucasny uzel (jeho index)
				}

			}
		}
		visited[v] = true;										//nastavime uzel jako navstiveny
	}

	if (!visited[problem.dimension - 1]) {
		std::cerr << "Destination node unreachable from source node.\n";
		system("pause");
		return 1;
	}



	//VYPISY
	high_resolution_clock::time_point stop = high_resolution_clock::now();

	auto d1 = std::chrono::duration_cast<std::chrono::milliseconds>(stop - t1).count();
	auto d2 = std::chrono::duration_cast<std::chrono::milliseconds>(stop - t2).count();

	std::cout << "Clock 1: " << d1 << "\n";
	std::cout << "Clock 2: " << d2 << "\n";
	std::cout << "Cost: " << dist[problem.dimension - 1] << "\n";

	std::cout << "\nShortest Path:\n";

	int prev = problem.dimension - 1;
	std::vector<int> path;
	path.push_back(problem.dimension - 1);			//zacneme koncovym bodem

	while (prev != 0) {
		//std::cout << " " << previous[prev];
		path.push_back(previous[prev]);
		prev = previous[prev];
	}
	for (int i = path.size()- 1; i >= 0; i--){
		std::cout << path[i] << " ";
	}
	std::cout << "\n";

	system("pause");
	return 0;
}
