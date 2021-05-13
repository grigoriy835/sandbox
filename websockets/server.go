package main

import (
	"crypto/subtle"
	"fmt"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"sync"
)

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	log.Printf("server: WARN env variable %s is not setted", key)
	return fallback
}

var CONN_HOST = "0.0.0.0"
var CONN_PORT = getEnv("ws_port", "8080")
var USER = getEnv("ws_user", "admin")
var PASSWORD = getEnv("ws_password", "admin")

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
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("server: upgrade:", err)
		return
	}
	defer c.Close()

	cliId := r.URL.Query()["id"]
	namespace := r.URL.Query()["namespace"]
	reconnect := r.URL.Query()["reconnect"]
	login := r.URL.Query()["login"]
	password := r.URL.Query()["password"]
	if len(login) < 1 || len(password) < 1 || login[0] != USER || password[0] != PASSWORD {
		log.Print("server: drop unauthorized client: ", cliId, login, password)
		return
	}

	if len(cliId) == 0 {
		cliId = []string{"generated_" + uuid.NewString()}
	}

	fmt.Printf("server: new client %s in %s\n", cliId[0], namespace[0])
	defer fmt.Printf("server: client out %s\n", cliId[0])

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
						log.Println("server: write:", err)
						break
					}
				}
			}
		}
	}

	for {
		message := <-cli.C
		fmt.Printf("server: write %v to %s\n", message, cliId)
		err = c.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			log.Println("server: write:", err)
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
		fmt.Fprintln(w, "server: no clients detected")
		return
	}
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
	log.Println("server: start server")
	http.HandleFunc("/get_updates", get_updates)
	http.HandleFunc("/push_update", push_update)
	log.Fatal(http.ListenAndServe(CONN_HOST+":"+CONN_PORT, nil))
}
