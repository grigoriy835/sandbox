package main

import (
	"crypto/subtle"
	"fmt"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
)

const (
	CONN_HOST = "localhost"
	CONN_PORT = "8080"
	USER      = "admin"
	PASSWORD  = "admin"
)

var nameSpaces = make(map[string]*ClientsList)
var history = make(map[string]*History)

var upgrader = websocket.Upgrader{} // use default options

func BasicAuth(w http.ResponseWriter, r *http.Request) bool {
	user, pass, ok := r.BasicAuth()
	if !ok || subtle.ConstantTimeCompare([]byte(user),
		[]byte(USER)) != 1 || subtle.ConstantTimeCompare([]byte(pass),
		[]byte(PASSWORD)) != 1 {
		w.Header().Set("WWW-Authenticate", `Basic realm="Credentials:"`)
		w.WriteHeader(401)
		w.Write([]byte("Unauthorized\n"))
		return false
	}
	return true
}

func get_updates(w http.ResponseWriter, r *http.Request) {
	if !BasicAuth(w, r) {
		return
	}
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()

	cliId := r.URL.Query()["id"]
	namespace := r.URL.Query()["namespace"]
	reconnect := r.URL.Query()["reconnect"]

	if len(cliId) == 0 {
		cliId = []string{"generated_" + uuid.NewString()}
	}

	fmt.Printf("new client %s in %s\n", cliId[0], namespace[0])
	defer fmt.Printf("client out %s\n", cliId[0])

	cList, prs := nameSpaces[namespace[0]]
	if !prs {
		cList = &ClientsList{}
		nameSpaces[namespace[0]] = cList
	}

	cli := Client{cliId[0], make(chan []byte)}
	cList.Push(&cli)
	defer cList.Delete(cliId[0])

	if len(reconnect) > 0 && reconnect[0] == "1" {
		historyByNamespace, prs := history[namespace[0]]
		if prs {
			for _, message := range historyByNamespace.GetArr() {
				if message != nil {
					err = c.WriteMessage(websocket.TextMessage, message)
					if err != nil {
						log.Println("write:", err)
						break
					}
				}
			}
		}
	}

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
	if !BasicAuth(w, r) {
		return
	}
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
	historyByNamespace, prs := history[namespace]
	if !prs {
		historyByNamespace = &History{sync.Mutex{}, make([][]byte, 10)}
		history[namespace] = historyByNamespace
	}

	historyByNamespace.Add(message)
	cList.SendToAll(message)

	w.WriteHeader(http.StatusOK)
}

func main() {
	log.SetFlags(0)
	http.HandleFunc("/get_updates", get_updates)
	http.HandleFunc("/push_update", push_update)
	log.Fatal(http.ListenAndServe(CONN_HOST+":"+CONN_PORT, nil))
}
