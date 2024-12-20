import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox, QCalendarWidget, QFileDialog, QAbstractItemView, QComboBox  # Import correto
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Initial data to be used in the Bullet Journal
initial_data = {
    "Organização": ["Exemplo de tarefa"],
    "Trabalhos a Fazer": ["Projeto A - prazo até sexta-feira"],
    "Treino Físico": ["Corrida - 30 minutos"],
    "Notas": ["Nota importante sobre o dia"],
    "Diário": ["Hoje foi um dia produtivo."],
    "Agenda": ["Reunião às 10h"]
}

# Data structure to hold the journal entries
data = initial_data.copy()

# Data structure to hold the objetivos and modelo entries
objetivos_data = {
    "Objetivos Gerais": [
        "Exercícios Físicos, Manter a saúde e melhorar o condicionamento físico.",
        "Estudos, Desenvolver habilidades e aprender algo novo diariamente.",
        "Trabalho, Aumentar a produtividade com organização.",
        "Lazer, Garantir tempo para relaxar e recarregar as energias."
    ],
    "Modelo Semanal": [
        "5:00h - 5:15h Acordar e alongamento leve.",
        "5:15h - 5:45h Exercícios físicos corrida leve, yoga ou treino de força.",
        "5:45h - 6:00h Meditação ou journaling para planejamento do dia.",
        "8:00h - 12:00h Trabalho ou estudos principais.",
        "12:00h - 15:30h Tempo para projetos ou lazer leve.",
        "15:30h - 16:30h Primeira refeição do dia.",
        "16:30h - 17:30h Revisão dos estudos ou leitura.",
        "17:30h - 18:30h Exercícios ou esportes ao ar livre.",
        "18:30h - 20:00h Atividades recreativas ou hobbies.",
        "20:00h - 21:00h Lazer (filmes, séries, hobbies).",
        "21:00h - 21:30h Planejamento do dia seguinte e relaxamento.",
        "21:30h Hora de dormir."
    ],
    "Dicas para Manutenção": [
        "Consistência, Tente seguir os horários regularmente, mas seja flexível quando necessário.",
        "Revisão Semanal, Reserve um tempo no domingo para avaliar o que funcionou e ajustar o que for preciso.",
        "Customização, Adapte os tempos e atividades às suas necessidades."
    ]
}

class BulletJournalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bullet Journal: Rotina Equilibrada")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.init_objetivos_tab()
        self.init_categories_tabs()

    def init_objetivos_tab(self):
        objetivos_tab = QWidget()
        self.tab_widget.addTab(objetivos_tab, "Objetivos Gerais")
        objetivos_layout = QVBoxLayout(objetivos_tab)

        self.objetivos_list_widget = QListWidget()
        self.objetivos_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.update_objetivos_list()
        objetivos_layout.addWidget(self.objetivos_list_widget)

        button_layout = QHBoxLayout()
        self.edit_objetivo_button = QPushButton("Editar")
        self.edit_objetivo_button.clicked.connect(self.edit_objetivo)
        self.remove_objetivo_button = QPushButton("Remover")
        self.remove_objetivo_button.clicked.connect(self.remove_objetivo)
        self.add_to_entry_button = QPushButton("Adicionar na Entrada")
        self.add_to_entry_button.clicked.connect(self.add_to_entry)

        # Alterar cores dos botões para melhor contraste
        self.edit_objetivo_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.remove_objetivo_button.setStyleSheet("background-color: #F44336; color: white;")
        self.add_to_entry_button.setStyleSheet("background-color: #FF9800; color: white;")

        button_layout.addWidget(self.edit_objetivo_button)
        button_layout.addWidget(self.remove_objetivo_button)
        button_layout.addWidget(self.add_to_entry_button)
        objetivos_layout.addLayout(button_layout)

        # Adicionar botões de Salvar, Carregar e Exportar
        self.save_button = QPushButton("Salvar JSON")
        self.save_button.clicked.connect(self.save_json)
        self.load_button = QPushButton("Carregar JSON")
        self.load_button.clicked.connect(self.load_json)
        self.export_button = QPushButton("Exportar TXT")
        self.export_button.clicked.connect(self.export_txt)
        self.export_pdf_button = QPushButton("Exportar PDF")
        self.export_pdf_button.clicked.connect(self.export_pdf)

        # Alterar cores dos botões para melhor contraste
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.load_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.export_button.setStyleSheet("background-color: #FF9800; color: white;")
        self.export_pdf_button.setStyleSheet("background-color: #9C27B0; color: white;")

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.export_pdf_button)
        objetivos_layout.addLayout(button_layout)

    def init_categories_tabs(self):
        self.category_tabs = {}
        for category in data.keys():
            category_tab = QWidget()
            self.tab_widget.addTab(category_tab, category)
            category_layout = QVBoxLayout(category_tab)

            entry_label = QLabel("Entrada:")
            entry_input = QLineEdit()
            description_label = QLabel("Descrição:")
            description_input = QTextEdit()
            add_button = QPushButton("Adicionar")
            add_button.clicked.connect(lambda _, c=category, e=entry_input, d=description_input: self.add_entry(c, e, d))

            date_label = QLabel("Data (para Agenda):")
            date_button = QPushButton("Selecionar Data")
            date_button.clicked.connect(self.select_date)

            list_widget = QListWidget()
            list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
            self.update_category_list(category, list_widget)

            edit_button = QPushButton("Editar Entrada")
            edit_button.clicked.connect(lambda _, l=list_widget, c=category: self.edit_category_entry(l, c))
            remove_button = QPushButton("Remover Entrada")
            remove_button.clicked.connect(lambda _, l=list_widget, c=category: self.remove_category_entry(l, c))

            # Alterar cores dos botões para melhor contraste
            add_button.setStyleSheet("background-color: #4CAF50; color: white;")
            edit_button.setStyleSheet("background-color: #2196F3; color: white;")
            remove_button.setStyleSheet("background-color: #F44336; color: white;")

            category_layout.addWidget(entry_label)
            category_layout.addWidget(entry_input)
            category_layout.addWidget(description_label)
            category_layout.addWidget(description_input)
            category_layout.addWidget(add_button)
            category_layout.addWidget(date_label)
            category_layout.addWidget(date_button)
            category_layout.addWidget(list_widget)

            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(remove_button)
            category_layout.addLayout(button_layout)

            # Adiciona o date_label à classe para que ele possa ser acessado globalmente
            self.date_label = date_label

            # Armazena a referência ao widget da lista para cada categoria
            self.category_tabs[category] = list_widget

    def update_category_list(self, category, list_widget):
        list_widget.clear()
        for entry in data[category]:
            item = QListWidgetItem(entry)
            list_widget.addItem(item)

    def add_entry(self, category, entry_input, description_input):
        entry = entry_input.text()
        description = description_input.toPlainText()
        date = self.date_label.text().split(": ")[1] if self.date_label.text() and ": " in self.date_label.text() else "N/A"
        if entry:
            # Limita o número de caracteres por linha
            entry = self.wrap_text(entry, 70)
            description = self.wrap_text(description, 70)
            formatted_entry = f"{entry} ({date}) - Descrição: {description}"
            data[category].append(formatted_entry)
            self.update_category_list(category, self.category_tabs[category])
            entry_input.clear()
            description_input.clear()
        else:
            QMessageBox.warning(self, "Erro", "Preencha o campo de entrada.")

    def wrap_text(self, text, max_length):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_length:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)

    def select_date(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Selecionar Data")
        layout = QVBoxLayout(dialog)
        calendar = QCalendarWidget()
        layout.addWidget(calendar)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = calendar.selectedDate()
            self.date_label.setText(f"Data (para Agenda): {selected_date.toString('dd-MM-yyyy')}")

    def save_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar JSON", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    json.dump({"data": data, "objetivos_data": objetivos_data}, f, indent=4)
                QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao salvar JSON: {e}")

    def load_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Carregar JSON", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    loaded_data = json.load(f)
                    global data, objetivos_data
                    data = loaded_data.get("data", initial_data)
                    objetivos_data = loaded_data.get("objetivos_data", objetivos_data)
                self.update_objetivos_list()
                for category in data.keys():
                    if category in self.category_tabs:
                        self.update_category_list(category, self.category_tabs[category])
                QMessageBox.information(self, "Sucesso", "Dados carregados com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao carregar JSON: {e}")

    def export_txt(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar TXT", "", "Text Files (*.txt)")
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    for category, entries in data.items():
                        f.write(f"{category}:\n")
                        for entry in entries:
                            f.write(f"  - {entry}\n")
                        f.write("\n")
                QMessageBox.information(self, "Sucesso", "Dados exportados com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao exportar TXT: {e}")

    def export_pdf(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Exportar PDF", "", "PDF Files (*.pdf)")
        if file_name:
            try:
                doc = SimpleDocTemplate(file_name, pagesize=A4)
                styles = getSampleStyleSheet()
                story = []

                # Título do documento
                story.append(Paragraph("Bullet Journal: Rotina Equilibrada", styles['Title']))
                story.append(Spacer(1, 12))

                # Exportar todas as categorias do dicionário data
                story.append(Paragraph("Categorias do Bullet Journal", styles['Heading2']))
                story.append(Spacer(1, 12))

                for category, entries in data.items():
                    story.append(Paragraph(f"<b>{category}:</b>", styles['Heading3']))
                    if not entries:
                        story.append(Paragraph("  Nenhuma entrada", styles['Normal']))
                    else:
                        for entry in entries:
                            story.append(Paragraph(f"  - {entry}", styles['Normal']))
                    story.append(Spacer(1, 6))

                # Seção de Objetivos Gerais
                story.append(Paragraph("Objetivos e Planejamento", styles['Heading2']))
                story.append(Spacer(1, 12))

                # Exportar todas as seções de objetivos_data
                for section, entries in objetivos_data.items():
                    story.append(Paragraph(f"<b>{section}:</b>", styles['Heading3']))
                    if not entries:
                        story.append(Paragraph("  Nenhuma entrada", styles['Normal']))
                    else:
                        for entry in entries:
                            story.append(Paragraph(f"  - {entry}", styles['Normal']))
                    story.append(Spacer(1, 6))

                # Adicionar data e hora de exportação
                story.append(Paragraph(f"Exportado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Italic']))

                # Salvar o PDF
                doc.build(story)
                QMessageBox.information(self, "Sucesso", "Todas as informações foram exportadas para PDF com sucesso!")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao exportar PDF: {e}")

    def edit_category_entry(self, list_widget, category):
        selected_item = list_widget.currentItem()
        if selected_item:
            entry = selected_item.text()
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Entrada")
            layout = QFormLayout(dialog)
            entry_input = QLineEdit(entry.split(" - ")[0])
            description_input = QTextEdit(entry.split(" - ")[1] if " - " in entry else "")
            layout.addRow("Entrada:", entry_input)
            layout.addRow("Descrição:", description_input)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            if dialog.exec_() == QDialog.Accepted:
                new_entry = entry_input.text()
                new_description = description_input.toPlainText()
                if new_entry != entry:
                    index = data[category].index(entry)
                    data[category][index] = f"{new_entry} - {new_description}"
                    self.update_category_list(category, list_widget)
                    QMessageBox.information(self, "Sucesso", "Dados editados com sucesso!")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item para editar.")

    def remove_category_entry(self, list_widget, category):
        selected_item = list_widget.currentItem()
        if selected_item:
            entry = selected_item.text()
            data[category].remove(entry)
            self.update_category_list(category, list_widget)
            QMessageBox.information(self, "Sucesso", "Dados removidos com sucesso!")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item para remover.")

    def update_objetivos_list(self):
        self.objetivos_list_widget.clear()
        for category, entries in objetivos_data.items():
            for entry in entries:
                item = QListWidgetItem(f"{category}: {entry}")
                self.objetivos_list_widget.addItem(item)

    def edit_objetivo(self):
        selected_item = self.objetivos_list_widget.currentItem()
        if selected_item:
            text = selected_item.text()
            category, entry = text.split(": ", 1)
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Objetivo")
            layout = QFormLayout(dialog)
            entry_input = QLineEdit(entry)
            layout.addRow("Entrada:", entry_input)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            if dialog.exec_() == QDialog.Accepted:
                new_entry = entry_input.text()
                if new_entry != entry:
                    index = objetivos_data[category].index(entry)
                    objetivos_data[category][index] = new_entry
                    self.update_objetivos_list()
                    QMessageBox.information(self, "Sucesso", "Objetivo editado com sucesso!")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item para editar.")

    def remove_objetivo(self):
        selected_item = self.objetivos_list_widget.currentItem()
        if selected_item:
            text = selected_item.text()
            category, entry = text.split(": ", 1)
            objetivos_data[category].remove(entry)
            self.update_objetivos_list()
            QMessageBox.information(self, "Sucesso", "Objetivo removido com sucesso!")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um item para remover.")

    def add_to_entry(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar na Entrada")
        layout = QFormLayout(dialog)

        # Adicionar um ComboBox para selecionar a seção
        section_label = QLabel("Selecione a seção:")
        section_combo = QComboBox()
        section_combo.addItems(objetivos_data.keys())  # Adiciona as seções disponíveis
        layout.addRow(section_label, section_combo)

        entry_input = QLineEdit()
        layout.addRow("Entrada:", entry_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            section = section_combo.currentText()
            new_entry = entry_input.text()
            if new_entry:
                objetivos_data[section].append(new_entry)
                self.update_objetivos_list()
                QMessageBox.information(self, "Sucesso", f"Entrada adicionada em '{section}' com sucesso!")
            else:
                QMessageBox.warning(self, "Aviso", "Preencha o campo de entrada.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BulletJournalApp()
    window.show()
    sys.exit(app.exec_())
