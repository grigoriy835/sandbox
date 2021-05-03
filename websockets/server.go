package main

import (
	"flag"
	"fmt"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
)

var addr = flag.String("addr", "localhost:8880", "http service address")

type Client struct {
	id string
	C  chan []byte
}

type ClientsList struct {
	sync.Mutex
	clients []*Client
}

func (cList *ClientsList) Push(c *Client) {
	cList.Lock()
	defer cList.Unlock()
	cList.clients = append(cList.clients, c)
}

func (cList *ClientsList) Delete(clientId string) {
	cList.Lock()
	defer cList.Unlock()

	for index, client := range cList.clients {
		if client.id == clientId {
			cList.clients = append(cList.clients[:index], cList.clients[index+1:]...)
			break
		}
	}
}

func (cList *ClientsList) SendToAll(mess []byte) {
	cList.Lock()
	defer cList.Unlock()

	for _, client := range cList.clients {
		client.C <- mess
	}
}

var nameSpaces = make(map[string]*ClientsList)

var upgrader = websocket.Upgrader{} // use default options

func get_updates(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()

	cliId := r.URL.Query()["id"][0]
	namespace := r.URL.Query()["namespace"][0]

	fmt.Printf("new client %s in %s\n", cliId, namespace)
	defer fmt.Printf("client out %s\n", cliId)

	cList, prs := nameSpaces[namespace]
	if !prs {
		cList = &ClientsList{}
		nameSpaces[namespace] = cList
	}

	cli := Client{cliId, make(chan []byte)}
	cList.Push(&cli)
	defer cList.Delete(cliId)

	for {
		message := <-cli.C
		fmt.Printf("write %v to %s\n", message, cliId)
		err = c.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			log.Println("write:", err)
			break
		}
	}
}

func push_update(w http.ResponseWriter, r *http.Request) {
	namespace := r.URL.Query()["namespace"][0]
	message, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Fatalln(err)
	}
	cList, prs := nameSpaces[namespace]
	if !prs || len(cList.clients) == 0 {
		fmt.Fprintln(w, "no clients detected\n")
		return
	}
	fmt.Printf("write message %s to all in %v\n", message, namespace)
	cList.SendToAll(message)

	w.WriteHeader(http.StatusOK)
}

func main() {
	log.SetFlags(0)
	http.HandleFunc("/get_updates", get_updates)
	http.HandleFunc("/push_update", push_update)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
