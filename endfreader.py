import os
import re
import endf



class Decay:
    def __init__(self):
        decay_folder = os.path.abspath('ENDF-B-VIII.1/decay-version.VIII.1')

        self.isotopes =[]
        self.decdata = []


        for filename in sorted(os.listdir(decay_folder)):
            if filename.endswith(".endf"):
                    parts = filename.split("-")[1].split(".")[0].split("_")
                    match = re.match(r"^(\d{3})([a-zA-Z0-9]*)$", parts[2])
                    if match:
                        A = int(match.group(1))
                        m = match.group(2) if match.group(2) else None
                        Z = int(parts[0])
                        symbol = parts[1]
                        lst = [symbol, Z, A]
                        self.isotopes.append(lst)
                    data =[]
                    file_path = os.path.join(decay_folder, filename)
                    with open(file_path, 'r') as decay:
                        for line in decay:
                            row = line.split()
                            if row[-1] == '8457':  # check row is not empty
                                converted_row = []
                                
                                for item in row:
                                    item = item.replace('+', 'E')
                                    if item[0] != '-':
                                        item = item.replace('-', 'E', 1)
                                    converted_row.append(float(item))
                                data.append(converted_row)
                        self.decdata.append(data)


        for i in range(len(self.decdata)):
            if self.decdata[i][0][4] == 1:
                self.isotopes[i].append('stable')
            elif self.decdata[i][4][0] == 0:
                self.isotopes[i].append('gamma')
            elif self.decdata[i][4][0] == 1:
                self.isotopes[i].append('beta-')
            elif self.decdata[i][4][0] == 2:
                self.isotopes[i].append('beta+')
            elif self.decdata[i][4][0] == 3:
                self.isotopes[i].append('IT')
            elif self.decdata[i][4][0] == 4:
                self.isotopes[i].append('alpha')
            elif self.decdata[i][4][0] == 5:
                self.isotopes[i].append('n')
            elif self.decdata[i][4][0] == 6:
                self.isotopes[i].append('sf')
            elif self.decdata[i][4][0] == 7:
                self.isotopes[i].append('p')
            elif self.decdata[i][4][0] == 10:
                self.isotopes[i].append('unkhown')
            elif self.decdata[i][4][0] == 1.4:
                self.isotopes[i].append('beta-, alpha')
            elif self.decdata[i][4][0] == 1.5:
                self.isotopes[i].append('beta-, n')
            elif self.decdata[i][4][0] == 2.4:
                self.isotopes[i].append('beta+, alpha')
            else:
                self.isotopes[i].append('uncertain')
        


    def get_isotopes(self):
        return self.isotopes
    

                    





        


# class Element:
#     def __init__(self, symbol, Z):
#         if not isinstance(Z, int) or Z < 0 or Z > 118:
#             raise ValueError("Atomic number (Z) must be an integer between 1 and 118.")
#         self.symbol = symbol
#         self.Z = Z

#     def describe(self):
#         print(f"Element: {self.symbol}, Atomic number: {self.Z}")

# class Isotope(Element):
#     def __init__(self, symbol, Z, A, m=None):
#         super().__init__(symbol, Z)
#         if not isinstance(A, int) or A <= 0 or A > 300:
#             raise ValueError("Mass number (A) must be an integer between 1 and 300.")
#         if A < Z:
#             raise ValueError("Mass number (A) cannot be less than atomic number (Z).")
#         self.A = A
#         self.m = m if m is not None else 0

#     def describe(self):
#         super().describe()
#         if self.m:
#             print(f"Mass number: {self.A}, Meta-stable state: {self.m}")
#         else:
#             print(f"Mass number: {self.A}")



# class endfReader:
#     def __init__(self):
#         self.decay_folder = os.path.abspath('ENDF-B-VIII.1/decay-version.VIII.1')
#         self.neutron_folder = os.path.abspath('ENDF/neutron')
        
#     def read_isotopes_from_decay_folder(decay_folder):
#         isotopes_with_files = []
#         if not os.path.exists(decay_folder):
#             raise FileNotFoundError(f"The folder '{decay_folder}' does not exist.")

#         for filename in os.listdir(decay_folder):
#             if filename.endswith(".endf"):
#                     parts = filename.split("-")[1].split(".")[0].split("_")
#                     match = re.match(r"^(\d{3})([a-zA-Z0-9]*)$", parts[2])
#                     if match:
#                         A = int(match.group(1))
#                         m = match.group(2) if match.group(2) else None
#                         Z = int(parts[0])
#                         symbol = parts[1]
#                         isotopes_with_files.append((Isotope(symbol, Z, A, m), filename))
#         return isotopes_with_files

#     def fetch_isotope_list(self, symbol, Z):
#         decay_folder = os.path.abspath("ENDF-B-VIII.1/decay-version.VIII.1")
#         isotopes = endfReader.read_isotopes_from_decay_folder(decay_folder, Z_filter=Z)
#         self.core_model.getRightLayout().show_isotope_list(symbol, Z, isotopes)


#     def create_isotope_callback(self, symbol, Z, A, m, filename):
#         return lambda: self.fetch_isotope_info(symbol, Z, A, m, filename)

#     def fetch_isotope_info(self, symbol, Z, A, m, filename):
#             decay_folder = os.path.abspath("ENDF-B-VIII.1/decay-version.VIII.1")
#             filepath = os.path.join(decay_folder, filename)
#             mat = endf.Material(filepath)
#             if (8, 457) in mat.section_data:
#                 decay_data = mat.section_data[(8, 457)]
#                 data = self.analyze_decay_data(decay_data, filename, Isotope(symbol, Z, A, m))
#                 self.update_info(symbol, data)


#     def analyze_decay_data(self, decay_data, filename, isotope):
#         result = {
#             "A": isotope.A,
#             "m": isotope.m,
#             "stable": "modes" not in decay_data or all(mode.get("RTYP") == 0.0 for mode in decay_data.get("modes", [])),
#             "decay_modes": []
#         }
#         if not result["stable"]:
#             for mode in decay_data.get("modes", []):
#                 rtyp = mode.get("RTYP")
#                 decay_type = {
#                     0.0: "Gamma radiation",
#                     1.0: "Beta-minus decay (β⁻)",
#                     2.0: "Electron capture or Positron decay (β⁺, e.c.)",
#                     3.0: "Isomeric transition (IT)",
#                     4.0: "Alpha decay (α)",
#                     5.0: "Neutron emission",
#                     6.0: "Spontaneous fission (SF)",
#                     7.0: "Proton emission",
#                     10.0: "Unknown decay type"
#                 }.get(rtyp, f"Unknown decay (RTYP={rtyp})")
#                 result["decay_modes"].append({
#                     "type": decay_type,
#                     "Q": mode.get("Q", [0.0])[0],
#                     "half_life": decay_data.get("T1/2", ["Unknown"])[0]
#                 })
#         return result

#     def update_info(self, symbol, data):
#         info = f"<h2 style='font-size: 26px; font-weight: bold; color: orange;'>{symbol}-{data['A']}{'m' if data['m'] else ''}</h2>"
#         info += f"<p style='font-size: 20px; color: orange;'><b>Stable:</b> {'Yes' if data.get('stable') else 'No'}</p>"
#         if not data.get("stable"):
#             info += "<p style='font-size: 20px; color: orange;'><b>Decay Modes:</b></p><ul>"
#             for mode in data.get("decay_modes", []):
#                 info += f"<li style='font-size: 18px; color: orange;'><b>Type:</b> {mode['type']}, <b>Energy:</b> {mode['Q']} keV, <b>Half-life:</b> {mode['half_life']} sec</li>"
#             info += "</ul>"
#         self.label.setText(info)
#         self.label.setWordWrap(True)

    


#     # def decaytypes(self, Z, A):
#     #     return decay_type
    
#     # def decayenergy(self, Z, A):
#     #     return energy
    
#     # def halflife(self, Z, A):
#     #     return half_life
    


# #     # функция для извлечения доступныз изотопов
# #     def read_isotopes_from_decay_folder(decay_folder, Z_filter=None, A_filter=None, m_filter=None):
# #         isotopes_with_files = []
# #         if not os.path.exists(decay_folder):
# #             raise FileNotFoundError(f"The folder '{decay_folder}' does not exist.")

# #         for filename in os.listdir(decay_folder):
# #             if filename.endswith(".endf"):
# #                 try:
# #                     parts = filename.split("-")[1].split(".")[0].split("_")
# #                     match = re.match(r"^(\d{3})([a-zA-Z0-9]*)$", parts[2])
# #                     if match:
# #                         A = int(match.group(1))
# #                         m = match.group(2) if match.group(2) else None
# #                         Z = int(parts[0])
# #                         symbol = parts[1]
# #                         if Z_filter is not None and Z != Z_filter:
# #                             continue
# #                         if A_filter is not None and A != A_filter:
# #                             continue
# #                         if m_filter is not None and m != m_filter:
# #                             continue
# #                         isotopes_with_files.append((Isotope(symbol, Z, A, m), filename))
# #                 except (ValueError, IndexError) as e:
# #                     print(f"Skipping file '{filename}': {e}")
# #         return isotopes_with_files
                



# #     def get_decay_info(self, Z, A):
# #         pass




# #     # def decay_reader(self):
# #     #     isotopes_with_files = []
# #     #     if not os.path.exists(self.decay_folder):
# #     #         raise FileNotFoundError(f"The folder '{self.decay_folder}' does not exist.")

# #     #     for filename in os.listdir(self.decay_folder):
# #     #         if filename.endswith(".endf"):
# #     #             # try:
# #     #             parts = filename.split("-")[1].split(".")[0].split("_")
# #     #             match = re.match(r"^(\d{3})([a-zA-Z0-9]*)$", parts[2])
# #     #             if match:
# #     #                 A = int(match.group(1))
# #     #                 m = match.group(2) if match.group(2) else None
# #     #                 Z = int(parts[0])
# #     #                 symbol = parts[1]
# #     #             #         if Z_filter is not None and Z != Z_filter:
# #     #             #             continue
# #     #             #         if A_filter is not None and A != A_filter:
# #     #             #             continue
# #     #             #         if m_filter is not None and m != m_filter:
# #     #             #             continue
# #     #             #         isotopes_with_files.append((Isotope(symbol, Z, A, m), filename))
# #     #             # except (ValueError, IndexError) as e:
# #     #             #     print(f"Skipping file '{filename}': {e}")
# #     #     return isotopes_with_files


# #     def neutron_reader(self):
# #         pass
        

# # class ELement:
# #     def __init__(self, symbol, Z):
# #         if not isinstance(Z, int) or Z < 0 or Z > 118:
# #             raise ValueError("Atomic number (Z) must be an integer between 1 and 118.")
# #         self.symbol = symbol
# #         self.Z = Z

# #     def describe(self):
# #         print(f"Element: {self.symbol}, Atomic number: {self.Z}")

# # class Isotope(ELement):
# #     def __init__(self, symbol, Z, A, m=None):
# #         super().__init__(symbol, Z)
# #         if not isinstance(A, int) or A <= 0 or A > 300:
# #             raise ValueError("Mass number (A) must be an integer between 1 and 300.")
# #         if A < Z:
# #             raise ValueError("Mass number (A) cannot be less than atomic number (Z).")
# #         self.A = A
# #         self.m = m if m is not None else 0

# #     def describe(self):
# #         super().describe()
# #         if self.m:
# #             print(f"Mass number: {self.A}, Meta-stable state: {self.m}")
# #         else:
# #             print(f"Mass number: {self.A}")

# # class EndfReader:
# #     @staticmethod
# #     def read_isotopes_from_decay_folder(decay_folder, Z_filter=None, A_filter=None, m_filter=None):
# #         isotopes_with_files = []
# #         if not os.path.exists(decay_folder):
# #             raise FileNotFoundError(f"The folder '{decay_folder}' does not exist.")

# #         for filename in os.listdir(decay_folder):
# #             if filename.endswith(".endf"):
# #                 try:
# #                     parts = filename.split("-")[1].split(".")[0].split("_")
# #                     match = re.match(r"^(\d{3})([a-zA-Z0-9]*)$", parts[2])
# #                     if match:
# #                         A = int(match.group(1))
# #                         m = match.group(2) if match.group(2) else None
# #                         Z = int(parts[0])
# #                         symbol = parts[1]
# #                         if Z_filter is not None and Z != Z_filter:
# #                             continue
# #                         if A_filter is not None and A != A_filter:
# #                             continue
# #                         if m_filter is not None and m != m_filter:
# #                             continue
# #                         isotopes_with_files.append((Isotope(symbol, Z, A, m), filename))
# #                 except (ValueError, IndexError) as e:
# #                     print(f"Skipping file '{filename}': {e}")
# #         return isotopes_with_files
    
    
# #     def fetch_isotope_list(self, symbol, Z):
# #         try:
# #             decay_folder = os.path.abspath("decay")
# #             isotopes = EndfReader.read_isotopes_from_decay_folder(decay_folder, Z_filter=Z)
# #             self.core_model.getRightLayout().show_isotope_list(symbol, Z, isotopes)
# #         except Exception as e:
# #             QMessageBox.critical(self, "Error", f"Couldn't read isotopes: {e}")