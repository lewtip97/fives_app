# Variables
PYTHON=python
SCRIPTS_DIR=scripts
MODELS_DIR=models
TEAM_STATS_DIR=team_stats
PLAYER_STATS_DIR=player_stats
HOMEPAGE_STATS_DIR=homepage

# Targets
all: help

help:
	@echo "Usage:"
	@echo "  make train_goals_model          - Train player goal models"
	@echo "  make train_goals_against_model  - Train goals against model"
	@echo "  make train_all                  - Train both models"
	@echo "  make run_app                    - Run Streamlit app"
	@echo "  make clean_models               - Remove all model files"

train_goals_model:
	$(PYTHON) generate_player_goals_model.py

train_goals_against_model:
	$(PYTHON) generate_goals_against_model.py

train_all: train_goals_model train_goals_against_model

run_app:
	streamlit run Home.py

clean_models:
	rm -f $(MODELS_DIR)/*.joblib

clean_stats_data:
	rm -r data/$(TEAM_STATS_DIR)
	rm -r data/$(PLAYER_STATS_DIR)
	rm -r data/$(HOMEPAGE_STATS_DIR)



generate_data:
	$(PYTHON) generate_homepage_data.py
	$(PYTHON) generate_player_stats_data.py
	$(PYTHON) generate_team_stats_data.py

clean: clean_models clean_stats_data 

build: train_all generate_data


