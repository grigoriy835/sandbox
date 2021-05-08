package main

import (
	"fmt"
)

type Test struct {
	tt []string
}

func (test *Test) do() []string {
	return append([]string{}, test.tt...)
}

func main() {
	fmt.Println("start\n")

	ll := make([][]byte, 10)

	for _, v := range ll {
		if v != nil {
			fmt.Println("ne nil")
		} else {
			fmt.Println("nil")
		}
	}
	fmt.Println(ll)

}
