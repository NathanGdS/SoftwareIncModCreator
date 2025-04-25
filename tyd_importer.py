import re
from tkinter import filedialog

class TydImporter:
    @staticmethod
    def import_tyd():
        file_path = filedialog.askopenfilename(
            defaultextension=".tyd",
            filetypes=[("TYD Files", "*.tyd")],
            title="Import TYD File"
        )
        
        if not file_path:
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        print("Arquivo lido com sucesso")

        # Parse software type data
        software_data = {}
        
        # Basic fields
        software_data["Software Name"] = TydImporter._extract_value(content, "Name")
        software_data["Description"] = TydImporter._extract_value(content, "Description")
        software_data["Iterative"] = TydImporter._extract_value(content, "Iterative")
        software_data["Optimal Dev Time"] = TydImporter._extract_value(content, "OptimalDevTime")
        software_data["Popularity"] = TydImporter._extract_value(content, "Popularity")
        software_data["Random"] = TydImporter._extract_value(content, "Random")
        software_data["Retention"] = TydImporter._extract_value(content, "Retention")
        software_data["True, False, or specific os eg Computer"] = TydImporter._extract_value(content, "OSSpecific")
        software_data["In House Software"] = TydImporter._extract_value(content, "InHouse")
        software_data["Ideal Price"] = TydImporter._extract_value(content, "IdealPrice")
        software_data["File Name"] = TydImporter._extract_value(content, "NameGenerator")

        # Submarkets
        submarkets = TydImporter._extract_array(content, "SubmarketNames")
        if len(submarkets) >= 1:
            software_data["Submarket Name One"] = submarkets[0]
        if len(submarkets) >= 2:
            software_data["Submarket Name Two"] = submarkets[1]
        if len(submarkets) >= 3:
            software_data["Submarket Name Three"] = submarkets[2]

        print("\nSoftware data parsed:", software_data)

        # Find and extract the main Features array content
        features_match = re.search(r'Features\s*\[(.*)\]\s*}\s*$', content, re.DOTALL)
        if not features_match:
            print("Não encontrou o array Features principal")
            return software_data, [], []

        features_content = features_match.group(1)
        print("\nConteúdo do array Features encontrado")

        # Process features
        spec_features = []
        sub_features = []
        
        # Split the content into individual feature blocks
        feature_blocks = TydImporter._split_blocks(features_content)
        print(f"\nEncontrou {len(feature_blocks)} blocos de features")

        for block in feature_blocks:
            # Verifica se é uma feature principal (tem Name e não é uma sub-feature)
            name = TydImporter._extract_value(block, "Name")
            if not name:
                continue

            print(f"\nProcessando feature: {name}")
            print("Conteúdo do bloco:")
            print(block[:200])
            
            # Create the feature object
            feature = {
                "Name": name,
                "Spec": TydImporter._extract_value(block, "Spec"),
                "Description": TydImporter._extract_value(block, "Description"),
                "Dependencies": ", ".join(TydImporter._extract_array(block, "Dependencies")),
                "Unlock": TydImporter._extract_value(block, "Unlock"),
                "DevTime": TydImporter._extract_value(block, "DevTime"),
                "CodeArt": TydImporter._extract_value(block, "CodeArt"),
                "Server": TydImporter._extract_value(block, "Server", "False"),
                "Optional": TydImporter._extract_value(block, "Optional", "False"),
                "Software Categories": ", ".join(TydImporter._extract_array(block, "Categories"))
            }

            # Extract submarkets
            submarkets = TydImporter._extract_array(block, "Submarkets")
            if len(submarkets) >= 1:
                feature["Submarket 1"] = submarkets[0]
            if len(submarkets) >= 2:
                feature["Submarket 2"] = submarkets[1]
            if len(submarkets) >= 3:
                feature["Submarket 3"] = submarkets[2]

            spec_features.append(feature)
            print(f"Adicionou feature principal: {name}")

            # Extract sub-features array content
            sub_features_section = re.search(r'Features\s*\[(.*)\](?=\s*})', block, re.DOTALL)
            if sub_features_section:
                sub_features_content = sub_features_section.group(1)
                print(f"\nConteúdo do array de sub-features para {name}:")
                print(sub_features_content)
                
                # Encontra todos os blocos de sub-features usando a mesma lógica do _split_blocks
                sub_feature_blocks = TydImporter._split_blocks(sub_features_content)
                
                print(f"Encontrou {len(sub_feature_blocks)} sub-features para {name}")

                for sub_block in sub_feature_blocks:
                    sub_name = TydImporter._extract_value(sub_block, "Name")
                    if not sub_name:
                        continue

                    print(f"Processando sub-feature: {sub_name}")
                    print("Conteúdo do bloco da sub-feature:")
                    print(sub_block)
                    
                    sub_feature = {
                        "Name": sub_name,
                        "Description": TydImporter._extract_value(sub_block, "Description"),
                        "Level": TydImporter._extract_value(sub_block, "Level"),
                        "Unlock": TydImporter._extract_value(sub_block, "Unlock"),
                        "DevTime": TydImporter._extract_value(sub_block, "DevTime"),
                        "CodeArt": TydImporter._extract_value(sub_block, "CodeArt"),
                        "Feature": name  # Mudei de "Software Feature" para "Feature" para corresponder ao campo correto
                    }

                    # Extract submarkets
                    submarkets = TydImporter._extract_array(sub_block, "Submarkets")
                    if len(submarkets) >= 1:
                        sub_feature["Submarket 1"] = submarkets[0]
                    if len(submarkets) >= 2:
                        sub_feature["Submarket 2"] = submarkets[1]
                    if len(submarkets) >= 3:
                        sub_feature["Submarket 3"] = submarkets[2]

                    sub_features.append(sub_feature)
                    print(f"Adicionou sub-feature: {sub_name}")

        print(f"\nContagem final: {len(spec_features)} features principais, {len(sub_features)} sub-features")
        return software_data, spec_features, sub_features

    @staticmethod
    def _split_blocks(content):
        blocks = []
        depth = 0
        current_block = ""
        in_string = False
        
        for char in content:
            if char == '"' and not in_string:
                in_string = True
                current_block += char
            elif char == '"' and in_string:
                in_string = False
                current_block += char
            elif not in_string:
                if char == '{':
                    depth += 1
                    if depth == 1:
                        current_block = char
                    else:
                        current_block += char
                elif char == '}':
                    depth -= 1
                    current_block += char
                    if depth == 0:
                        blocks.append(current_block)
                        current_block = ""
                else:
                    if depth > 0:
                        current_block += char
            else:
                current_block += char
        
        return blocks

    @staticmethod
    def _extract_value(content, key, default=""):
        match = re.search(rf'{key}\s+"([^"]*)"', content) or \
                re.search(rf'{key}\s+(\S+)', content)
        return match.group(1) if match else default

    @staticmethod
    def _extract_array(content, key, alt_key=None):
        # Try primary key
        match = re.search(rf'{key}\s*\[(.*?)\]', content, re.DOTALL)
        
        # Try alternative key if provided and primary key failed
        if not match and alt_key:
            match = re.search(rf'{alt_key}\s*\[(.*?)\]', content, re.DOTALL)
        
        if match:
            values = match.group(1).strip()
            return [v.strip(' "') for v in values.split(';')] if values else []
        return [] 