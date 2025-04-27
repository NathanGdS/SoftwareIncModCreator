from tkinter import filedialog, messagebox

class ModExporter:
    @staticmethod
    def to_bool(val):
        return "True" if val.lower() == "true" else "False"

    @staticmethod
    def _add_field_if_exists(data, key, default="", bool_field=False):
        value = data.get(key, default)
        if value and value != default:
            if bool_field:
                return f"\n    {key} {ModExporter.to_bool(value)}"
            return f'\n    {key} "{value}"'
        return ""

    @staticmethod
    def _add_array_if_exists(data, key, fields):
        values = [data.get(field, "") for field in fields]
        if any(values):
            values_str = "; ".join(str(val) for val in values if val)
            if values_str:
                return f"\n    {key} [ {values_str} ]"
        return ""

    @staticmethod
    def export_mod_to_string(software_type_data, spec_features, sub_features):
        """Export mod data to a string without saving to file (for testing)"""
        software_name = software_type_data.get("Software Name", "Unnamed Software")

        tyd = f"""SoftwareType
{{
    Name "{software_name}"
    Category "Development\""""

        # Add optional software type fields
        tyd += ModExporter._add_field_if_exists(software_type_data, "Description")
        tyd += ModExporter._add_field_if_exists(software_type_data, "Iterative", "0")
        tyd += ModExporter._add_field_if_exists(software_type_data, "OptimalDevTime", "12")
        
        # Add submarkets if they exist
        submarkets = ModExporter._add_array_if_exists(
            software_type_data,
            "SubmarketNames",
            ["Submarket Name One", "Submarket Name Two", "Submarket Name Three"]
        )
        if submarkets:
            tyd += submarkets

        tyd += ModExporter._add_field_if_exists(software_type_data, "Popularity", "0.5")
        tyd += ModExporter._add_field_if_exists(software_type_data, "Random", "0.5")
        tyd += ModExporter._add_field_if_exists(software_type_data, "Retention", "12")
        tyd += "\n    TimeScale 1"
        tyd += ModExporter._add_field_if_exists(software_type_data, "OSSpecific", "False", bool_field=True)
        tyd += "\n    OneClient False"
        tyd += ModExporter._add_field_if_exists(software_type_data, "InHouse", "False", bool_field=True)
        tyd += ModExporter._add_field_if_exists(software_type_data, "IdealPrice", "50")
        tyd += ModExporter._add_field_if_exists(software_type_data, "NameGenerator", "default")
        tyd += "\n    Features\n    ["

        for sf in spec_features:
            if not sf['Name']:  # Skip if no name
                continue

            tyd += "\n        {"
            tyd += f'\n            Name "{sf["Name"]}"'
            
            if sf['Spec']:
                tyd += f'\n            Spec "{sf["Spec"]}"'
            if sf['Description']:
                tyd += f'\n            Description "{sf["Description"]}"'
            if sf['Dependencies']:
                tyd += f'\n            Dependencies [ {sf["Dependencies"]} ]'
            if sf['Unlock']:
                tyd += f'\n            Unlock {sf["Unlock"]}'
            if sf['DevTime']:
                tyd += f'\n            DevTime {sf["DevTime"]}'
            
            # Add submarkets if any exists
            submarkets = [sf.get('Submarket 1', ''), sf.get('Submarket 2', ''), sf.get('Submarket 3', '')]
            if any(submarkets):
                submarkets_str = "; ".join(str(s) for s in submarkets if s)
                tyd += f'\n            SubmarketNames [ {submarkets_str} ]'
            
            if sf.get('CodeArt'):
                tyd += f'\n            CodeArt {sf["CodeArt"]}'
            if sf.get('Server') and sf['Server'].lower() != 'false':
                tyd += f'\n            Server {ModExporter.to_bool(sf["Server"])}'
            if sf.get('Optional') and sf['Optional'].lower() != 'false':
                tyd += f'\n            Optional {ModExporter.to_bool(sf["Optional"])}'
            if sf.get('Software Categories'):
                tyd += f'\n            Categories [ {sf["Software Categories"]} ]'

            # Add sub-features
            tyd += "\n            Features\n            ["
            
            for sub in sub_features:
                if sub.get('Software Feature') == sf['Name'] and sub.get('Name'):
                    tyd += "\n                {"
                    tyd += f'\n                    Name "{sub["Name"]}"'
                    
                    if sub.get('Description'):
                        tyd += f'\n                    Description "{sub["Description"]}"'
                    if sub.get('Level'):
                        tyd += f'\n                    Level {sub["Level"]}'
                    if sub.get('DevTime'):
                        tyd += f'\n                    DevTime {sub["DevTime"]}'
                    if sub.get('CodeArt'):
                        tyd += f'\n                    CodeArt {sub["CodeArt"]}'
                    
                    # Add submarkets if any exists
                    submarkets = [sub.get('Submarket 1', ''), sub.get('Submarket 2', ''), sub.get('Submarket 3', '')]
                    if any(submarkets):
                        submarkets_str = "; ".join(str(s) for s in submarkets if s)
                        tyd += f'\n                    Submarkets [ {submarkets_str} ]'
                    
                    tyd += "\n                }"
            
            tyd += "\n            ]"  # Close Features array
            tyd += "\n        }"  # Close feature object

        tyd += "\n    ]\n}"  # Close main Features array and SoftwareType
        return tyd

    @staticmethod
    def export_mod(software_type_data, spec_features, sub_features):
        """Export mod data to a file"""
        tyd = ModExporter.export_mod_to_string(software_type_data, spec_features, sub_features)
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tyd",
            filetypes=[("TYD Files", "*.tyd")],
            title="Save your Mod File"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(tyd)
            messagebox.showinfo("Export Successful", f"Mod file saved to:\n{file_path}")
            return True
        return False 