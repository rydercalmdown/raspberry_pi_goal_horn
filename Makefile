.PHONY: install
install:
	@cd scripts && bash install.sh

.PHONY: run
run:
	@. env/bin/activate && cd src && python app.py
