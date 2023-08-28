class JSONToDartObject:
    generatedCode = ""
    className = ""
    json = ""
    codeToBeGeneratedLater = []

    def __init__(self, name, json):
        self.className = name
        self.json = json

    def generate(self, isList):
        self.addImport()
        self.declareClass(self.className)
        self.createVariables(self.json)
        self.createConstructor(self.className, self.json)
        self.createToMap(self.className, self.json)
        self.createFromMap(self.className, self.json, isList)
        self.createToJson(self.className, self.json)
        self.createFromJson(self.className)
        self.generateClassLater()

        return self.generatedCode

    def addImport(self):
        self.generatedCode += "import 'dart:convert';\n\n"

    def declareClass(self, className):
        self.generatedCode += f"class {className[0].upper() + className[1:]} {{\n"

    def createVariables(self, jsonReceived):
        for key, value in jsonReceived.items():
            if type(value) is dict:
                self.handleMap(key, value)
            elif type(value) is list:
                self.handleList(key, value[0])
            elif type(value) is str:
                self.generatedCode += f"  final String {key[0].lower() + key[1:]};\n"
            elif type(value) is int:
                self.generatedCode += f"  final int {key[0].lower() + key[1:]};\n"
            else:
                self.generatedCode += f"  final bool {key[0].lower() + key[1:]};\n"

    def createConstructor(self, className, fields):
        self.generatedCode += f"\n  const {className[0].upper() + className[1:]} ({{\n"

        for key in fields:
            self.generatedCode += f"    required this.{key[0].lower() + key[1:]},\n"

        self.generatedCode += "  });\n\n"

    def createFromJson(self, className):
        self.generatedCode += f"  factory {className[0].upper() + className[1:]}.fromJson(String source) => {className[0].upper() + className[1:]}.fromMap(json.decode(source));\n"
        self.generatedCode += "}\n\n"

    def createFromMap(self, className, fields, isList=False):
        if isList:
            self.generatedCode += f"  factory {className[0].upper() + className[1:]}.fromMap(List list) {{\n"
        else:
            self.generatedCode += f"  factory {className[0].upper() + className[1:]}.fromMap(Map<String, dynamic> map) {{\n"
        self.generatedCode += f"    return {className[0].upper() + className[1:]}(\n"

        for key, value in fields.items():
            if type(value) is dict:
                self.generatedCode += f"      {key[0].lower() + key[1:]}: {key[0].upper() + key[1:]}.fromMap(map['{key}']),\n"
            elif type(value) is list:
                if isList:
                    self.generatedCode += f"      {key[0].lower() + key[1:]}: list.map((e) => {key[0].upper() + key[1:]}.fromMap(e)).toList(),\n"
                else:
                    self.generatedCode += f"      {key[0].lower() + key[1:]}: (map['{key}'] as List).map((e) => {key[0].upper() + key[1:]}.fromMap(e)).toList(),\n"
            elif type(value) is str:
                self.generatedCode += (
                    f"      {key[0].lower() + key[1:]}: map['{key}'] ?? '',\n"
                )

            elif type(value) is int:
                self.generatedCode += (
                    f"      {key[0].lower() + key[1:]}: map['{key}'].toInt() ?? 0,\n"
                )

            else:
                self.generatedCode += (
                    f"      {key[0].lower() + key[1:]}: map['{key}'] ?? false,\n"
                )

        self.generatedCode += "    );\n  }\n\n"

    def createToMap(self, className, fields):
        self.generatedCode += f"  Map<String, dynamic> toMap() {{\n"
        self.generatedCode += f"    final result = <String, dynamic>{{}};\n\n"

        for key, value in fields.items():
            self.generatedCode += f"    result.addAll({{'{key[0].lower() + key[1:]}': {key[0].lower() + key[1:]}}});\n"

        self.generatedCode += "\n    return result;\n"
        self.generatedCode += "  }\n\n"

    def createToJson(self, className, fields):
        self.generatedCode += f"  String toJson() => json.encode(toMap());\n\n"

    def generateClassLater(self):
        for json in self.codeToBeGeneratedLater:
            className = list(json.keys())[0]
            values = list(json.values())[0]

            self.declareClass(className)
            self.createVariables(values)
            self.createConstructor(className, values)
            self.createToMap(className, values)
            self.createFromMap(className, values)
            self.createToJson(className, values)
            self.createFromJson(className)

    def handleMap(self, key, value):
        self.generatedCode += (
            f"  final {key[0].upper() + key[1:]} {key[0].lower() + key[1:]};\n"
        )

        self.codeToBeGeneratedLater.append({key: value})

    def handleList(self, key, value):
        self.generatedCode += (
            f"  final List<{key[0].upper() + key[1:]}> {key[0].lower() + key[1:]};\n"
        )

        self.codeToBeGeneratedLater.append({key: value})
