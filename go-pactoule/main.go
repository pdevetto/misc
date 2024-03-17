package main

import (
	"fmt"
	"pactoule/party"
)

func main() {
	fmt.Println("Pactoule")

	p := party.CreateParty()
	p.PlayCLI()
	//bubblecli.PlayBubbleTea()

}
