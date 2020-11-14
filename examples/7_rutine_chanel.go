package main

import (
	"fmt"
	"time"
)

func f(from string) {
	for i := 0; i < 3; i++ {
		fmt.Println(from, ":", i)
	}
}

func worker(done chan bool) {
	fmt.Print("working...")
	time.Sleep(time.Second)
	fmt.Println("done")

	done <- true
}

func main() {
	// GORUTINE -----------------------------------------------------------------------------

	f("direct")

	go f("goroutine")

	go func(msg string) {
		fmt.Println(msg)
	}("going")

	time.Sleep(time.Second)
	fmt.Println("done")

	//CHAIN -----------------------------------------------------------------------

	messages := make(chan string)

	go func() { messages <- "ping" }()

	msg := <-messages
	fmt.Println(msg)

	//BUFFERED ---------------------------------------------------------------------

	messages1 := make(chan string, 2)

	messages1 <- "buffered"
	messages1 <- "channel"

	fmt.Println(<-messages1)
	fmt.Println(<-messages1)

	//GORUTINE SYNC ---------------------------------------------------------------\

	done := make(chan bool, 1)
	go worker(done)

	<-done

	//SELECT ----------------------------------------------------------------------------
	c1 := make(chan string)
	c2 := make(chan string)

	go func() {
		time.Sleep(1 * time.Second)
		c1 <- "one"
	}()
	go func() {
		time.Sleep(2 * time.Second)
		c2 <- "two"
	}()

	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-c1:
			fmt.Println("received", msg1)
		case msg2 := <-c2:
			fmt.Println("received", msg2)
		}
	}

	//TIMEOUT -----------------------------------------------------------------------

	v1 := make(chan string, 1)
	go func() {
		time.Sleep(2 * time.Second)
		v1 <- "result 1"
	}()

	select {
	case res := <-v1:
		fmt.Println(res)
	case <-time.After(1 * time.Second):
		fmt.Println("timeout 1")
	}

	v2 := make(chan string, 1)
	go func() {
		time.Sleep(2 * time.Second)
		v2 <- "result 2"
	}()
	select {
	case res := <-v2:
		fmt.Println(res)
	case <-time.After(3 * time.Second):
		fmt.Println("timeout 2")
	}

	// NON-BLOCKING -------------------------------------------------------------

	messages2 := make(chan string)
	signals := make(chan bool)

	select {
	case msg := <-messages2:
		fmt.Println("received message", msg)
	default:
		fmt.Println("no message received")
	}

	msg = "hi"
	select {
	case messages2 <- msg:
		fmt.Println("sent message", msg)
	default:
		fmt.Println("no message sent")
	}

	select {
	case msg := <-messages2:
		fmt.Println("received message", msg)
	case sig := <-signals:
		fmt.Println("received signal", sig)
	default:
		fmt.Println("no activity")
	}

	//CLOSING JOBS -------------------------------------------------------------------------

	jobs := make(chan int, 5)
	done1 := make(chan bool)

	go func() {
		for {
			j, more := <-jobs
			if more {
				fmt.Println("received job", j)
			} else {
				fmt.Println("received all jobs")
				done1 <- true
				return
			}
		}
	}()

	for j := 1; j <= 3; j++ {
		jobs <- j
		fmt.Println("sent job", j)
	}
	close(jobs)
	fmt.Println("sent all jobs")

	<-done1

	// RANGE ---------------------------------------------------------------------------------------

	queue := make(chan string, 2)
	queue <- "one"
	queue <- "two"
	close(queue)

	for elem := range queue {
		fmt.Println(elem)
	}
}
