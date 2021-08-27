package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

type WebStorage struct {
	host string
}

func NewWebStorage(host string) *WebStorage {
	return &WebStorage{host: host}
}

type PairRecord struct {
	pair_id   int
	curr_from string
	curr_to   string
	config    map[string]interface{}
}

type ScheduleRecord struct {
	source_name string
	source_id   int
	pairs       []PairRecord
}

func (s *WebStorage) FetchScheduleConfig() ([]ScheduleRecord, error) {
	var m []ScheduleRecord

	req, err := http.NewRequest("POST", fmt.Sprintf("http://%v/schedule/get_all_by_sources", s.host), nil)
	if err != nil {
		return nil, err
	}
	defer req.Body.Close()
	err = json.NewDecoder(req.Body).Decode(&m)
	if err != nil {
		return nil, err
	}

	return m, nil
}

func (s *WebStorage) StoreQuotesData(data []interface{}) error {
	body, err := json.Marshal(data)
	if err != nil {
		return err
	}
	_, err = http.NewRequest("POST", fmt.Sprintf("http://%v/quotes/save_quotes", s.host), bytes.NewBuffer(body))
	if err != nil {
		return err
	}

	return nil
}

func main() {

	fmt.Println("")
}
