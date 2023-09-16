def converter(input_notebook_file):
    """This function automates the process of converting Jupyter Notebook files (.ipynb) to plain text files (.txt)
    by extracting only the code portions.

    Args:
        input_notebook_file (str, optional): A str with the name of the Jupyter Notebook file 
        (including the file extension .ipynb) that you want to convert to plain text.
    """
    
    import nbformat as nbf
    import os
    import traceback
    
    if '.ipynb' not in input_notebook_file:
            input_notebook_file = input_notebook_file + '.ipynb'
    
    output_text_file = input_notebook_file.split('.')[0] + '.txt'

    try:
        ntbk = nbf.read(input_notebook_file, nbf.NO_CONVERT)
        new_ntbk = ntbk
        new_ntbk.cells = [cell for cell in ntbk.cells if cell.cell_type != "markdown"]
        nbf.write(new_ntbk, output_text_file, version=nbf.NO_CONVERT)
        lines = [cell['source'] + '\n\n\n' for cell in new_ntbk['cells']]
        with open(os.path.join('.', output_text_file), 'w', encoding='utf-8') as file:
            file.writelines(lines)
    except:
        traceback.print_exc()
    
def converter_2(input_notebook_file):
    """ This function automates the process of converting Jupyter Notebook files (.ipynb) to plain text files (.txt)
        by extracting only the code portions.

        Args:
            input_notebook_file (str, optional): A str with the name of the Jupyter Notebook file 
            (including the file extension .ipynb) that you want to convert to plain text.
    """
    
    import os
    import json
    
    if '.ipynb' not in input_notebook_file:
            input_notebook_file = input_notebook_file + '.ipynb'
    
    output_text_file = input_notebook_file.split('.')[0] + '.txt'
    
    temp_text_file = output_text_file.split('.')[0] + ".json"
    src = os.path.join('.',input_notebook_file)
    dst = os.path.join('.',temp_text_file)
        
    if os.name == 'nt':  # Windows
        cmd = f'copy "{src}" "{dst}"'
    else:  # Unix/Linux
        cmd = f'cp "{src}" "{dst}"'
    try:    
        os.system(cmd)
            
        with open(dst, "r", encoding="utf-8") as file:
            file_load = json.load(file)
            file_cells = file_load['cells']
            txt_file = []
            for cell in file_cells:
                if cell['cell_type'] != 'markdown':
                    for index, source in enumerate(cell['source']):
                        txt_file.append(source)
                        if index == len(cell['source'])-1:
                            txt_file.append('\n\n\n\n')
                
                
        with open(output_text_file, "w", encoding="utf-8") as file:
            file.writelines(txt_file)
        
        if os.name == 'nt':  # Windows
            cmd = f'del "{dst}"'
        else:  # Unix/Linux
            cmd = f'rm "{dst}"'
        
        os.system(cmd)
    except:
        print('Los argumentos no son validos.')