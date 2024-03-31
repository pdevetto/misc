package main

import (
	"fmt"
	"os"

	"pactoule/party"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

type highScore struct {
	name  string
	score int
}

type step = int

const (
	play step = iota
	newparty
	highscore
	menu
)

type model struct {
	party    *party.Party
	scores   []highScore
	step     step
	cursor   int      // which to-do menu item our cursor is pointing at
	mainMenu []string // items on the menu
	logs     string
}

var pactouleStyle = lipgloss.NewStyle().PaddingLeft(2).PaddingTop(1).PaddingBottom(5)

func initialModel() model {
	return model{
		party:  nil,
		scores: make([]highScore, 0, 5),
		step:   menu,
		cursor: 0,
		mainMenu: []string{
			"Continue",
			"New party",
			"High scores",
		},
	}
}

func (m model) Init() tea.Cmd {
	// Just return `nil`, which means "no I/O right now, please."
	return nil
}

func controlMenu(msg tea.Msg, m model) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case tea.KeyMsg:

		// Cool, what was the actual key pressed?
		switch msg.String() {

		// These keys should exit the program.
		case "ctrl+c", "q":
			return m, tea.Quit

		// The "up" and "k" keys move the cursor up
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}

		// The "down" and "j" keys move the cursor down
		case "down", "j":
			if m.cursor < len(m.mainMenu)-1 {
				m.cursor++
			}

		// The "enter" key and the spacebar (a literal space) toggle
		// the selected state for the item that the cursor is pointing at.
		case "enter", " ":
			switch m.cursor {
			case newparty:
				m.party = party.CreateParty()
				m.logs += "-New-\n"
				m.step = play
			case play:
				if m.party != nil {
					m.step = play
				}
			case highscore:
				m.step = highscore
			default:
				m.step = menu
			}
		}
	}
	return m, nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch m.step {
	case menu:
		return controlMenu(msg, m)
	case highscore:
		return controlHighscore(msg, m)
	case play:
		return controlParty(msg, m)
	}

	// Return the updated model to the Bubble Tea runtime for processing.
	// Note that we're not returning a command.
	return m, nil
}

func showMenu(m model) string {
	s := "Pactoule >\n\n"

	// Iterate over our choices
	for i, choice := range m.mainMenu {

		// Is the cursor pointing at this choice?
		cursor := " " // no cursor
		if m.cursor == i {
			cursor = ">" // cursor!
		}
		if i == play && m.party == nil {
			choice = lipgloss.NewStyle().
				Foreground(lipgloss.Color("#3C3C3C")).
				Render(choice)
		}

		// Render the row
		s += fmt.Sprintf("%s %s\n", cursor, choice)
	}

	// The footer
	s += "\nPress q to quit.\n"

	// Send the UI for rendering
	return pactouleStyle.Render(s)
}

func (m model) View() string {
	switch m.step {
	default:
		return showMenu(m)
	case play:
		return showParty(m)
	case highscore:
		return showHighscore(m)
	}
}

func main() {
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
