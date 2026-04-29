all:
	pdflatex report.tex
	pdflatex report.tex

clean:
	rm -f report.aux report.log report.out report.toc

cleanall: clean
	rm -f report.pdf