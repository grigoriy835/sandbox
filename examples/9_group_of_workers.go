package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	fmt.Printf("start\n")

	workerPools()

	waitGroup()
}

func worker1(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Println("worker", id, "started  job", j)
		time.Sleep(time.Second)
		fmt.Println("worker", id, "finished job", j)
		results <- j * 2
	}
}

func workerPools() {
	const numJobs = 10
	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)

	for w := 1; w <= 3; w++ {
		go worker1(w, jobs, results)
	}

	for j := 1; j <= numJobs; j++ {
		jobs <- j
	}
	close(jobs)

	for a := 1; a <= numJobs; a++ {
		<-results
	}
}

func worker2(id int, wg *sync.WaitGroup) {

	defer wg.Done()

	fmt.Printf("Worker %d starting\n", id)

	time.Sleep(2 * time.Second)
	fmt.Printf("Worker %d done\n", id)
}

func waitGroup() {

	var wg sync.WaitGroup

	go func(group *sync.WaitGroup) {
		for i := 1; i <= 5; i++ {
			wg.Add(1)
			go worker2(i, &wg)
		}
		wg.Wait()
		fmt.Printf("w8ed in gorutine\n")

	}(&wg)

	time.Sleep(time.Second)
	wg.Wait()
	fmt.Printf("w8ed in main tread\n")
}
