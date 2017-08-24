package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"time"

	"github.com/wcharczuk/go-chart"
)

func mapSliceIntToSliceInt(mappedFunc func([]int) []int, in [][]int) (out [][]int) {
	out = make([][]int, len(in))
	for i := range in {
		out[i] = mappedFunc(in[i])
	}
	return
}

func sliceIntFilter(filterFunc func([]int) bool, in [][]int) (out [][]int) {
	for _, val := range in {
		if filterFunc(val) {
			out = append(out, val)
		}
	}
	return
}

func minInt(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func order(e edge) (o edge) {
	if e.V1 < e.V2 {
		o.V1, o.V2 = e.V2, e.V1
		return
	}
	return e
}

type edge struct {
	V1 int
	V2 int
}

type graph struct {
	nodeList     []int
	edgeList     map[edge]bool
	neighborList map[int]map[int]bool
}

func (g *graph) init(n int) {
	g.nodeList = make([]int, n)
	g.edgeList = make(map[edge]bool)
	g.neighborList = make(map[int]map[int]bool)
	for v := 0; v < n; v++ {
		g.nodeList[v] = v
		g.neighborList[v] = map[int]bool{}
	}
}

func (g *graph) edges() (edges []edge) {
	for edge, prs := range g.edgeList {
		if prs {
			edges = append(edges, edge)
		}
	}
	return
}

func (g *graph) nodes() []int {
	return g.nodeList
}

func (g *graph) neighbors(v int) (neighborVerts []int) {
	for v2, exists := range g.neighborList[v] {
		if exists {
			neighborVerts = append(neighborVerts, v2)
		}
	}
	return
}

func (g *graph) edge(v1, v2 int) bool {
	return g.edgeList[order(edge{v1, v2})]
}

func (g *graph) addEdge(v1, v2 int, prs bool) {
	if v1 != v2 { // don't allow loops
		//fmt.Println("adding edge", v1, v2, prs)
		g.neighborList[v1][v2] = prs
		g.neighborList[v2][v1] = prs
		//fmt.Println("ordered", order(edge{v1, v2}))
		g.edgeList[order(edge{v1, v2})] = prs
		//fmt.Println(g.edgeList)
		//fmt.Println(g.neighborList)
	}
}

func makeRandomBiPartGraph(l int, r int, prob float64) (g *graph) {
	g = new(graph)
	g.init(l + r)
	for li := 0; li < l; li++ {
		for ri := 0; ri < r; ri++ {
			prs := prob > rand.Float64()
			//fmt.Println(prs, li, ri)
			g.addEdge(li, l+ri, prs)
		}
	}
	return
}

func makeRandomGraph(n int, prob float64) (g *graph) {
	g = new(graph)
	g.init(n)
	for v1 := 0; v1 < n; v1++ {
		for v2 := 0; v2 < n; v2++ {
			g.addEdge(v1, v2, prob > rand.Float64())
		}
	}
	return
}

//Finds all sublists of our list, and multiplicities count.
func sublists(l []int) (subs [][]int) {
	if len(l) == 0 {
		return [][]int{[]int{}}
	}
	smallerSublists := sublists(l[1:])
	return append(smallerSublists, mapSliceIntToSliceInt(func(s []int) []int {
		return append(l[0:1], s...)
	}, smallerSublists)...)
}

//Finds all sublists of l with at most k elements.
func suffSmallSublists(l []int, k int) (subLists [][]int) {
	if k == 0 {
		return [][]int{}
	}
	if len(l) == 0 {
		return [][]int{[]int{}}
	}
	smallerSublists := suffSmallSublists(l[1:], k)
	allSublists := [][]int{}
	for _, s := range smallerSublists {
		if len(s) < k {
			allSublists = append(allSublists, append([]int{l[0]}, s...))
		}
	}
	return append(smallerSublists, allSublists...)
}

func edgeBoundary(G *graph, nodes []int) (edges []edge) {
	nodeMap := map[int]bool{}
	for _, node := range nodes {
		nodeMap[node] = true
	}
	for _, edge := range G.edges() {
		if (nodeMap[edge.V1] && !nodeMap[edge.V2]) || (nodeMap[edge.V2] && !nodeMap[edge.V1]) {
			edges = append(edges, edge)
		}
	}
	return
}

//Returns all length k lists that are contained within a given list, such that list
//ordering is preserved and multiplicities count. That is, [0,1,2,3,4,5,6] appears twice in the 7-sublists of[0,1,2,3,4,5,6,6].
func kSublists(l []int, k int) (subLists [][]int) {
	if k == 0 {
		return [][]int{[]int{}}
	}
	if len(l) < k {
		return
	}
	return append(kSublists(l[1:], k), mapSliceIntToSliceInt(func(s []int) []int {
		return append([]int{l[0]}, s...)
	}, kSublists(l[1:], k-1))...)
}

func removeEmptySublists(sublists [][]int) [][]int {
	return sliceIntFilter(func(subList []int) bool {
		return len(subList) > 0
	}, sublists)
}

//Finds the Cheeger constant of any graph (warning: my implementation is EXPTIME)
//The Cheeger constant of G is the minimum value of |dS| / |S|, over all node_sublists S of G with <= n/2 vertices. dS is the edge boundary of S.
func cheegerConstant(G *graph) (cheegerVal float64) {
	numNodes := len(G.nodes())
	nodeSublists := suffSmallSublists(G.nodes(), numNodes/2)
	cheegerVal = float64(numNodes) - 1 // An upper bound on the minimum value of the edge boundary, but it's possible that no node attains this value. In the for loop, this value will be used for comparison.
	for _, sl := range removeEmptySublists(nodeSublists) {
		cheegerVal = math.Min(cheegerVal, float64(len(edgeBoundary(G, sl)))/float64(len(sl)))
	}
	return
}

//func experimentalCheegerConstant(G graph) (cheegerVal float64) {
//	numNodes := len(G.nodes())
//	if numNodes == 1 {
//		return 0
//	}
//	nodeSublists := kSublists(G.nodes(), numNodes/2)
//	cheegerVal = float64(numNodes) - 1 //An upper bound on the minimum value of the edge boundary, but it's possible that no node attains this value. In the for loop, this value will be used for comparison.
//	for _, sl := range nodeSublists {
//		cheegerVal = math.Min(cheegerVal, float64(len(edgeBoundary(G, sl)))/float64(numNodes/2))
//	}
//	return
//}

type ioPair struct {
	R  float64
	N  int
	Cc float64
}

func getCheegerConst(r float64, n int, returnChan chan (ioPair)) {
	//g := makeRandomGraph(n, r)
	g := makeRandomBiPartGraph(4, n, r)
	fmt.Println(".edges()", g.edges())
	cc := cheegerConstant(g)
	returnChan <- ioPair{
		R:  r,
		N:  n,
		Cc: cc,
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())
	//n := 10
	//g := makeRandomGraph(n, 0.1)
	//fmt.Println(g.edges())
	//for i := 0; i < n; i++ {
	//	fmt.Println(i, g.neighbors(i))
	//}
	//fmt.Println(cheegerConstant(g))
	//fmt.Println(experimentalCheegerConstant(g))
	x := []float64{}
	y := []float64{}
	//for r := float64(0); r <= 1; r = r + 0.1 {
	returnChan := make(chan ioPair)
	r := 0.5
	var count = 0
	for i := 1; i < 15; i++ {
		for n := 0; n < 8; n++ {
			go getCheegerConst(r, i, returnChan)
			count++
		}
	}
	for i := 0; i < count; i++ {
		pair := <-returnChan
		x = append(x, float64(pair.N))
		y = append(y, pair.Cc)
	}
	fmt.Println(x, y)
	drawGraph(x, y)
}

func drawGraph(x, y []float64) {
	//fmt.Println(x)
	//fmt.Println(y)
	graph := chart.Chart{
		XAxis: chart.XAxis{
			Style: chart.Style{
				Show: true, //enables / displays the x-axis
			},
		},
		YAxis: chart.YAxis{
			Style: chart.Style{
				Show: true, //enables / displays the y-axis
			},
		},
		Series: []chart.Series{
			chart.ContinuousSeries{
				Style: chart.Style{
					Show:        true,
					StrokeWidth: chart.Disabled,
					DotWidth:    5,
				},
				XValues: x,
				YValues: y,
			},
		},
	}

	buffer, err := os.Create("/tmp/cheeger.png")
	if err != nil {
		fmt.Println(err)
	}
	defer buffer.Close()
	err = graph.Render(chart.PNG, buffer)
	if err != nil {
		fmt.Println(err)
	}
}
