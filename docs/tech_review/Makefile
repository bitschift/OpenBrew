TARGET=tech_review

default: pdf

clean: clean-doc
# Documentation

pdf: ps
	ps2pdf $(TARGET).ps

ps: dvi
	dvips $(TARGET).dvi

dvi: $(TARGET).tex
	latex $(TARGET).tex
	bibtex $(TARGET)
	latex $(TARGET).tex
	latex $(TARGET).tex

clean-doc:
	rm -f $(TARGET).aux
	rm -f $(TARGET).dvi
	rm -f $(TARGET).log
	rm -f $(TARGET).out
	rm -f $(TARGET).ps
	rm -f $(TARGET).toc
	rm -f $(TARGET).bbl
	rm -f $(TARGET).blg


