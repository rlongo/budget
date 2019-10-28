
INPUT_DIR ?= inputs
INPUTS=$(wildcard $(INPUT_DIR)/*.csv)

.PHONY: clean tracker

show: tracker
	firefox output.html &

tracker: output.html

output.html: budget.py generator.py read_inputs.py | $(INPUTS)
	python3 budget.py

clean:
	rm output.html *.png
