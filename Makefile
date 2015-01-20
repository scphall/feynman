
MAIN=feynman_diagrams
MAINEXT=.pdf

all:
	rm -f aux/*
	pdflatex --output-directory=aux $(MAIN)
	@echo ""
	@echo " Splitting output diagrams"
	@echo " ========================="
	./split aux/$(MAIN)$(MAINEXT)
	mv aux/$(MAIN)_*$(MAINEXT) .


.PHONY : clean

clean :
	rm -f aux/* *.pdf
