ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
	export
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
	MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
	MESSAGE
endif
HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

env: ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.sample .env


help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

db: ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up database -d --remove-orphans

dev-run: ##@Application Run dev application server in one thread
	@cd backend/ && uvicorn main:app --reload

run: ##@Application Run application server in prod stage
	@cd backend/ && gunicorn -c gunicorn_conf.py main:app