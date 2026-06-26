package config

import (
	"log"
	"os"
	"strconv"

	"github.com/joho/godotenv"
)

type Config struct {
	DatabaseURL string
	AppPort     string

	RedisHost     string
	RedisPassword string
	RedisDB       int

	RapidAPIKey        string
	RapidAPIHost       string
	StockResearchAIURL string
}

func LoadConfig() *Config {
	// Load environment variables from .env
	_ = godotenv.Load()

	cfg := &Config{
		DatabaseURL: getEnv("DATABASE_URL", ""),
		AppPort:     getEnv("APP_PORT", "8080"),
	}

	if cfg.DatabaseURL == "" {
		log.Fatal("DATABASE_URL not found in .env file")
	}

	// Load Redis configuration
	cfg.RedisHost = getEnv("REDIS_HOST", "localhost:6379")
	cfg.RedisPassword = getEnv("REDIS_PASSWORD", "")
	cfg.RedisDB = parseInt(getEnv("REDIS_DB", "0"))

	cfg.RapidAPIKey = getEnv("RAPIDAPI_KEY", "")
	cfg.RapidAPIHost = getEnv("RAPIDAPI_HOST", "")
	cfg.StockResearchAIURL = getEnv("STOCK_RESEARCH_AI_URL", "http://localhost:8000")

	return cfg
}

func getEnv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func parseInt(s string) int {
	v, err := strconv.Atoi(s)
	if err != nil {
		return 0
	}
	return v
}
