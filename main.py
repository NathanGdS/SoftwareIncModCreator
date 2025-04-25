import customtkinter as ctk
from frames import (
    SoftwareTypeFrame, SpecFeaturesFrame, SubFeaturesFrame,
    NewFeatureFrame, NewSubFeatureFrame
)
from mod_exporter import ModExporter
from tyd_importer import TydImporter

class ModCreatorApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self._setup_window()
        self._create_sidebar()
        self._create_main_area()
        self.frames = {}
        self.create_frames()
        self._create_sidebar_buttons()
        self.show_frame("Software Type")

    def _setup_window(self):
        self.root.geometry("1500x800")
        self.root.title("Software Inc. Mod Creator")
        self.root.resizable(True, True)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("red.json")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=5, pady=5)
        self.sidebar.grid_rowconfigure(99, weight=1)

        self.sidebar_label = ctk.CTkLabel(
            self.sidebar, text="🧩 Mod Sections", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(25, 10), sticky="ew")

    def _create_main_area(self):
        self.main_frame_container = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame_container.grid_rowconfigure(0, weight=1)
        self.main_frame_container.grid_columnconfigure(0, weight=1)

    def _create_sidebar_buttons(self):
        self.buttons = {
            "Import": ctk.CTkButton(
                self.sidebar,
                text="Import TYD",
                command=self.import_tyd
            ),
            "Software Type": ctk.CTkButton(
                self.sidebar, 
                text="Software Type", 
                command=lambda: self.show_frame("Software Type")
            ),
            "Spec Features": ctk.CTkButton(
                self.sidebar, 
                text="Spec Features", 
                command=lambda: self.show_frame("Spec Features"), 
                state="disabled"
            ),
            "Sub Features": ctk.CTkButton(
                self.sidebar, 
                text="Sub Features", 
                command=lambda: self.show_frame("Sub Features"), 
                state="disabled"
            ),
            "Export": ctk.CTkButton(
                self.sidebar, 
                text="Export Mod", 
                command=self.export_mod
            ),
        }

        for i, (_, button) in enumerate(self.buttons.items(), start=1):
            button.grid(row=i, column=0, padx=20, pady=5, sticky="ew")

    def create_frames(self):
        self.frames["Software Type"] = SoftwareTypeFrame(
            self.main_frame_container,
            on_next_callback=self.on_software_type_next
        )
        
        self.frames["Spec Features"] = SpecFeaturesFrame(
            self.main_frame_container,
            on_back_callback=lambda: self.show_frame("Software Type"),
            on_add_callback=lambda: self.show_frame("Add Feature"),
            on_next_callback=self.on_spec_features_next
        )
        
        self.frames["Sub Features"] = SubFeaturesFrame(
            self.main_frame_container,
            on_back_callback=lambda: self.show_frame("Spec Features"),
            on_add_callback=lambda: self.show_frame("Add Sub Feature")
        )

        self.frames["Add Feature"] = NewFeatureFrame(
            self.main_frame_container,
            on_back_callback=lambda: self.show_frame("Spec Features"),
            on_save_callback=self.save_new_feature
        )

        self.frames["Add Sub Feature"] = NewSubFeatureFrame(
            self.main_frame_container,
            on_back_callback=lambda: self.show_frame("Sub Features"),
            on_save_callback=self.save_new_sub_feature
        )

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            if name == "Add Sub Feature":
                feature_names = self.frames["Spec Features"].get_feature_names()
                self.frames["Add Sub Feature"].update_feature_options(feature_names)
            frame.tkraise()

    def on_software_type_next(self):
        self.buttons["Spec Features"].configure(state="normal")
        self.show_frame("Spec Features")

    def on_spec_features_next(self):
        self.buttons["Sub Features"].configure(state="normal")
        self.show_frame("Sub Features")

    def save_new_feature(self, data):
        entries = self.frames["Spec Features"].add_row()
        
        field_mapping = {
            "Name": 0,
            "Spec": 1,
            "Description": 2,
            "Dependencies": 3,
            "Unlock": 4,
            "DevTime": 5,
            "Submarket 1": 6,
            "Submarket 2": 7,
            "Submarket 3": 8,
            "Code Art": 9,
            "Server": 10,
            "Optional": 11,
            "Software Categories": 12
        }

        for form_field, row_index in field_mapping.items():
            if form_field in data and data[form_field]:
                if isinstance(entries[row_index], ctk.CTkOptionMenu):
                    entries[row_index].set(data[form_field])
                else:
                    entries[row_index].insert(0, data[form_field])

        self.update_sub_features_button()
        self.frames["Spec Features"].update_next_button()
        self.show_frame("Spec Features")

    def save_new_sub_feature(self, data):
        entries = self.frames["Sub Features"].add_row()
        
        field_mapping = {
            "Name": 0,
            "Description": 1,
            "Level": 2,
            "Unlock Year": 3,
            "Dev Time": 4,
            "Submarket 1": 5,
            "Submarket 2": 6,
            "Submarket 3": 7,
            "Code Art": 8,
            "Server": 9,
            "Software Categories": 10,
            "Feature": 11
        }

        for form_field, row_index in field_mapping.items():
            if form_field in data and data[form_field]:
                if isinstance(entries[row_index], ctk.CTkOptionMenu):
                    entries[row_index].set(data[form_field])
                else:
                    entries[row_index].insert(0, data[form_field])

        self.show_frame("Sub Features")

    def on_add_spec_feature(self):
        self.frames["Spec Features"].add_row()
        self.update_sub_features_button()
        self.frames["Spec Features"].update_next_button()

    def on_add_sub_feature(self):
        feature_names = self.frames["Spec Features"].get_feature_names()
        self.frames["Sub Features"].add_row(feature_names)

    def update_sub_features_button(self):
        has_features = bool(self.frames["Spec Features"].get_feature_names())
        self.buttons["Sub Features"].configure(state="normal" if has_features else "disabled")

    def export_mod(self):
        software_type_data = self.frames["Software Type"].get_data()
        spec_features = self.frames["Spec Features"].get_data()
        sub_features = self.frames["Sub Features"].get_data()
        
        ModExporter.export_mod(software_type_data, spec_features, sub_features)

    def import_tyd(self):
        result = TydImporter.import_tyd()
        if result:
            software_data, spec_features, sub_features = result
            
            # Clear existing data
            self.frames["Software Type"].clear_fields()
            self.frames["Spec Features"].feature_rows.clear()
            self.frames["Sub Features"].sub_feature_rows.clear()
            
            # Load software type data
            for field, value in software_data.items():
                if field in self.frames["Software Type"].fields:
                    widget = self.frames["Software Type"].fields[field]
                    if isinstance(widget, ctk.CTkEntry):
                        widget.insert(0, value)
                    elif isinstance(widget, ctk.CTkOptionMenu):
                        widget.set(value)
            
            # Load spec features
            for feature in spec_features:
                entries = self.frames["Spec Features"].add_row()
                # Primeiro limpa todos os campos
                self.frames["Spec Features"].clear_row_entries(entries)
                
                # Agora preenche com os dados corretos
                if feature.get("Name"):
                    entries[0].insert(0, feature["Name"])
                if feature.get("Spec"):
                    entries[1].insert(0, feature["Spec"])
                if feature.get("Description"):
                    entries[2].insert(0, feature["Description"])
                if feature.get("Dependencies"):
                    entries[3].insert(0, feature["Dependencies"])
                if feature.get("Unlock"):
                    entries[4].insert(0, feature["Unlock"])
                if feature.get("DevTime"):
                    entries[5].insert(0, feature["DevTime"])
                if feature.get("Submarket 1"):
                    entries[6].insert(0, feature["Submarket 1"])
                if feature.get("Submarket 2"):
                    entries[7].insert(0, feature["Submarket 2"])
                if feature.get("Submarket 3"):
                    entries[8].insert(0, feature["Submarket 3"])
                if feature.get("CodeArt"):
                    entries[9].set(feature["CodeArt"])
                if feature.get("Server"):
                    entries[10].set(feature["Server"])
                if feature.get("Optional"):
                    entries[11].set(feature["Optional"])
                if feature.get("Software Categories"):
                    entries[12].insert(0, feature["Software Categories"])
            
            # Load sub features
            for sub_feature in sub_features:
                entries = self.frames["Sub Features"].add_row()
                # Primeiro limpa todos os campos
                self.frames["Sub Features"].clear_row_entries(entries)
                
                # Agora preenche com os dados corretos
                field_mapping = {
                    "Name": 0,
                    "Description": 1,
                    "Level": 2,
                    "Unlock": 3,
                    "DevTime": 4,
                    "Submarket 1": 5,
                    "Submarket 2": 6,
                    "Submarket 3": 7,
                    "CodeArt": 8,
                    "Server": 9,
                    "Software Categories": 10,
                    "Feature": 11
                }
                
                for field, index in field_mapping.items():
                    value = sub_feature.get(field)
                    if value is not None:
                        if isinstance(entries[index], ctk.CTkEntry):
                            entries[index].delete(0, "end")
                            entries[index].insert(0, value)
                        elif isinstance(entries[index], ctk.CTkOptionMenu):
                            entries[index].set(str(value))
            
            # Enable buttons and show software type frame
            self.buttons["Spec Features"].configure(state="normal")
            self.buttons["Sub Features"].configure(state="normal")
            self.show_frame("Software Type")

def main():
    root = ctk.CTk()
    app = ModCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 