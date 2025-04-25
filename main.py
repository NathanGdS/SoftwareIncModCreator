import json
from tkinter import filedialog
import customtkinter as ctk
 
class ModCreatorApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self._setup_window()
        self._create_sidebar()
        self._create_main_area()

        self.frames = {}
        self.sub_feature_dropdowns = []
        self.spec_feature_rows = []
        self.sub_feature_rows = []
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
            "Software Type": ctk.CTkButton(self.sidebar, text="Software Type", command=lambda: self.show_frame("Software Type")),
            "Spec Features": ctk.CTkButton(self.sidebar, text="Spec Features", command=lambda: self.show_frame("Spec Features"), state="disabled"),
            "Sub Features": ctk.CTkButton(self.sidebar, text="Sub Features", command=lambda: self.show_frame("Sub Features"), state="disabled"),
            "Export": ctk.CTkButton(self.sidebar, text="Export Mod", command=self.export_mod),
        }

        for i, (_, button) in enumerate(self.buttons.items(), start=1):
            button.grid(row=i, column=0, padx=20, pady=5, sticky="ew")

    def create_frames(self):
        self.frames["Software Type"] = self.create_input_frame("Software Type", {
            "Software Name": "Software Name",
            "Description": "Description",
            "Unlock Year": "Year",
            "Random": "Sales Weight (0-1)",
            "Ideal Price": "Price",
            "Optimal Dev Time": "Months",
            "Popularity": "Max Customer Multiplier (0-1)",
            "Retention": "Months",
            "Iterative": "(0-1)",
            "OS Supports": "True, False, or specific os eg Computer",
            "Contract Software": "True False",
            "In House Software": "True False",
            "Name Generator": "File Name",
            "Submarket Name One": "",
            "Submarket Name Two": "",
            "Submarket Name Three": ""
        })
        self.frames["Add Sub Feature"] = self.create_new_sub_feature_frame()
        self.frames["Add Feature"] = self.create_new_feature_frame()
        self.frames["Spec Features"] = self.create_spec_features_frame()
        self.frames["Sub Features"] = self.create_sub_features_frame()

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def create_input_frame(self, title, fields):
        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Frame scrollable para conteúdo
        content_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        content_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(1, weight=1)

        # Título
        title_label = ctk.CTkLabel(content_frame, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dicionário para armazenar as referências dos campos e mensagens de erro
        self.software_type_fields = {}
        self.error_labels = {}

        # Lista de campos que devem ser option boxes True/False
        boolean_fields = ["OS Supports", "Contract Software", "In House Software"]

        # Criar campos
        for i, (label_text, entry_placeholder) in enumerate(fields.items(), start=1):
            # Label do campo
            ctk.CTkLabel(content_frame, text=f"{label_text}:", anchor="e", font=ctk.CTkFont(size=14)).grid(
                row=i*2-1, column=0, padx=(0, 15), pady=5, sticky="e"
            )
            
            # Campo de entrada
            if label_text in boolean_fields:
                entry = ctk.CTkOptionMenu(content_frame, values=["True", "False"], width=300)
                entry.grid(row=i*2-1, column=1, pady=5, sticky="ew")
                entry.set("False")  # Valor padrão
            else:
                entry = ctk.CTkEntry(content_frame, placeholder_text=entry_placeholder, width=300)
                entry.grid(row=i*2-1, column=1, pady=5, sticky="ew")
            
            self.software_type_fields[label_text] = entry
            
            # Label de erro
            error_label = ctk.CTkLabel(content_frame, text="", text_color="#FF4444", font=ctk.CTkFont(size=12))
            error_label.grid(row=i*2, column=1, sticky="w")
            self.error_labels[label_text] = error_label
            
            # Evento de validação (apenas para campos de texto)
            if isinstance(entry, ctk.CTkEntry):
                entry.bind("<KeyRelease>", lambda e, lbl=label_text: self.validate_field(lbl))

        # Frame para botões no final (fora do scrollable frame)
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="e", padx=20, pady=(0, 20))

        # Botão Next
        next_btn = ctk.CTkButton(button_frame, text="Next", width=100, command=self.validate_and_proceed)
        next_btn.pack(pady=10)

        return frame

    def validate_field(self, field_label):
        """Valida um campo específico e atualiza sua mensagem de erro"""
        # Campos que não são obrigatórios
        optional_fields = ["Unlock Year", "Name Generator"]
        
        widget = self.software_type_fields[field_label]
        error_label = self.error_labels[field_label]
        
        if field_label not in optional_fields and not widget.get().strip():
            error_label.configure(text="This field is required")
        else:
            error_label.configure(text="")

    def create_select_field(self, frame: ctk.CTkFrame, labelTx, select_values, index):
        ctk.CTkLabel(frame, text=f"{labelTx}:", anchor="e", font=ctk.CTkFont(size=14)).grid(
            row=index, column=0, padx=15, pady=5, sticky="e"
        )
        entry = ctk.CTkOptionMenu(frame, values=select_values, width=120)
        entry.grid(row=index, column=1, padx=10, pady=5, sticky="ew")

    def create_btn(self, frame: ctk.CTkFrame, btnTx, index, cmd):
        entry = ctk.CTkButton(frame, text=btnTx, width=30, command=cmd)
        entry.grid(row=index, column=1, padx=10, pady=5, sticky="ew")


    def create_spec_features_frame(self):
        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # Título
        ctk.CTkLabel(frame, text="Spec Features", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(20, 10))

        # Container para o scrollable frame
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=20)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Frame scrollable para a tabela (com tamanho fixo)
        self.spec_feature_scroll_frame = ctk.CTkScrollableFrame(container, width=1200, height=500)
        self.spec_feature_scroll_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar colunas no scrollable frame
        for i in range(13):  # 13 colunas
            self.spec_feature_scroll_frame.grid_columnconfigure(i, weight=1)

        # Frame para os botões (fora do scrollable frame)
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        # Frame para botão de adicionar (à esquerda)
        add_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        add_button_frame.pack(side="left")
        
        # Frame para botões à direita
        right_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_button_frame.pack(side="right")
        
        # Botão de adicionar
        ctk.CTkButton(add_button_frame, text="+", width=30, command=lambda: self.show_frame("Add Feature")).pack(side="left")
        
        # Botão Add Sub Features (desabilitado inicialmente)
        self.add_sub_features_btn = ctk.CTkButton(
            right_button_frame, 
            text="Add Sub Features", 
            width=120, 
            command=lambda: self.show_frame("Sub Features"),
            state="disabled"
        )
        self.add_sub_features_btn.pack(side="right", padx=(5, 0))
        
        # Botão de voltar
        ctk.CTkButton(right_button_frame, text="Back", width=100, command=lambda: self.show_frame("Software Type")).pack(side="right", padx=5)

        return frame

    def create_sub_features_frame(self):
        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)
        ctk.CTkLabel(frame, text="Sub Features", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        # Scrollable frame que vai conter headers e linhas
        self.sub_feature_scroll_frame = ctk.CTkScrollableFrame(frame, orientation="horizontal", width=1200, height=300)
        self.sub_feature_scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Cabeçalhos diretamente no grid da scroll_frame
        headers = [
            "Name", "Description", "Level", "Unlock Year", "Dev Time",
            "Submarket 1", "Submarket 2", "Submarket 3",
            "Code Art", "Server", "Software Categories", "Software Feature"
        ]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(self.sub_feature_scroll_frame, text=text, font=ctk.CTkFont(size=12, weight="bold"), anchor="w", width=120)
            label.grid(row=0, column=col, padx=5, pady=(5, 10), sticky="w")

        # Frame para os botões
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))

        # Frame para botão de adicionar (à esquerda)
        add_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        add_button_frame.pack(side="left")
        
        # Frame para botão de voltar (à direita)
        back_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        back_button_frame.pack(side="right")

        # Botão de adicionar
        ctk.CTkButton(add_button_frame, text="+", width=30, command=lambda: self.show_frame("Add Sub Feature")).pack(side="left")
        
        # Botão de voltar
        ctk.CTkButton(back_button_frame, text="Back", width=100, command=lambda: self.show_frame("Spec Features")).pack(side="right")

        return frame

    def create_new_sub_feature_frame(self):
        labels = {
            "Name": "Sub feature name",
            "Description": "Description",
            "Level": "",
            "Unlock Year": "Year of Unlock",
            "Dev Time": "",
            "Code Art": "",
            "Submarket 1": "",
            "Submarket 2": "",
            "Submarket 3": "",
            "Feature": ""
        }

        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)

        title_label = ctk.CTkLabel(frame, text="Sub Feature", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Dicionário para armazenar as referências dos campos e mensagens de erro
        self.sub_feature_fields = {}
        self.sub_feature_error_labels = {}

        for i, (label_text, entry_placeholder) in enumerate(labels.items(), start=1):
            # Criar o label do campo
            ctk.CTkLabel(frame, text=f"{label_text}:", anchor="e", font=ctk.CTkFont(size=14)).grid(
                row=i*2-1, column=0, padx=15, pady=5, sticky="e"
            )
            
            if label_text == "Level":
                entry = ctk.CTkOptionMenu(frame, values=["1", "2"], width=300)
                entry.grid(row=i*2-1, column=1, padx=10, pady=5, sticky="ew")
            elif label_text == "Dev Time" or label_text == "Code Art":
                entry = ctk.CTkOptionMenu(frame, values=["1", "2", "3", "4", "5"], width=300)
                entry.grid(row=i*2-1, column=1, padx=10, pady=5, sticky="ew")
            elif label_text.find("Submarket") != -1:
                entry = ctk.CTkOptionMenu(frame, values=["1", "2", "3", "4", "5"], width=300)
                entry.grid(row=i*2-1, column=1, padx=10, pady=5, sticky="ew")
            elif label_text == "Feature":
                # Inicializar com lista vazia se ainda não houver features
                feature_names = []
                if hasattr(self, 'spec_feature_rows'):
                    feature_names = [row[0].get() for row in self.spec_feature_rows if row[0].get().strip()]
                entry = ctk.CTkOptionMenu(frame, values=feature_names if feature_names else [""], width=300)
                entry.grid(row=i*2-1, column=1, padx=10, pady=5, sticky="ew")
            else:
                entry = ctk.CTkEntry(frame, placeholder_text=entry_placeholder, width=300)
                entry.grid(row=i*2-1, column=1, padx=10, pady=5, sticky="ew")
            
            self.sub_feature_fields[label_text] = entry
            
            # Criar label de erro (inicialmente vazio)
            error_label = ctk.CTkLabel(frame, text="", text_color="#FF4444", font=ctk.CTkFont(size=12))
            error_label.grid(row=i*2, column=1, sticky="w", padx=10)
            self.sub_feature_error_labels[label_text] = error_label
            
            # Bind do evento de digitação para validar o campo (apenas para campos de texto)
            if isinstance(entry, ctk.CTkEntry):
                entry.bind("<KeyRelease>", lambda e, lbl=label_text: self.validate_sub_feature_field(lbl))

        # Criar um frame para os botões
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=len(labels)*2+1, column=1, pady=20, sticky="e")
        
        # Botão Back
        back_btn = ctk.CTkButton(button_frame, text="Back", width=100, command=lambda: self.show_frame("Sub Features"))
        back_btn.pack(side="left", padx=5)
        
        # Botão Save
        save_btn = ctk.CTkButton(button_frame, text="Save", width=100, command=self.save_new_sub_feature)
        save_btn.pack(side="left", padx=5)

        frame.grid_columnconfigure(1, weight=1)
        return frame

    def validate_sub_feature_field(self, field_label):
        """Valida um campo específico do formulário de sub-feature e atualiza sua mensagem de erro"""
        widget = self.sub_feature_fields[field_label]
        error_label = self.sub_feature_error_labels[field_label]
        
        if isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
            error_label.configure(text="This field is required")
        else:
            error_label.configure(text="")

    def add_sub_feature_row(self, start_row=None):
        if start_row is None:
            start_row = len(self.sub_feature_rows) + 1  # +1 por causa dos headers

        row_index = len(self.sub_feature_rows)
        labels = [
            "Name", "Description", "Level", "Unlock", "Dev Time",
            "Submarket 1", "Submarket 2", "Submarket 3", "Code Art", "Server", "Software Categories", "Software Feature"
        ]
        # self.sub_feature_rows.append(labels)
        entries = []

        for col, label in enumerate(labels):
            if label == "Level":
                entry = ctk.CTkOptionMenu(self.sub_feature_scroll_frame, values=["1", "2"], width=120)
            elif label == "Software Feature":
                entry = ctk.CTkOptionMenu(self.sub_feature_scroll_frame, values=[""], width=120)
                self.sub_feature_dropdowns.append(entry)
            else:
                entry = ctk.CTkEntry(self.sub_feature_scroll_frame, placeholder_text=label, width=120)

            entry.grid(row=row_index, column=col, padx=5, pady=2)
            entries.append(entry)

        self.sub_feature_rows.append(entries)
        self.update_sub_feature_dropdowns()

    def update_sub_feature_dropdowns(self):
        feature_names = [row[0].get() for row in self.spec_feature_rows if row[0].get().strip()]
        for dropdown in self.sub_feature_dropdowns:
            # print("drodown on sub feature:")
            # print(feature_names)
            dropdown.configure(values=feature_names or [""])

    def create_export_frame(self):
        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)
        ctk.CTkLabel(frame, text="Export Mod", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30)
        ctk.CTkButton(frame, text="Export to File", command=self.export_mod).pack(pady=10)
        return frame

    def export_mod(self):
        from tkinter import messagebox

        # --- Software Type ---
        type_entries = self.frames["Software Type"].winfo_children()
        type_data = {}
        for entry in type_entries:
            if isinstance(entry, ctk.CTkEntry):
                label = entry.cget("placeholder_text")
                value = entry.get()
                type_data[label] = value

        software_name = type_data.get("Software Name", "Unnamed Software")

        # --- Spec Features ---
        spec_features = []
        for row in self.spec_feature_rows:
            if not any(entry.get().strip() for entry in row):
                continue  # ignora linhas vazias
            spec_features.append({
                "Name": row[0].get(),
                "Spec": row[1].get(),
                "Description": row[2].get(),
                "Dependencies": row[3].get(),
                "Unlock": row[4].get(),
                "DevTime": row[5].get(),
                "Submarket 1": row[6].get(),
                "Submarket 2": row[7].get(),
                "Submarket 3": row[8].get(),
                "CodeArt": row[9].get(),
                "Server": row[10].get(),
                "Optional": row[11].get(),
                "Software Categories": row[12].get()
            })

        # --- Sub Features ---
        sub_features = []
        for row in self.sub_feature_rows:
            if not any(entry.get().strip() for entry in row):
                continue  # ignora linhas vazias
            sub_features.append({
                "Name": row[0].get(),
                "Description": row[1].get(),
                "Level": row[2].get(),
                "Unlock": row[3].get(),
                "DevTime": row[4].get(),
                "Submarket 1": row[5].get(),
                "Submarket 2": row[6].get(),
                "Submarket 3": row[7].get(),
                "CodeArt": row[8].get(),
                "Server": row[9].get(),
                "Software Categories": row[10].get(),
                "Software Feature": row[11].get()
            })

        # --- Monta string TYD ---
        def to_bool(val): return "True" if val.lower() == "true" else "False"

        tyd = f"""SoftwareType
{{
        Name "{software_name}"
        Category "Development"
        Description "{type_data.get("Description", "")}"
        Iterative {type_data.get("(0-1)", "0")}
        OptimalDevTime {type_data.get("Months", "12")}
        SubmarketNames [ {type_data.get("Submarket Name One", "")}; {type_data.get("Submarket Name Two", "")}; {type_data.get("Submarket Name Three", "")} ]
        Popularity {type_data.get("Max Customer Multiplier (0-1)", "0.5")}
        Random {type_data.get("Sales Weight (0-1)", "0.5")}
        Retention {type_data.get("Retention", "12")}
        TimeScale 1
        OSSpecific {to_bool(type_data.get("True, False, or specific os eg Computer", "False"))}
        OneClient False
        InHouse {to_bool(type_data.get("In House Software", "False"))}
        IdealPrice {type_data.get("Price", "50")}
        NameGenerator "{type_data.get("File Name", "default")}"
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
                Server {to_bool(sf['Server'])}
                Optional {to_bool(sf['Optional'])}
                Categories [ {sf['Software Categories']} ]
                Features
                ["""
            for sub in sub_features:
                print(sub)
                if (sub['Software Feature'] == sf['Name']):
                    print("found")
                    print(sub)
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

        # --- Salvar o arquivo ---
        file_path = filedialog.asksaveasfilename(
            defaultextension=".tyd",
            filetypes=[("TYD Files", "*.tyd")],
            title="Save your Mod File"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(tyd)
            messagebox.showinfo("Export Successful", f"Mod file saved to:\n{file_path}")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def save_new_sub_feature(self):
        # Verificar se todos os campos foram preenchidos
        has_errors = False
        first_error_field = None
        
        # Validar todos os campos
        for label, widget in self.sub_feature_fields.items():
            if isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
                self.sub_feature_error_labels[label].configure(text="This field is required")
                if not first_error_field:
                    first_error_field = widget
                has_errors = True

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        # Coletar dados do formulário
        entries = {}
        for label, widget in self.sub_feature_fields.items():
            if isinstance(widget, ctk.CTkEntry):
                entries[label] = widget.get()
            else:  # CTkOptionMenu
                entries[label] = widget.get()

        # Adicionar nova linha na listagem de sub-features
        self.add_sub_feature_row()
        row = self.sub_feature_rows[-1]  # Pega a última linha adicionada
        
        # Mapear os valores nos campos corretos
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
            "Feature": 11
        }

        # Preencher os campos da nova linha
        for form_field, row_index in field_mapping.items():
            if form_field in entries and entries[form_field]:
                if isinstance(row[row_index], ctk.CTkOptionMenu):
                    row[row_index].set(entries[form_field])
                else:
                    row[row_index].insert(0, entries[form_field])

        # Limpar os campos do formulário
        for widget in self.sub_feature_fields.values():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget.cget("values")[0])

        # Voltar para a tela de Sub Features
        self.show_frame("Sub Features")

    def update_feature_select(self):
        # Verificar se o frame existe antes de tentar atualizá-lo
        if "Add Sub Feature" not in self.frames:
            return

        # Encontrar o select de Feature no frame Add Sub Feature
        feature_select = None
        for widget in self.frames["Add Sub Feature"].winfo_children():
            if isinstance(widget, ctk.CTkOptionMenu):
                # Encontra o label associado
                grid_info = widget.grid_info()
                for w in self.frames["Add Sub Feature"].winfo_children():
                    if isinstance(w, ctk.CTkLabel):
                        if w.grid_info()["row"] == grid_info["row"] and w.cget("text").replace(":", "") == "Feature":
                            feature_select = widget
                            break
                if feature_select:
                    break

        if feature_select:
            # Atualizar as opções com as features existentes
            feature_names = [row[0].get() for row in self.spec_feature_rows if row[0].get().strip()]
            feature_select.configure(values=feature_names if feature_names else [""])
            if feature_names:
                feature_select.set(feature_names[0])

    def update_dropdowns(self):
        self.update_sub_feature_dropdowns()
        self.update_feature_select()

    def create_new_feature_frame(self):
        labels = {
            "Name": "Feature name",
            "Spec": "Feature specification",
            "Description": "Description",
            "Dependencies": "Dependencies",
            "Unlock": "Unlock year",
            "DevTime": "Development time in months",
            "Submarket 1": "",
            "Submarket 2": "",
            "Submarket 3": "",
            "Code Art": "",
            "Server": "True/False",
            "Optional": "True/False",
            "Software Categories": "Categories"
        }

        frame = ctk.CTkFrame(self.main_frame_container, corner_radius=15)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # Título
        title_label = ctk.CTkLabel(frame, text="New Feature", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Frame scrollable para o conteúdo
        content_frame = ctk.CTkScrollableFrame(frame, width=800, height=500)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content_frame.grid_columnconfigure(1, weight=1)

        # Dicionário para armazenar as referências dos campos e mensagens de erro
        self.feature_fields = {}
        self.feature_error_labels = {}

        for i, (label_text, entry_placeholder) in enumerate(labels.items(), start=0):
            # Label do campo
            ctk.CTkLabel(content_frame, text=f"{label_text}:", anchor="e", font=ctk.CTkFont(size=14)).grid(
                row=i*2, column=0, padx=(0, 15), pady=5, sticky="e"
            )
            
            # Campo de entrada
            if label_text == "Code Art":
                entry = ctk.CTkOptionMenu(content_frame, values=["1", "2", "3", "4", "5"], width=300)
                entry.set("1")  # Valor padrão
            elif label_text.find("Submarket") != -1:
                entry = ctk.CTkOptionMenu(content_frame, values=["1", "2", "3", "4", "5"], width=300)
                entry.set("1")  # Valor padrão
            elif label_text in ["Server", "Optional"]:
                entry = ctk.CTkOptionMenu(content_frame, values=["True", "False"], width=300)
                entry.set("False")  # Valor padrão
            else:
                entry = ctk.CTkEntry(content_frame, placeholder_text=entry_placeholder, width=300)
            
            entry.grid(row=i*2, column=1, pady=5, sticky="ew")
            self.feature_fields[label_text] = entry
            
            # Label de erro
            error_label = ctk.CTkLabel(content_frame, text="", text_color="#FF4444", font=ctk.CTkFont(size=12))
            error_label.grid(row=i*2+1, column=1, sticky="w", padx=10)
            self.feature_error_labels[label_text] = error_label
            
            # Evento de validação (apenas para campos de texto)
            if isinstance(entry, ctk.CTkEntry):
                entry.bind("<KeyRelease>", lambda e, lbl=label_text: self.validate_feature_field(lbl))

        # Frame para os botões (fora do scrollable frame)
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(0, 20), sticky="e", padx=20)
        
        # Botão Back
        back_btn = ctk.CTkButton(button_frame, text="Back", width=100, command=lambda: self.show_frame("Spec Features"))
        back_btn.pack(side="left", padx=5)
        
        # Botão Save
        save_btn = ctk.CTkButton(button_frame, text="Save", width=100, command=self.save_new_feature)
        save_btn.pack(side="left", padx=5)

        return frame

    def validate_feature_field(self, field_label):
        """Valida um campo específico do formulário de feature e atualiza sua mensagem de erro"""
        # Campos que não são obrigatórios
        optional_fields = ["Unlock", "Software Categories"]
        
        widget = self.feature_fields[field_label]
        error_label = self.feature_error_labels[field_label]
        
        if field_label not in optional_fields and isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
            error_label.configure(text="This field is required")
        else:
            error_label.configure(text="")

    def save_new_feature(self):
        # Verificar se todos os campos foram preenchidos
        has_errors = False
        first_error_field = None
        
        # Campos que não são obrigatórios
        optional_fields = ["Unlock", "Software Categories"]
        
        # Validar todos os campos
        for label, widget in self.feature_fields.items():
            if label not in optional_fields and isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
                self.feature_error_labels[label].configure(text="This field is required")
                if not first_error_field:
                    first_error_field = widget
                has_errors = True

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        # Coletar dados do formulário
        entries = {}
        for label, widget in self.feature_fields.items():
            if isinstance(widget, ctk.CTkEntry):
                entries[label] = widget.get()
            else:  # CTkOptionMenu
                entries[label] = widget.get()

        # Adicionar nova linha na listagem de features
        self.add_spec_feature_row()
        row = self.spec_feature_rows[-1]  # Pega a última linha adicionada
        
        # Mapear os valores nos campos corretos
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

        # Preencher os campos da nova linha
        for form_field, row_index in field_mapping.items():
            if form_field in entries and entries[form_field]:
                if isinstance(row[row_index], ctk.CTkOptionMenu):
                    row[row_index].set(entries[form_field])
                else:
                    row[row_index].insert(0, entries[form_field])

        # Limpar os campos do formulário
        for widget in self.feature_fields.values():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget.cget("values")[0])

        # Atualizar os dropdowns que dependem das features
        self.update_dropdowns()
        
        # Habilitar o botão Add Sub Features se houver pelo menos uma feature
        if hasattr(self, 'add_sub_features_btn'):
            self.add_sub_features_btn.configure(state="normal")
        
        # Atualizar o estado do botão Sub Features
        self.update_sub_features_button()

        # Voltar para a tela de Spec Features
        self.show_frame("Spec Features")

    def add_spec_feature_row(self):
        row_index = len(self.spec_feature_rows)
        
        # Se é a primeira linha, adiciona os cabeçalhos
        if row_index == 0:
            headers = [
                "Name", "Spec", "Description", "Dependencies", "Unlock",
                "DevTime", "Submarkets 1", "Submarket 2", "Submarket 3", 
                "Code Art", "Server", "Optional", "Software Categories"
            ]
            
            for col, text in enumerate(headers):
                label = ctk.CTkLabel(self.spec_feature_scroll_frame, text=text, 
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   width=90)
                label.grid(row=0, column=col, padx=5, pady=(5, 10), sticky="ew")

        entries = []
        for col in range(13):
            if col in [10, 11]:  # Server e Optional são True/False
                entry = ctk.CTkOptionMenu(self.spec_feature_scroll_frame, values=["True", "False"], width=90)
                entry.set("False")  # Valor padrão
            elif col == 9:  # Code Art é 1-5
                entry = ctk.CTkOptionMenu(self.spec_feature_scroll_frame, values=["1", "2", "3", "4", "5"], width=90)
                entry.set("1")  # Valor padrão
            else:
                entry = ctk.CTkEntry(self.spec_feature_scroll_frame, width=90)
            
            entry.grid(row=row_index + 1, column=col, padx=2, pady=2, sticky="ew")
            entries.append(entry)

        # Set up name trace for dynamic dropdown update
        entries[0].bind("<FocusOut>", lambda e: self.update_dropdowns())

        self.spec_feature_rows.append(entries)
        self.update_dropdowns()

    def validate_and_proceed(self):
        # Campos que não são obrigatórios
        optional_fields = ["Unlock Year", "Name Generator"]
        
        # Verificar se todos os campos obrigatórios foram preenchidos
        has_errors = False
        first_error_field = None
        
        # Validar todos os campos
        for label in self.software_type_fields:
            if label not in optional_fields and not self.software_type_fields[label].get().strip():
                self.error_labels[label].configure(text="This field is required")
                if not first_error_field:
                    first_error_field = self.software_type_fields[label]
                has_errors = True
            else:
                self.error_labels[label].configure(text="")

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        # Se o Unlock Year não foi preenchido, define o valor default
        unlock_year_field = self.software_type_fields["Unlock Year"]
        if not unlock_year_field.get().strip():
            unlock_year_field.insert(0, "1970")

        # Se todos os campos obrigatórios estão preenchidos, habilitar o botão Spec Features
        self.buttons["Spec Features"].configure(state="normal")
        
        # Mudar para o frame de Spec Features
        self.show_frame("Spec Features")

    def update_sub_features_button(self):
        # Habilita o botão Sub Features apenas se houver features criadas
        has_features = any(row[0].get().strip() for row in self.spec_feature_rows)
        self.buttons["Sub Features"].configure(state="normal" if has_features else "disabled")

 
if __name__ == "__main__":
    root = ctk.CTk()
    app = ModCreatorApp(root)
    root.mainloop()