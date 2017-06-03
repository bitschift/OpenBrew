TARGET=tech_review
TEX=/usr/local/apps/tex_live/current/bin/x86_64-linux/latex

default: pdf

clean: clean-doc
# Documentation

pdf: ps
	ps2pdf $(TARGET).ps

ps: dvi
	dvips $(TARGET).dvi

dvi: $(TARGET).tex
	$(TEX) $(TARGET).tex
	bibtex $(TARGET)
	$(TEX) $(TARGET).tex
	$(TEX) $(TARGET).tex

clean-doc:
	rm -f $(TARGET).aux
	rm -f $(TARGET).dvi
	rm -f $(TARGET).log
	rm -f $(TARGET).out
	rm -f $(TARGET).ps
	rm -f $(TARGET).toc
	rm -f $(TARGET).bbl
	rm -f $(TARGET).blg


