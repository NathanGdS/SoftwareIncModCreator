import customtkinter as ctk

class BaseFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.fields = {}
        self.error_labels = {}

    def validate_field(self, field_label, optional_fields=None):
        if optional_fields is None:
            optional_fields = []
            
        widget = self.fields[field_label]
        error_label = self.error_labels[field_label]
        
        if field_label not in optional_fields and isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
            error_label.configure(text="This field is required")
            return False
        else:
            error_label.configure(text="")
            return True

    def create_field(self, parent, label_text, entry_placeholder="", field_type="entry", options=None, row=0, column=0):
        ctk.CTkLabel(parent, text=f"{label_text}:", anchor="e", font=ctk.CTkFont(size=14)).grid(
            row=row, column=column, padx=(0, 15), pady=5, sticky="e"
        )

        if field_type == "option":
            entry = ctk.CTkOptionMenu(parent, values=options or [], width=300)
            entry.set(options[0] if options else "")
        else:
            entry = ctk.CTkEntry(parent, placeholder_text=entry_placeholder, width=300)
        
        entry.grid(row=row, column=column + 1, pady=5, sticky="ew")
        self.fields[label_text] = entry
        
        error_label = ctk.CTkLabel(parent, text="", text_color="#FF4444", font=ctk.CTkFont(size=12))
        error_label.grid(row=row + 1, column=column + 1, sticky="w", padx=10)
        self.error_labels[label_text] = error_label

        if isinstance(entry, ctk.CTkEntry):
            entry.bind("<KeyRelease>", lambda e, lbl=label_text: self.validate_field(lbl))

        return entry

class SoftwareTypeFrame(BaseFrame):
    def __init__(self, parent, on_next_callback):
        super().__init__(parent, corner_radius=15)
        self.on_next_callback = on_next_callback
        self._create_frame()

    def _create_frame(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(content_frame, text="Software Type", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = {
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
        }

        boolean_fields = ["OS Supports", "Contract Software", "In House Software"]

        for i, (label_text, entry_placeholder) in enumerate(fields.items(), start=1):
            if label_text in boolean_fields:
                self.create_field(content_frame, label_text, field_type="option", 
                                options=["True", "False"], row=i*2-1)
            else:
                self.create_field(content_frame, label_text, entry_placeholder, row=i*2-1)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, columnspan=2, sticky="e", padx=20, pady=(0, 20))

        next_btn = ctk.CTkButton(button_frame, text="Next", width=100, command=self.validate_and_proceed)
        next_btn.pack(pady=10)

    def validate_and_proceed(self):
        optional_fields = ["Unlock Year", "Name Generator"]
        has_errors = False
        first_error_field = None

        for label in self.fields:
            if not self.validate_field(label, optional_fields):
                if not first_error_field:
                    first_error_field = self.fields[label]
                has_errors = True

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        unlock_year_field = self.fields["Unlock Year"]
        if not unlock_year_field.get().strip():
            unlock_year_field.insert(0, "1970")

        if self.on_next_callback:
            self.on_next_callback()

    def get_data(self):
        return {label: widget.get() for label, widget in self.fields.items()}

class SpecFeaturesFrame(BaseFrame):
    def __init__(self, parent, on_back_callback, on_add_callback, on_next_callback):
        super().__init__(parent, corner_radius=15)
        self.on_back_callback = on_back_callback
        self.on_add_callback = on_add_callback
        self.on_next_callback = on_next_callback
        self.feature_rows = []
        self._create_frame()

    def _create_frame(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Spec Features", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, pady=(20, 10)
        )

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew", padx=20)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(container, width=1200, height=500)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")

        for i in range(13):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))

        add_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        add_button_frame.pack(side="left")

        right_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_button_frame.pack(side="right")

        ctk.CTkButton(add_button_frame, text="+", width=30, command=self.on_add_callback).pack(side="left")
        
        ctk.CTkButton(right_button_frame, text="Back", width=100, command=self.on_back_callback).pack(side="left", padx=5)
        self.next_button = ctk.CTkButton(right_button_frame, text="Next", width=100, command=self.on_next_callback, state="disabled")
        self.next_button.pack(side="left", padx=5)

    def add_row(self):
        row_index = len(self.feature_rows)
        
        if row_index == 0:
            headers = [
                "Name", "Spec", "Description", "Dependencies", "Unlock",
                "DevTime", "Submarkets 1", "Submarket 2", "Submarket 3", 
                "Code Art", "Server", "Optional", "Software Categories"
            ]
            
            for col, text in enumerate(headers):
                label = ctk.CTkLabel(self.scroll_frame, text=text, 
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   width=90)
                label.grid(row=0, column=col, padx=5, pady=(5, 10), sticky="ew")

        entries = []
        for col in range(13):
            if col in [10, 11]:  # Server e Optional são True/False
                entry = ctk.CTkOptionMenu(self.scroll_frame, values=["True", "False"], width=90)
                entry.set("False")
            elif col == 9:  # Code Art é 1-5
                entry = ctk.CTkOptionMenu(self.scroll_frame, values=["1", "2", "3", "4", "5"], width=90)
                entry.set("1")
            else:
                entry = ctk.CTkEntry(self.scroll_frame, width=90)
            
            entry.grid(row=row_index + 1, column=col, padx=2, pady=2, sticky="ew")
            entries.append(entry)

        self.feature_rows.append(entries)
        self.update_next_button()
        return entries

    def update_next_button(self):
        has_features = bool(self.get_feature_names())
        self.next_button.configure(state="normal" if has_features else "disabled")

    def get_feature_names(self):
        return [row[0].get() for row in self.feature_rows if row[0].get().strip()]

    def get_data(self):
        features = []
        for row in self.feature_rows:
            if not any(entry.get().strip() for entry in row):
                continue
            features.append({
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
        return features

class SubFeaturesFrame(BaseFrame):
    def __init__(self, parent, on_back_callback, on_add_callback):
        super().__init__(parent, corner_radius=15)
        self.on_back_callback = on_back_callback
        self.on_add_callback = on_add_callback
        self.sub_feature_rows = []
        self._create_frame()

    def _create_frame(self):
        ctk.CTkLabel(self, text="Sub Features", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", width=1200, height=300)
        self.scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

        headers = [
            "Name", "Description", "Level", "Unlock Year", "Dev Time",
            "Submarket 1", "Submarket 2", "Submarket 3",
            "Code Art", "Server", "Software Categories", "Software Feature"
        ]
        
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(self.scroll_frame, text=text, font=ctk.CTkFont(size=12, weight="bold"), 
                               anchor="w", width=120)
            label.grid(row=0, column=col, padx=5, pady=(5, 10), sticky="w")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))

        add_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        add_button_frame.pack(side="left")
        
        back_button_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        back_button_frame.pack(side="right")

        ctk.CTkButton(add_button_frame, text="+", width=30, command=self.on_add_callback).pack(side="left")
        ctk.CTkButton(back_button_frame, text="Back", width=100, command=self.on_back_callback).pack(side="right")

    def add_row(self, feature_names=None):
        row_index = len(self.sub_feature_rows)
        entries = []

        for col in range(12):
            if col == 2:  # Level
                entry = ctk.CTkOptionMenu(self.scroll_frame, values=["1", "2"], width=120)
            elif col == 11:  # Software Feature
                entry = ctk.CTkOptionMenu(self.scroll_frame, values=feature_names or [""], width=120)
            else:
                entry = ctk.CTkEntry(self.scroll_frame, width=120)

            entry.grid(row=row_index + 1, column=col, padx=5, pady=2)
            entries.append(entry)

        self.sub_feature_rows.append(entries)
        return entries

    def update_feature_dropdowns(self, feature_names):
        for row in self.sub_feature_rows:
            row[11].configure(values=feature_names or [""])

    def get_data(self):
        sub_features = []
        for row in self.sub_feature_rows:
            if not any(entry.get().strip() for entry in row):
                continue
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
        return sub_features 

class NewFeatureFrame(BaseFrame):
    def __init__(self, parent, on_back_callback, on_save_callback):
        super().__init__(parent, corner_radius=15)
        self.on_back_callback = on_back_callback
        self.on_save_callback = on_save_callback
        self._create_frame()

    def _create_frame(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(self, text="New Feature", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        content_frame = ctk.CTkScrollableFrame(self, width=800, height=500)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content_frame.grid_columnconfigure(1, weight=1)

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

        for i, (label_text, entry_placeholder) in enumerate(labels.items(), start=0):
            if label_text == "Code Art":
                self.create_field(content_frame, label_text, field_type="option", 
                                options=["1", "2", "3", "4", "5"], row=i*2)
            elif label_text.startswith("Submarket"):
                self.create_field(content_frame, label_text, field_type="option", 
                                options=["1", "2", "3", "4", "5"], row=i*2)
            elif label_text in ["Server", "Optional"]:
                self.create_field(content_frame, label_text, field_type="option", 
                                options=["True", "False"], row=i*2)
            else:
                self.create_field(content_frame, label_text, entry_placeholder, row=i*2)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(0, 20), sticky="e", padx=20)
        
        back_btn = ctk.CTkButton(button_frame, text="Back", width=100, command=self.on_back_callback)
        back_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", width=100, command=self.validate_and_save)
        save_btn.pack(side="left", padx=5)

    def validate_and_save(self):
        optional_fields = ["Unlock", "Software Categories"]
        has_errors = False
        first_error_field = None
        
        for label in self.fields:
            if not self.validate_field(label, optional_fields):
                if not first_error_field:
                    first_error_field = self.fields[label]
                has_errors = True

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        data = self.get_data()
        self.on_save_callback(data)
        self.clear_fields()

    def clear_fields(self):
        for widget in self.fields.values():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget.cget("values")[0])

    def get_data(self):
        return {label: widget.get() for label, widget in self.fields.items()}

class NewSubFeatureFrame(BaseFrame):
    def __init__(self, parent, on_back_callback, on_save_callback):
        super().__init__(parent, corner_radius=15)
        self.on_back_callback = on_back_callback
        self.on_save_callback = on_save_callback
        self._create_frame()

    def _create_frame(self):
        title_label = ctk.CTkLabel(self, text="Sub Feature", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

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

        for i, (label_text, entry_placeholder) in enumerate(labels.items(), start=1):
            if label_text == "Level":
                self.create_field(self, label_text, field_type="option", 
                                options=["1", "2"], row=i*2-1)
            elif label_text == "Dev Time" or label_text == "Code Art":
                self.create_field(self, label_text, field_type="option", 
                                options=["1", "2", "3", "4", "5"], row=i*2-1)
            elif label_text.startswith("Submarket"):
                self.create_field(self, label_text, field_type="option", 
                                options=["1", "2", "3", "4", "5"], row=i*2-1)
            elif label_text == "Feature":
                self.create_field(self, label_text, field_type="option", 
                                options=[""], row=i*2-1)
            else:
                self.create_field(self, label_text, entry_placeholder, row=i*2-1)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=len(labels)*2+1, column=1, pady=20, sticky="e")
        
        back_btn = ctk.CTkButton(button_frame, text="Back", width=100, command=self.on_back_callback)
        back_btn.pack(side="left", padx=5)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", width=100, command=self.validate_and_save)
        save_btn.pack(side="left", padx=5)

    def update_feature_options(self, feature_names):
        if "Feature" in self.fields:
            self.fields["Feature"].configure(values=feature_names or [""])
            if feature_names:
                self.fields["Feature"].set(feature_names[0])

    def validate_and_save(self):
        has_errors = False
        first_error_field = None
        
        for label, widget in self.fields.items():
            if isinstance(widget, ctk.CTkEntry) and not widget.get().strip():
                self.error_labels[label].configure(text="This field is required")
                if not first_error_field:
                    first_error_field = widget
                has_errors = True
            else:
                self.error_labels[label].configure(text="")

        if has_errors:
            if first_error_field:
                first_error_field.focus_set()
            return

        data = self.get_data()
        self.on_save_callback(data)
        self.clear_fields()

    def clear_fields(self):
        for widget in self.fields.values():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget.cget("values")[0])

    def get_data(self):
        return {label: widget.get() for label, widget in self.fields.items()} 