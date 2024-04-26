package main

import (
	"fmt"
	"os"
	"strings"

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
	logs     []string
}

var pactouleStyle = lipgloss.NewStyle().PaddingLeft(2).PaddingTop(1).PaddingBottom(5)

func initialModel() model {
	return model{
		party: party.CreateParty(),
		scores: []highScore{
			{"Kwame", 500},
			{"Wheeler", 400},
			{"Linka", 300},
			{"Gi", 250},
			{"Ma-ti", 200},
		},
		step:   play,
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
				m.logs = append(m.logs, "-New-")
				m.step = play
			case play:
				m.logs = append(m.logs, "-Continue-")
				if m.party != nil {
					m.step = play
				}
			case highscore:
				m.logs = append(m.logs, "-High-")
				m.step = highscore
			default:
				m.logs = append(m.logs, "-M-")
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
	var view string
	switch m.step {
	default:
		view = showMenu(m)
	case play:
		view = showParty(m)
	case highscore:
		view = showHighscore(m)
	}

	logtext := strings.Join(m.logs[max(0, len(m.logs)-10):], "\n")
	logs := lipgloss.NewStyle().
		Border(lipgloss.NormalBorder()).
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("240")).
		MarginLeft(5).
		Render(
			lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("logs:\n") + logtext,
		)

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		view,
		pactouleStyle.Render(logs),
	)
}

func main() {
	p := tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
