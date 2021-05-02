package main

import (
	"flag"
	"fmt"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
)

var addr = flag.String("addr", "localhost:8880", "http service address")

var upgrader = websocket.Upgrader{} // use default options

func get_updates(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()
	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			break
		}
		log.Printf("recv: %s", message)
		err = c.WriteMessage(mt, message)
		if err != nil {
			log.Println("write:", err)
			break
		}
	}
}

func push_update(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "hello\n")
	log.Println("hello bitch")
}

func main() {
	log.SetFlags(0)
	http.HandleFunc("/get_updates", get_updates)
	http.HandleFunc("/push_update", push_update)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
