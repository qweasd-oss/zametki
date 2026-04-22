from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QListWidget,
    QLineEdit,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog,
    
    )
import json
# Инициализация
app = QApplication([])
notes_win = QWidget()




with open('notes_data.json', 'r') as f:
    notes = json.load(f)


#Виджеты
note_info_widget = QTextEdit()
note_list_label_widget = QLabel(text='Список заметок')
note_list_widget = QListWidget()
create_note_widget = QPushButton(text='Создать заметку')
delete_note_widget = QPushButton(text='Удалить заметку')
save_note_widget = QPushButton(text='Сохранить заметку')

tag_list_label_widget = QLabel(text='Список тегов')
tag_list_widget = QListWidget()
tag_input_widget = QLineEdit(text='Введите тег...')
add_tag_widget = QPushButton(text='Добавить к заметке')
delete_tag_widget = QPushButton(text='Открепить от заметки')
search_tag_widget = QPushButton(text='Искать заметки по тегу')

#Настройки виджетов
for key in notes:
    note_list_widget.addItem(key)


#Слои
main_layout = QHBoxLayout()
settings_layout = QVBoxLayout()
settings_note = QVBoxLayout()
settings_note_buttons = QHBoxLayout()

setting_tag = QVBoxLayout()
settings_tag_buttons = QHBoxLayout()

#Заполнение слоев
main_layout.addWidget(note_info_widget)
settings_note_buttons.addWidget(create_note_widget)
settings_note_buttons.addWidget(delete_note_widget)
settings_note.addWidget(note_list_label_widget)
settings_note.addWidget(note_list_widget)
settings_note.addLayout(settings_note_buttons)
settings_note.addWidget(save_note_widget)

settings_tag_buttons.addWidget(add_tag_widget)
settings_tag_buttons.addWidget(delete_tag_widget)
setting_tag.addWidget(tag_list_label_widget)
setting_tag.addWidget(tag_list_widget)
setting_tag.addWidget(tag_input_widget)
setting_tag.addLayout(settings_tag_buttons)
setting_tag.addWidget(search_tag_widget)



settings_layout.addLayout(settings_note)
settings_layout.addLayout(setting_tag)
main_layout.addLayout(settings_layout)
notes_win.setLayout(main_layout)

def select_note():
    note_text = note_list_widget.selectedItems()[0].text()
    note_info_widget.clear()
    note_info_widget.setText(notes[note_text]['текст'])
    tags = notes[note_text]['теги']
    tag_list_widget.clear()
    for tag in tags:
        tag_list_widget.addItem(tag)

def delete_note():
    note_text = note_list_widget.selectedItems()[0].text()
    del notes[note_text]
    note_list_widget.clear()
    tag_list_widget.clear()
    note_info_widget.clear()
    for key in notes:
        note_list_widget.addItem(key)




def save_note():
    note_text = note_list_widget.selectedItems()[0].text()
    main_text = note_info_widget.toPlainText()
    notes[note_text]['текст'] = main_text
    
def create_note():
    new_note_text, btn_ok_is_clicked = QInputDialog.getText(
        notes_win, 'Новая заметка', 'Название заметки:'
    )
    if btn_ok_is_clicked and new_note_text != '':
        notes[new_note_text] = {'текст': '', 'теги': []}
        note_list_widget.clear()
        tag_list_widget.clear()
        note_info_widget.clear()
        for key in notes:
            note_list_widget.addItem(key)

def delete_tag():
    tag_text = tag_list_widget.selectedItems()[0].text()
    note_text = note_list_widget.selectedItems()[0].text()
    notes[note_text]['теги'].remove(tag_text)
    tag_list_widget.clear()
    tags = notes[note_text]['теги']
    for tag in tags:
        tag_list_widget.addItem(tag)

def add_tag():
    new_tag = tag_input_widget.text()
    if new_tag != '':
        note_text = note_list_widget.selectedItems()[0].text()
        notes[note_text]['теги'].append(new_tag)
        tag_list_widget.clear()
        tag_input_widget.clear()
        tags = notes[note_text]['теги']
        for tag in tags:
            tag_list_widget.addItem(tag)

def search_by_tag():
    tag = tag_input_widget.text()
    note_list_widget.clear()
    tag_list_widget.clear()
    note_info_widget.clear()

    if tag != '':
        for k, v in notes.items():
            if tag in v['теги']:
                note_list_widget.addItem(k)
    else:
        for key in notes:
            note_list_widget.addItem(key)



#Подключение функций
note_list_widget.itemClicked.connect(select_note)
delete_note_widget.clicked.connect(delete_note)
save_note_widget.clicked.connect(save_note)
create_note_widget.clicked.connect(create_note)
delete_tag_widget.clicked.connect(delete_tag)
add_tag_widget.clicked.connect(add_tag)
search_tag_widget.clicked.connect(search_by_tag)

#Запуск приложения
notes_win.show()
app.exec()

with open('notes_data.json', 'w') as f:
    json.dump(notes, f)