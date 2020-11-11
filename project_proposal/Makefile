.Phony:: all view 

all: pdf

ps: main.tex 
	latex main.tex
	bibtex main
	latex main.tex
	latex main.tex
	dvips -q main.dvi -o main.ps
	ps2pdf main.ps draft.pdf
	#dvips -h draft.pro main.dvi -o draftmain.ps

pdf: main.tex 
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex
	#dvips -h draft.pro main.dvi -o draftmain.ps

view:
	gv main.ps &

pspdf:
	ps2pdf main.ps 
	acroread main.pdf &

clean:
	-rm -rf *~ *.bak main.ps main.pdf main.out
	-rm -rf main.aux main.blg main.bbl main.dvi main.log  
	-find . -name "*.bak" | xargs rm -rf

