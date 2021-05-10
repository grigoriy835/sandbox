package main

import (
	"bytes"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"net/url"
	"testing"
	"time"
)

//positive test for main functionality
func TestServer1(t *testing.T) {
	//start server
	go func() {
		main()
	}()

	<-time.After(2 * time.Second)

	//message emitter 1 to test
	go func() {
		u := url.URL{Scheme: "http", Host: CONN_HOST + ":" + CONN_PORT,
			Path: "/push_update", User: url.UserPassword(USER, PASSWORD),
			RawQuery: "namespace=test"}
		messages := []string{"mess1", "mess2", "mess3", "mess4"}

		for number, message := range messages {
			<-time.After(time.Second)
			buf := bytes.NewBuffer([]byte(message))
			log.Printf("push message %s to %s", message, u.String())
			resp, err := http.Post(u.String(), "text", buf)
			if err != nil {
				t.Errorf("error while sending %d message, %s", number, err)
			}
			if resp.Status != "200 OK" {
				t.Errorf("not 200 response while sending %d message, %s", number, resp.Status)
			}
		}

	}()
	//message emitter 2 to test1
	go func() {
		u := url.URL{Scheme: "http", Host: CONN_HOST + ":" + CONN_PORT,
			Path: "/push_update", User: url.UserPassword(USER, PASSWORD),
			RawQuery: "namespace=test1"}
		messages := []string{"xxxx1", "xxxx2", "xxxx3"}

		for number, message := range messages {
			<-time.After(time.Second)
			buf := bytes.NewBuffer([]byte(message))
			log.Printf("push message %s to %s", message, u.String())
			resp, err := http.Post(u.String(), "text", buf)
			if err != nil {
				t.Errorf("error while sending %d message, %s", number, err)
			}
			if resp.Status != "200 OK" {
				t.Errorf("not 200 response while sending %d message, %s", number, resp.Status)
			}
		}

	}()
	//message emitter 3 to testNone
	go func() {
		u := url.URL{Scheme: "http", Host: CONN_HOST + ":" + CONN_PORT,
			Path: "/push_update", User: url.UserPassword(USER, PASSWORD),
			RawQuery: "namespace=testNone"}
		messages := []string{"none1", "none2", "none3", "none4"}

		for number, message := range messages {
			<-time.After(time.Second)
			buf := bytes.NewBuffer([]byte(message))
			log.Printf("push message %s to %s", message, u.String())
			resp, err := http.Post(u.String(), "text", buf)
			if err != nil {
				t.Errorf("error while sending %d message, %s", number, err)
			}
			if resp.Status != "200 OK" {
				t.Errorf("not 200 response while sending %d message, %s", number, resp.Status)
			}
		}

	}()

	//clients
	u := url.URL{Scheme: "ws", Host: CONN_HOST + ":" + CONN_PORT,
		Path: "/get_updates"}

	//ws client
	u.RawQuery = "login=" + USER + "&password=" + PASSWORD + "&namespace=test&id=cli1"
	url1 := u.String()
	go func() {
		CheckMessagesFromSocket("cli1", url1, []string{"mess1", "mess2", "mess3", "mess4"}, t)
	}()

	//ws client
	u.RawQuery = "login=" + USER + "&password=" + PASSWORD + "&namespace=test&id=cli2"
	url2 := u.String()
	go func() {
		CheckMessagesFromSocket("cli2", url2, []string{"mess1", "mess2", "mess3", "mess4"}, t)
	}()

	//ws client
	u.RawQuery = "login=" + USER + "&password=" + PASSWORD + "&namespace=test1&id=cli3"
	url3 := u.String()
	go func() {
		CheckMessagesFromSocket("cli3", url3, []string{"xxxx1", "xxxx2", "xxxx3"}, t)
	}()

	<-time.After(3 * time.Second)
	//ws client
	u.RawQuery = "login=" + USER + "&password=" + PASSWORD + "&namespace=test&id=cli4&reconnect=1"
	url4 := u.String()
	go func() {
		CheckMessagesFromSocket("cli4", url4, []string{"mess1", "mess2", "mess3", "mess4"}, t)
	}()

	<-time.After(5 * time.Second)
}

func CheckMessagesFromSocket(clientPrefix string, url string, messages []string, t *testing.T) {
	log.Printf("connect to %s", url)
	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		t.Errorf("client %s, cant connect to %s, %s", clientPrefix, url, err)
		return
	}
	defer c.Close()
	for number, expectedMessage := range messages {
		_, message, err := c.ReadMessage()
		if expectedMessage != string(message) {
			t.Errorf("client %s, message number %d, expected %s, actual %s",
				clientPrefix, number, expectedMessage, string(message))
		}
		if err != nil {
			t.Errorf("client %s, cant get message number %d, %s", clientPrefix, number, err)
			return
		}
	}
}
