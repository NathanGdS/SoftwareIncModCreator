from tkinter import filedialog, messagebox

class ModExporter:
    @staticmethod
    def to_bool(val):
        return "True" if val.lower() == "true" else "False"

    @staticmethod
    def export_mod(software_type_data, spec_features, sub_features):
        software_name = software_type_data.get("Software Name", "Unnamed Software")

        tyd = f"""SoftwareType
{{
        Name "{software_name}"
        Category "Development"
        Description "{software_type_data.get("Description", "")}"
        Iterative {software_type_data.get("(0-1)", "0")}
        OptimalDevTime {software_type_data.get("Months", "12")}
        SubmarketNames [ {software_type_data.get("Submarket Name One", "")}; {software_type_data.get("Submarket Name Two", "")}; {software_type_data.get("Submarket Name Three", "")} ]
        Popularity {software_type_data.get("Max Customer Multiplier (0-1)", "0.5")}
        Random {software_type_data.get("Sales Weight (0-1)", "0.5")}
        Retention {software_type_data.get("Retention", "12")}
        TimeScale 1
        OSSpecific {ModExporter.to_bool(software_type_data.get("True, False, or specific os eg Computer", "False"))}
        OneClient False
        InHouse {ModExporter.to_bool(software_type_data.get("In House Software", "False"))}
        IdealPrice {software_type_data.get("Price", "50")}
        NameGenerator "{software_type_data.get("File Name", "default")}"
        Features
        ["""

        for sf in spec_features:
            tyd += f"""
            {{
                Name "{sf['Name']}"
                Spec "{sf['Spec']}"
                Description "{sf['Description']}"
                Dependencies [ {sf['Dependencies']} ]
                Unlock {sf['Unlock']}
                DevTime {sf['DevTime']}
                SubmarketNames [ {sf['Submarket 1']}; {sf['Submarket 2']}; {sf['Submarket 3']} ]
                CodeArt {sf['CodeArt']}
                Server {ModExporter.to_bool(sf['Server'])}
                Optional {ModExporter.to_bool(sf['Optional'])}
                Categories [ {sf['Software Categories']} ]
                Features
                ["""
            for sub in sub_features:
                if sub['Software Feature'] == sf['Name']:
                    tyd += f"""
                    {{
                        Name "{sub['Name']}"
                        Description "{sub['Description']}"
                        Level {sub['Level']}
                        DevTime {sub['DevTime']}
                        CodeArt {sub['CodeArt']}
                        Submarkets [ {sub['Submarket 1']}; {sub['Submarket 2']}; {sub['Submarket 3']} ]
                    }}
            """
                    
        tyd += "\t]\n            }\n        ]\n}"

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