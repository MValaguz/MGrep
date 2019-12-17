# ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
v_index = self.ui.o_lst1.selectedIndexes()[0]                    
v_item = self.lista_risultati.itemFromIndex(v_index)
v_seltext = v_item.text()                                               