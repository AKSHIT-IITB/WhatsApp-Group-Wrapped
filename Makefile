report.pdf: report.tex
	pdflatex report.tex

clean:
	rm -f *.aux *.log *.out *.toc *.pdf
