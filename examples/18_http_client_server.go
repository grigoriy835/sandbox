package main

import (
	"bufio"
	"fmt"
	"net/http"
)

func main() {
	print("start\n")

	//client()
	server()
}

func client() {

	resp, err := http.Get("http://gobyexample.com")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("Response status:", resp.Status)

	scanner := bufio.NewScanner(resp.Body)
	for i := 0; scanner.Scan() && i < 5; i++ {
		fmt.Println(scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}
}

// SERVER --------------------------------------------------------------------------------
func hello1(w http.ResponseWriter, req *http.Request) {

	fmt.Fprintf(w, "hello\n")
}

func headers(w http.ResponseWriter, req *http.Request) {

	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func getParams(w http.ResponseWriter, req *http.Request) {
	fmt.Println(req.URL.Query())

	for name, params := range req.URL.Query() {
		for _, h := range params {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func server() {

	http.HandleFunc("/hello", hello1)
	http.HandleFunc("/headers", headers)
	http.HandleFunc("/get_params", getParams)

	http.ListenAndServe(":8090", nil)
}
