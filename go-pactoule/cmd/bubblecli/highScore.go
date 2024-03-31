package main

import tea "github.com/charmbracelet/bubbletea"

func showHighscore(m model) string {
	return "party"
}

func controlHighscore(msg tea.Msg, m model) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "esc":
			m.step = menu
		}
	}
	return m, nil
}
