import os
import shutil
import subprocess
import threading

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar

class ComicManager:
    @staticmethod
    def add_book(repo_dir):
        # Verifica se o diretório 'repo' existe e o cria se não existir
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)

        # Cria uma nova instância do FileChooser para selecionar arquivos
        file_chooser = FileChooserListView()

        # Define o diretório inicial como o diretório 'Downloads'
        file_chooser.path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Permite a seleção de múltiplos arquivos
        file_chooser.multiselect = True

        # Exibe apenas arquivos de imagem e CBR
        file_chooser.filters = [
            lambda folder, filename: filename.lower().endswith(('.cbr'))
        ]

        # Habilita a pesquisa pelo nome do arquivo
        file_chooser.search = True

        # Cria uma janela pop-up para exibir o FileChooser
        popup = Popup(title='Selecione a(s) HQ(s)/Mangá(s)', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

        # Associa o evento de seleção ao manipulador de seleção
        file_chooser.bind(on_submit=lambda instance, selection, touch: ComicManager.select_hq_manga(instance, selection, touch, popup, repo_dir))


    @staticmethod
    def select_hq_manga(instance, selection, touch, popup, repo_dir):
        def copy_files():
            total_size = sum(os.path.getsize(file_path) for file_path in selection)
            progress_bar = ProgressBar(max=total_size, size_hint_y=None)

            message_box = BoxLayout(orientation='vertical')
            message_box.add_widget(Label(text='Copying files...'))
            message_box.add_widget(progress_bar)

            message_popup = Popup(title="Progess", content=message_box, size_hint=(None, None), size=(400, 200))
            message_popup.open()

            try:
                copied_bytes = 0
                for file_path in selection:
                    shutil.copy(file_path, repo_dir)
                    copied_bytes += os.path.getsize(file_path)
                    progress_bar.value = copied_bytes
                
                message_box.clear_widgets()
                message_box.add_widget(Label(text="Files copied sucessfully to 'repo' directory!"))
            except Exception as e:
                message_box.clear_widgets()
                message_box.add_widget(Label(text=f"Error copying files: {e}"))

            App.get_running_app().root_window.after(2, message_popup.dismiss)
            popup.dismiss() # Fecha a janela pop-up de seleção de arquivo após a cópia

        threading.Thread(target=copy_files).start()
    
    @staticmethod
    def view_book(layout):
        # Verifica se há arquivos no diretório 'repo'
        repo_dir = os.path.join(os.getcwd(), 'repo')
        if not os.path.exists(repo_dir) or not os.listdir(repo_dir):
            print("Nenhum HQ/Mangá encontrado para visualização.")
            return

        # Obtém a lista de arquivos no diretório 'repo'
        files = os.listdir(repo_dir)

        # Extrai imagens dos arquivos .cbr e adiciona à lista de arquivos de imagem
        image_files = []
        for file in files:
            if file.lower().endswith('.cbr'):
                # Extrai imagens do arquivo .cbr
                extracted_images = ComicManager.extract_images_from_cbr(repo_dir, file)
                if extracted_images:
                    image_files.extend(extracted_images)

        # Verifica se há arquivos de imagem para exibir
        if not image_files:
            print("Nenhum arquivo de imagem encontrado para visualização.")
            return

        # Limpa os widgets atuais
        layout.clear_widgets()

        # Cria um GridLayout para organizar as imagens em uma grade
        grid_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Adiciona as imagens à grade
        for file_name in image_files:
            image_path = os.path.join(repo_dir, file_name)
            image_widget = Image(source=image_path, size_hint_y=None)
            image_widget.height = dp(200)  # Ajusta a altura da imagem
            grid_layout.add_widget(image_widget)

            # Adiciona um botão "Adicionar" para cada imagem
            add_button = Button(text='Adicionar', size_hint_y=None, height=dp(50))
            add_button.bind(on_press=lambda instance: ComicManager.add_hq_manga(file_name, repo_dir))
            grid_layout.add_widget(add_button)

        # Adiciona a grade a um ScrollView para permitir rolagem vertical
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(grid_layout)

        # Adiciona botões de navegação
        navigation_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        previous_button = Button(text='Página Anterior', size_hint_x=0.5)
        next_button = Button(text='Próxima Página', size_hint_x=0.5)
        navigation_layout.add_widget(previous_button)
        navigation_layout.add_widget(next_button)
        grid_layout.add_widget(navigation_layout)

        layout.add_widget(scroll_view)


    @staticmethod
    def add_hq_manga(file_name, repo_dir):
        # Verifica se o arquivo já existe no diretório de destino
        destination_file = os.path.join(repo_dir, file_name)
        if os.path.exists(destination_file):
            print(f'O arquivo "{file_name}" já existe no diretório de destino.')
            return

        # Copia o arquivo selecionado para o diretório de destino
        selected_file = os.path.join(repo_dir, file_name)
        try:
            shutil.copy(selected_file, repo_dir)
            print(f'O arquivo "{file_name}" foi adicionado com sucesso.')
        except Exception as e:
            print(f'Erro ao adicionar o arquivo "{file_name}": {e}')


    @staticmethod
    def extract_images_from_cbr(directory, cbr_file):
        # Cria um diretório temporário para extrair as imagens
        temp_dir = os.path.join(directory, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        try:
            # Extrai as imagens do arquivo .cbr para o diretório temporário
            subprocess.run(['unrar', 'x', os.path.join(directory, cbr_file), temp_dir])
        except Exception as e:
            print(f"Erro ao extrair as imagens do arquivo .cbr: {e}")
            return None

        # Obtém a lista de arquivos extraídos
        extracted_files = os.listdir(temp_dir)

        # Filtra os arquivos de imagem
        image_files = [f for f in extracted_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.cbr'))]

        # Move os arquivos de imagem para o diretório principal
        for image_file in image_files:
            shutil.move(os.path.join(temp_dir, image_file), os.path.join(directory, image_file))

        # Remove o diretório temporário
        shutil.rmtree(temp_dir)

        return image_files

class ComicHubApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Adiciona título ao topo do layout
        self.title = "ComicHub"
        title_label = Label(text=self.title, size_hint_y=None, height=dp(100), font_size=40)
        self.layout.add_widget(title_label)

        self.layout.add_widget(Label(size_hint_y=None, height=dp(20))) # Adiciona espaçamento

        # Adiciona botões para adicionar e visualizar HQs/Mangás
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        add_button = Button(text='Adicionar Livro', size_hint_x=0.5, font_size=18)
        add_button.bind(on_press=lambda instance: ComicManager.add_book(os.path.join(os.getcwd(), 'repo')))
        view_button = Button(text='Visualizar Livro', size_hint_x=0.5, font_size=18)
        view_button.bind(on_press=lambda instance: ComicManager.view_book(self.layout))
        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(view_button)
        self.layout.add_widget(buttons_layout)

        return self.layout

if __name__ == '__main__':
    ComicHubApp().run()
