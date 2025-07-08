from kivy.uix.progressbar import ProgressBar
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.card import MDCard
import json, os, random
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.widget import Widget

Window.size= (300,600)

PREGUNTAS_FILE = "preguntas.json"
class Ui(ScreenManager):
    pass
class MainApp(MDApp):
    # global screen_manager
    # screen_manager = ScreenManager()

    def build(self):
        self.title = "Examén AeroCivil"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = 'Skyblue' #'Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet', 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate', 'Coral', 'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan', 'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta', 'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen', 'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet', 'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick', 'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray', 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink', 'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen', 'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow', 'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen', 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow', 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue', 'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen', 'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose', 'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange', 'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred', 'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen'
        self.puntaje = 0
        Builder.load_file('design.kv')
        return Ui()
    def on_start(self):
        self.load_question()
        Clock.schedule_once(self.change_screen,3)   
    def change_screen(self,*args):
        app = App.get_running_app()
        app.root.current = "MainScreen"
    def change_style(self,checked, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
    def load_question(self,*args):
        if os.path.exists(PREGUNTAS_FILE):
            with open(PREGUNTAS_FILE, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        else:
            self.questions = [{
                "question": "¿Cuál es la capital de Francia?",
                "options": {"A": "París", "B": "Madrid", "C": ""},
                "answer": "A",
                "veces_respondida": 0
            }]
    def load_random_question(self,*args):
        if len(args) >=1:
            if args[0] == "Estudio Libre":
                self.screen2LoadQuestion = self.root.ids.Pregunta
                min_veces = min(q["veces_respondida"] for q in self.questions)
                self.candidatas = [q for q in self.questions if q["veces_respondida"] == min_veces]
            elif args[0] == "Examén":
                self.screen2LoadQuestion = self.root.ids.Examen
                self.candidatas = self.load_questions_exam()
    def answer_question_A(self,*args):
        self.answer_question("A")
    def answer_question_B(self,*args):
        self.answer_question("B")
    def answer_question_C(self,*args):
        self.answer_question("C")
    def answer_question(self,answer):
        if answer == self.selected_question['answer']:
            self.puntaje = self.puntaje+1
            self.dialogo = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="check-circle",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="CORRECTO",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton( 
                    MDButtonText(text="Continuar"),
                    style="text",
                    on_press = self.next_question, 
                    on_release = self.close_dialog
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
            )
            self.dialogo.autodismiss = False
            self.dialogo.open()
        else:
            self.dialogo = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="close-circle",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="INCORRECTO",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="La respuesta correcta es: "+ self.selected_question['options'][self.selected_question['answer']],
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Continuar"),
                    style="text",
                    pos_hint = {'center_x':0.5},
                    on_press = self.next_question,
                    on_release = self.close_dialog
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.dialogo.auto_dismiss = False
        self.dialogo.open()
    def close_dialog(self,*args):
        if self.dialogo:
            self.dialogo.dismiss()
    def load_questions_exam(self, *args):
        candidatas = []
        modulos = ["Derecho Aéreo","RAC 100","Aerodinámica Aplicada","Planificación de Vuelo","Meteorología Aeronáutica",
                   "Navegación Aérea","Comunicaciones Aeronaúticas","Factores Humanos y Actuación Humanda","Sistema de Gestión de la Seguridad Ocupacional", "Conocimiento Generales de las UA"
                   ]
        derecho_aereo = [q for q in self.questions if q["modulo"] == "Derecho Aéreo"]
        rac_100 = [q for q in self.questions if q["modulo"] == "RAC 100"]
        Aerodinamica = [q for q in self.questions if q["modulo"] == "Aerodinámica Aplicada"]
        PlanVuelo = [q for q in self.questions if q["modulo"] == "Planificación de Vuelo"]
        Metereologia = [q for q in self.questions if q['modulo']=='Metereología Aeronáutica']
        Navegacion = [q for q in self.questions if q["modulo"] == "Navegación Aérea"]
        Comunicaciones = [q for q in self.questions if q["modulo"] == "Comunicaciones Aeronaúticas"]
        FactoresHumanos = [q for q in self.questions if q["modulo"] == "Factores Humanos y Actuación Humanda"]
        SistemaGestion = [q for q in self.questions if q["modulo"] == "Sistema de Gestión de la Seguridad Ocupacional"]
        ConocimientoGeneral = [q for q in self.questions if q["modulo"] == "Conocimiento Generales de las UA"]
        for i in range(7): #7
            if i == 0:
                candidatas.append(random.choice(derecho_aereo))
            else:
                pregunta_propuesta = random.choice(derecho_aereo)
                pregunta = self.verify_question(candidatas,derecho_aereo,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(17): #17
            if i == 0:
                candidatas.append(random.choice(rac_100))
            else:
                pregunta_propuesta = random.choice(rac_100)
                pregunta = self.verify_question(candidatas,rac_100,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(5): #5
            if i == 0:
                candidatas.append(random.choice(Aerodinamica))
            else:
                pregunta_propuesta = random.choice(Aerodinamica)
                pregunta = self.verify_question(candidatas,Aerodinamica,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(3): #3
            if i == 0:
                candidatas.append(random.choice(PlanVuelo))
            else:
                pregunta_propuesta = random.choice(PlanVuelo)
                pregunta = self.verify_question(candidatas,PlanVuelo,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(10): #10
            if i == 0:
                candidatas.append(random.choice(Metereologia))
            else:
                pregunta_propuesta = random.choice(Metereologia)
                pregunta = self.verify_question(candidatas,Metereologia,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(9): #9
            if i == 0:
                candidatas.append(random.choice(Navegacion))
            else:
                pregunta_propuesta = random.choice(Navegacion)
                pregunta = self.verify_question(candidatas,Navegacion,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(2): #2
            if i == 0:
                candidatas.append(random.choice(Comunicaciones))
            else:
                pregunta_propuesta = random.choice(Comunicaciones)
                pregunta = self.verify_question(candidatas,Comunicaciones,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(3): #3
            if i == 0:
                candidatas.append(random.choice(FactoresHumanos))
            else:
                pregunta_propuesta = random.choice(FactoresHumanos)
                pregunta = self.verify_question(candidatas,FactoresHumanos,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(8): #8
            if i == 0:
                candidatas.append(random.choice(SistemaGestion))
            else:
                pregunta_propuesta = random.choice(SistemaGestion)
                pregunta = self.verify_question(candidatas,SistemaGestion,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(6): #6
            if i == 0:
                candidatas.append(random.choice(ConocimientoGeneral))
            else:
                pregunta_propuesta = random.choice(ConocimientoGeneral)
                pregunta = self.verify_question(candidatas,ConocimientoGeneral,pregunta_propuesta)
                candidatas.append(pregunta)
        for i in range(5): #5
            pregunta_propuesta = random.choice(self.questions)
            pregunta = self.verify_question(candidatas,self.questions,pregunta_propuesta)
            candidatas.append(pregunta)
        return candidatas
    def verify_question(self,candidatas,modulo,pregunta_propuesta):
        if pregunta_propuesta in candidatas:
            pregunta_propuesta = random.choice(modulo)
            self.verify_question(candidatas,modulo,pregunta_propuesta)
        return pregunta_propuesta
    def next_question(self, *args):
        if len(args) >=1:
            if args[0] == "Estudio Libre":
                self.screen2LoadQuestion = self.root.ids.Pregunta
            elif args[0] == "Examén":
                self.screen2LoadQuestion = self.root.ids.Examen
        if len(self.candidatas)>0:
            self.selected_question = random.choice(self.candidatas)
            self.screen2LoadQuestion.text = self.selected_question['question']
            self.candidatas.remove(self.selected_question)
            self.screen2LoadQuestion.ids.A_text.text = "A. "+ self.selected_question['options']['A']
            self.screen2LoadQuestion.ids.A_text.adaptive_size = False
            self.screen2LoadQuestion.ids.A_text.adaptive_height = True
            self.screen2LoadQuestion.ids.B_text.text = "B. "+ self.selected_question['options']['B']
            self.screen2LoadQuestion.ids.B_text.adaptive_size = False
            self.screen2LoadQuestion.ids.B_text.adaptive_height = True
            if 'C' in self.selected_question['options'].keys():
                if self.selected_question['options']['C'] == '':
                    self.screen2LoadQuestion.ids.C.C_text = ""
                    self.screen2LoadQuestion.ids.C.opacity = 0.
                    self.screen2LoadQuestion.ids.C.disabled = True
                else:
                    self.screen2LoadQuestion.ids.C_text.text = "C. "+self.selected_question['options']['C']
                    self.screen2LoadQuestion.ids.C_text.adaptive_size = False
                    self.screen2LoadQuestion.ids.C_text.adaptive_height = True
                    self.screen2LoadQuestion.ids.C.opacity = 1.
                    self.screen2LoadQuestion.ids.C.disabled = False
            else:
                self.screen2LoadQuestion.ids.C_text.text = ""
                self.screen2LoadQuestion.ids.C.opacity = 0.
                self.screen2LoadQuestion.ids.C.disabled = True
        else:
            app = App.get_running_app()
            app.root.current = "Resultado Examén"
            self.root.ids.ResultadosExamen.text =  "HA FINALIZADO EL EXAMEN SU PUNTAJE ES DE:"+ str(self.puntaje)
if __name__ == "__main__":
    MainApp().run()