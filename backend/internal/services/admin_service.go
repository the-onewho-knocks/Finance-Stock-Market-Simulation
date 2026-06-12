package services

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"github.com/the-onewho-knocks/finance-Simulation/backend/internal/models"
	"github.com/the-onewho-knocks/finance-Simulation/backend/internal/repositories/interfaces"
)

type AdminService struct {
	adminRepo interfaces.AdminRepository
}

func NewAdminService(adminRepo interfaces.AdminRepository) *AdminService {
	return &AdminService{
		adminRepo: adminRepo,
	}
}

// read functions
func (s *AdminService) GetAllUsers(
	ctx context.Context,
) ([]models.User, error) {
	return s.adminRepo.GetAllUsers()
}

func (s *AdminService) GetUserPortfolio(
	ctx context.Context,
	userID uuid.UUID,
) ([]models.PortfolioItem, error) {
	return s.adminRepo.GetUserPortfolio(userID)
}

// delete a user account(admin-only prevliage)
// Admin deletes are dangerous
func (s *AdminService) DeleteUser(
	ctx context.Context,
	userID uuid.UUID,
) error {
	if userID == uuid.Nil {
		return errors.New("invalid user id")
	}
	return s.adminRepo.DeleteUser(userID)
}
