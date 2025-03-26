import xml.etree.ElementTree as ET
import pandas as pd

def graphml_to_data_dictionary(graphml_file, output_file):
    """Converte GraphML (yEd) em dicionário de dados e salva em TXT."""
    tree = ET.parse(graphml_file)
    root = tree.getroot()
    ns = {'y': 'http://www.yworks.com/xml/graphml'}

    tables = []
    for node in root.findall('.//y:GenericNode', ns):
        table_name = node.find('.//y:NodeLabel[@configuration="com.yworks.entityRelationship.label.name"]', ns).text
        attributes_label = node.find('.//y:NodeLabel[@configuration="com.yworks.entityRelationship.label.attributes"]', ns)

        if attributes_label is not None:
            attributes_text = "".join(attributes_label.itertext())
            attributes = []
            for line in attributes_text.strip().splitlines():
                name_type = line.split(':')
                if len(name_type) == 2:
                    attr_name = name_type[0].strip()
                    attr_type = name_type[1].strip()
                    attributes.append({'Nome': attr_name, 'Tipo': attr_type})
        else:
            attributes = []

        tables.append({'Tabela': table_name, 'Atributos': attributes})

    data_dictionary = {}
    relationships = []

    for table in tables:
        data_dictionary[table['Tabela']] = table['Atributos']
        for attribute in table['Atributos']:
            if attribute['Nome'].endswith('_ID') and attribute['Nome'] != 'ID':
                related_table = attribute['Nome'].replace('_ID', '')
                if related_table in data_dictionary:
                    relationships.append({
                        'Tabela Origem': table['Tabela'],
                        'Tabela Destino': related_table,
                        'Atributo': attribute['Nome'],
                        'Relacionamento': 'Um-para-Muitos'
                    })


    with open(output_file, 'w', encoding='utf-8') as f:  # Indentação corrigida
        for table_name, attributes in data_dictionary.items(): # Indentação corrigida
            f.write(f"\nTabela: {table_name}\n") # Indentação corrigida
            df = pd.DataFrame(attributes) # Indentação corrigida
            f.write(df.to_string(index=False)) # Indentação corrigida
            f.write("\n") # Indentação corrigida

        f.write("\nRelacionamentos:\n") # Indentação corrigida
        df_relationships = pd.DataFrame(relationships) # Indentação corrigida
        f.write(df_relationships.to_string(index=False)) # Indentação corrigida



# Uso:
graphml_to_data_dictionary('SAPIENS.graphml', 'dicionario_dados.txt')  # Indentação corrigida se estiver dentro de uma função ou bloco de código.
print("Dicionário de dados salvo em dicionario_dados.txt")