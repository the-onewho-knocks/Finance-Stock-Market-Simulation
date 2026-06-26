package routes

import (
	"github.com/go-chi/chi/v5"
	handler "github.com/the-onewho-knocks/finance-Simulation/backend/internal/handlers"
)

func RegisterResearchRoutes(r chi.Router, h *handler.ResearchHandler) {
	r.Post("/research", h.Proxy)
}
