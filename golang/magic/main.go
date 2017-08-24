package main

import (
  "os"
  "log"
)

func mapSliceInt8ToInt8(mappedFunc func([]int8) int8, in [][]int8) (out []int8) {
	out = make([]int8, len(in))
	for i := range in {
		out[i] = mappedFunc(in[i])
	}
	return
}

func sliceInt8Filter(filterFunc func([]int8) bool, in [][]int8) (out [][]int8) {
	for _, val := range in {
		if filterFunc(val) {
			out = append(out, val)
		}
	}
	return
}


func sum(list []int8) (total int8) {
	for _, val := range list {
		total += val
	}
	return
}

// Finds the dot product of two equi-dimensional vectors.
func dotF2(v []int8, w []int8) (dotProd int8) {
	var total int
	if len(v) != len(w) {
		panic("len(v) != len(w)")
	}
	for i := range v {
		total += int(v[i] * w[i])
	}
	return int8(total % 2)
}

// Computes Av in the field with two elements.
func matmulF2(A [][]int8, v []int8) []int8{
  return mapSliceInt8ToInt8(func(arow []int8) int8 {
    return dotF2(arow, v)
  }, A)
}


func concatenateToAll(start []int8, listofls [][]int8) (result [][]int8) {
	result = make([][]int8, len(listofls))
	for i := range listofls {
		result[i] = append(start, listofls[i]...)
	}
	return
}

//Suppose w is a row vector over F2, and k is a scalar in F2. This finds all column vectors that satisfy w*v = k.
func vecsolveF2(w []int8, k int8) (v [][]int8) {
  if len(w) == 0 {
    panic("len(w) == 0")
  }
	if len(w) == 1 {
		if w[0] == 0 {
			return [][]int8{[]int8{0}, []int8{1}}
		}
    return [][]int8{[]int8{k}}
	}
	//subresult0 is the solution to the vector equation for w[1:] assuming w[0] * v[0] = 0
	subresult0 := vecsolveF2(w[1:], k)
	if w[0] == 0 {
		return append(concatenateToAll([]int8{0}, subresult0), concatenateToAll([]int8{1}, subresult0)...)
	}
	//subresult1 is the solution to the vector equation for w[1:]assuming w[0] * v[0] = 0
	subresult1 := vecsolveF2(w[1:], (k-1)%2)
	return append(concatenateToAll([]int8{0}, subresult0), concatenateToAll([]int8{1}, subresult1)...)
}

// Finds the set of all elements v such that A*v is the vector of all k's.
func matsolveF2(A [][]int8, k int8) (candidates [][]int8) {
	candidates = vecsolveF2(A[0], k)
	for _, r := range A[1:] {
		candidates = sliceInt8Filter(func(x []int8) bool { return dotF2(r, x) == k }, candidates)
	}
	return candidates
}

func kernelF2(A [][]int8) [][]int8 {
	return matsolveF2(A, 0)
}

var logger = log.New(os.Stdout, "magic ecc: ", log.Lshortfile|log.LUTC|log.Ltime|log.Ldate)

func main() {
  //matmul
  A := [][]int8{
    []int8{0,0,0},
    []int8{1,0,1},
    []int8{0,1,1},
    []int8{1,1,1},
  }
  v := []int8{1,1,0}
  result := []int8{0,1,1,0}
  logger.Println(result)
  logger.Println(matmulF2(A, v))

  //matsolve
  var k int8 = 0
  result2 := [][]int8{[]int8{0,0,0}}
  logger.Println(result2)
  logger.Println(matsolveF2(A, k))

  A = [][]int8{
    []int8{0,0,0,0},
    []int8{0,1,0,1},
    []int8{1,1,0,0},
  }

  result3 := [][]int8{
    []int8{0,0,0,0},
    []int8{0,0,1,0},
    []int8{1,1,0,1},
    []int8{1,1,1,1},
  }
  logger.Println(result3)
  logger.Println(kernelF2(A))
}


//func dotProd(w []int8, a int8)(vs [][]int8){
//
//}
