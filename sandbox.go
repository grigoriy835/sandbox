package main

import (
	"fmt"
	"time"
)

func get(messages chan string, prefix string) {
	for {
		mess := <-messages
		println(mess + prefix)
	}
}

func main() {
	print("start\n")

	messages := make(chan string)

	go get(messages, " first")
	go get(messages, " second")

	go func() {
		ticker := time.NewTicker(time.Hour)
		for {
			<-ticker.C
			messages <- "mess"
		}
	}()

	var ll []int
	ll = make([]int, 0)
	ll = append(ll, 1, 2, 3, 4, 5)

	for k, v := range ll {
		if v == 3 {
			ll = append(ll[:k], ll[k+1:]...)
			break
		}
	}

	fmt.Println(ll)
}
