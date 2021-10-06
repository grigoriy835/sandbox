package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	fmt.Printf("start\n")

	arguments()
	flags()
}

func arguments() {
	/*
		$ ./command-line-arguments a b c d
	*/

	argsWithProg := os.Args
	argsWithoutProg := os.Args[1:]

	arg := os.Args[3]

	fmt.Println(argsWithProg)    //[./command-line-arguments a b c d]
	fmt.Println(argsWithoutProg) //[a b c d]
	fmt.Println(arg)             //c
}

func flags() {
	/*
		$ ./command-line-flags -word=opt -numb=7 -fork -svar=flag
	*/

	wordPtr := flag.String("word", "foo", "a string")

	numbPtr := flag.Int("numb", 42, "an int")
	boolPtr := flag.Bool("fork", false, "a bool")

	var svar string
	flag.StringVar(&svar, "svar", "bar", "a string var")

	flag.Parse()

	fmt.Println("word:", *wordPtr)    //word: opt
	fmt.Println("numb:", *numbPtr)    //numb: 7
	fmt.Println("fork:", *boolPtr)    //fork: true
	fmt.Println("svar:", svar)        //svar: flag
	fmt.Println("tail:", flag.Args()) //tail: []
}
