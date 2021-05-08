package main

import "sync"

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

type History struct {
	sync.Mutex
	records [][]byte
}

func (history *History) Add(record []byte) {
	history.Lock()
	defer history.Unlock()
	history.records = append(history.records[1:], record)
}

func (history *History) GetArr() [][]byte {
	history.Lock()
	defer history.Unlock()
	return append([][]byte{}, history.records...)
}
