package routes

import (
	"github.com/go-chi/chi/v5"

	handler "github.com/the-onewho-knocks/finance-Simulation/backend/internal/handlers"
)

type Handlers struct {
	Auth           *handler.AuthHandler
	User           *handler.UserHandler
	Admin          *handler.AdminHandler
	Portfolio      *handler.PortfolioHandler
	Transaction    *handler.TransactionHandler
	Market         *handler.MarketHandler
	Expense        *handler.ExpenseHandler
	PlannedExpense *handler.PlannedExpenseHandler
	Networth       *handler.NetworthHandler
	Heatmap        *handler.HeatmapHandler
	Dashboard      *handler.DashboardHandler
	Research *handler.ResearchHandler 

}

func RegisterRoutes(h *Handlers) chi.Router {
	r := chi.NewRouter()

	// =========================
	// Public routes
	// =========================
	RegisterAuthRoutes(r, h.Auth)

	// =========================
	// App routes
	// =========================
	RegisterUserRoutes(r, h.User)
	RegisterAdminRoutes(r, h.Admin)
	RegisterPortfolioRoutes(r, h.Portfolio)
	RegisterTransactionRoutes(r, h.Transaction)
	RegisterExpenseRoutes(r, h.Expense)
	RegisterPlannedExpenseRoutes(r, h.PlannedExpense)
	RegisterNetworthRoutes(r, h.Networth)
	RegisterMarketRoutes(r, h.Market)
	RegisterHeatmapRoutes(r, h.Heatmap)
	RegisterDashboardRoutes(r, h.Dashboard)
	RegisterResearchRoutes(r, h.Research)

	return r
}
