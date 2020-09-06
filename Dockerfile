FROM tiagopeixoto/graph-tool

RUN pacman -Syu python-openpyxl python-lxml python-networkx python-igraph python-colorama --noconfirm --needed
