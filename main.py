import os
import shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label  
from kivy.metrics import dp
from zipfile import ZipFile

class HQMangaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Adiciona título ao topo do layout
        self.title = "Leitor de HQs e Mangás | Zer0"
        title_label = Label(text=self.title, size_hint_y=None, height=dp(100), font_size=40)
        self.layout.add_widget(title_label)

        # Adiciona espaçamento
        self.layout.add_widget(Label(size_hint_y=None, height=dp(20)))

        # Adiciona botões para adicionar e visualizar HQs/Mangás
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        add_button = Button(text='Adicionar HQ/Mangá', size_hint_x=0.5, font_size=18)
        add_button.bind(on_press=self.add_hq_manga)
        view_button = Button(text='Visualizar HQs/Mangás', size_hint_x=0.5, font_size=18)
        view_button.bind(on_press=self.view_hq_manga)
        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(view_button)
        self.layout.add_widget(buttons_layout)

        return self.layout

    def add_hq_manga(self, instance):
        # Cria uma nova instância do FileChooser para selecionar arquivos
        file_chooser = FileChooserListView()

        # Define o diretório inicial como o diretório 'Downloads'
        file_chooser.path = "/storage/emulated/0/Download"

        # Permite a seleção de múltiplos arquivos
        file_chooser.multiselect = True

        # Exibe apenas arquivos de imagem
        file_chooser.filters = [lambda folder, filename: filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        # Habilita a pesquisa pelo nome do arquivo
        file_chooser.search = True

        # Cria uma janela pop-up para exibir o FileChooser
        popup = Popup(title='Selecione a(s) HQ(s)/Mangá(s)', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

        # Associa o evento de seleção ao manipulador de seleção
        file_chooser.bind(on_submit=lambda instance, selection, touch: self.select_hq_manga(instance, selection, touch, popup))

    def select_hq_manga(self, instance, selection, touch, popup):
        # Verifica se um arquivo foi selecionado e o adiciona à lista de HQs/mangás
        if selection:
            hq_manga_files = selection
            # Cria um arquivo ZIP para armazenar as imagens selecionadas
            with ZipFile('hq_mangas.cbr', 'w') as zipf:
                for file_path in hq_manga_files:
                    zipf.write(file_path, os.path.basename(file_path))
            print('Arquivos adicionados e compactados com sucesso.')
        popup.dismiss()  # Fecha a janela pop-up após a seleção

    def view_hq_manga(self, instance):
        # Verifica se o arquivo compactado 'hq_mangas.cbr' existe
        hq_manga_file = os.path.join(os.getcwd(), 'hq_mangas.cbr')
        if not os.path.exists(hq_manga_file):
            print("Arquivo 'hq_mangas.cbr' não encontrado.")
            return

        # Lista todos os arquivos de HQs/mangás compactados na pasta do aplicativo e os exibe na interface do usuário
        self.layout.clear_widgets()  # Limpa os widgets atuais

        # Exibe o arquivo compactado
        image_widget = Image(source='hq_mangas.cbr', size_hint_y=None, height=dp(300))
        self.layout.add_widget(image_widget)

if __name__ == '__main__':
    HQMangaApp().run()
      
