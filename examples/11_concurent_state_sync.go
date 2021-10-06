package main

import (
	"fmt"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	fmt.Printf("start\n")

	byAtomic()

	byMutex()

	byStatefulGorutine()
}

func byAtomic() {
	var ops uint64

	var wg sync.WaitGroup

	for i := 0; i < 50; i++ {
		wg.Add(1)

		go func() {
			for c := 0; c < 1000; c++ {

				//операция поддерживает корректную работу при куче конкарент потоков которые хотят работать с переменной
				atomic.AddUint64(&ops, 1)
			}
			wg.Done()
		}()
	}

	wg.Wait()

	fmt.Println("ops:", ops)
}

func byMutex() {

	var state = make(map[int]int)

	//ссылка на обьект мутекс который может локать доступ к стейту
	var mutex = &sync.Mutex{}

	var readOps uint64
	var writeOps uint64

	//100 воткеров на чтение
	for r := 0; r < 100; r++ {
		go func() {
			total := 0
			for {

				key := rand.Intn(5)
				//пока мы не залокаем мутекс мы не можем читатть/писать в пошереную между потоками переменную
				mutex.Lock()
				total += state[key]
				mutex.Unlock()
				atomic.AddUint64(&readOps, 1)

				time.Sleep(time.Millisecond)
			}
		}()
	}

	//10 воркеров на запись
	for w := 0; w < 10; w++ {
		go func() {
			for {
				key := rand.Intn(5)
				val := rand.Intn(100)
				mutex.Lock()
				state[key] = val
				mutex.Unlock()
				atomic.AddUint64(&writeOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	//даем этому всему поработать секунду
	time.Sleep(time.Second)

	//принт статистику
	readOpsFinal := atomic.LoadUint64(&readOps)
	fmt.Println("readOps:", readOpsFinal)
	writeOpsFinal := atomic.LoadUint64(&writeOps)
	fmt.Println("writeOps:", writeOpsFinal)

	//доступ к переменной все еще через лок потомучто за эту переменную куча бомжей(потоков) сражается
	mutex.Lock()
	fmt.Println("state:", state)
	mutex.Unlock()
}

func byStatefulGorutine() {
	// типы которые будут запросом на чтение или запись
	type readOp struct {
		key  int
		resp chan int
	}
	type writeOp struct {
		key  int
		val  int
		resp chan bool
	}

	// счетчики событий чтения и записи
	var readOps uint64
	var writeOps uint64

	//каналы для пересылки запросов чтения и записи
	reads := make(chan readOp)
	writes := make(chan writeOp)

	//главная горутина, хранит стейт и предоставляет к нему доступ через слушание каналов чтения и записи и обработки
	//запросов которые с них приходят
	go func() {
		var state = make(map[int]int)
		for {
			select {
			case read := <-reads:
				read.resp <- state[read.key]
			case write := <-writes:
				state[write.key] = write.val
				write.resp <- true
			}
		}
	}()

	//100 воркеров на чтение, на каждое событие создается обьект с событием чтения и канал через который придет ответ
	for r := 0; r < 100; r++ {
		go func() {
			for {
				read := readOp{
					key:  rand.Intn(5),
					resp: make(chan int)}
				reads <- read
				<-read.resp
				atomic.AddUint64(&readOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	//10 воркеров на запись
	for w := 0; w < 10; w++ {
		go func() {
			for {
				write := writeOp{
					key:  rand.Intn(5),
					val:  rand.Intn(100),
					resp: make(chan bool)}
				writes <- write
				<-write.resp
				atomic.AddUint64(&writeOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}

	//даем секунду этому добру поработать
	time.Sleep(time.Second)

	//принт результат
	readOpsFinal := atomic.LoadUint64(&readOps)
	fmt.Println("readOps:", readOpsFinal)
	writeOpsFinal := atomic.LoadUint64(&writeOps)
	fmt.Println("writeOps:", writeOpsFinal)
}
