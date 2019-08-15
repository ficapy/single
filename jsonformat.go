package main

import (
	"bytes"
	"encoding/json"
	"github.com/atotto/clipboard"
	"log"
)

func main() {
	j, err := clipboard.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	dst := &bytes.Buffer{}
	if err := json.Indent(dst, []byte(j), "", "    "); err != nil {
		log.Fatal(err)
	}

	err = clipboard.WriteAll(string(dst.Bytes()))
	if err != nil {
		log.Fatal(err)
	}
}
