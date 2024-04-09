# ComicHub

## Descrição

**ComicHub** é uma plataforma que oferece acesso a uma vasta coleção de histórias em quadrinhos (HQs) e mangás, permitindo aos usuários explorar, descobrir e desfrutar de seus títulos favoritos em um único lugar. Com recursos avançados de organização e uma interface intuitiva, ComicHub oferece uma experiência de leitura imersiva para entusiastas de HQs e mangás.

## Instalação

### Clonar o Repositório

Para instalar ComicHub, clone o repositório do GitHub:

```bash
git clone https://github.com/Zer0G0ld/ComicHub
```

### Configurar Ambiente Virtual

Crie e ative um ambiente virtual Python:

```bash
python3 -m venv venv
```

Ative o ambiente virtual:

- **Linux/MacOS:**
```bash
source venv/bin/activate
```

- **Windows:**
```cmd
.\venv\Scripts\Activate
```

### Instalar Dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Compilar e Instalar no Dispositivo Android Usando Buildozer

1. **Compilar o Aplicativo:**

   Execute o seguinte comando para compilar o aplicativo:

   ```bash
   buildozer android debug
   ```

2. **Conectar Dispositivo Android:**

   Certifique-se de que o dispositivo Android esteja conectado ao computador via USB.

3. **Copiar APK para o Dispositivo:**

   Encontre o arquivo APK gerado no diretório `bin` do projeto e copie-o para o dispositivo Android.

4. **Instalar o Aplicativo:**

   No dispositivo Android, abra o gerenciador de arquivos, navegue até o local onde o APK foi copiado e toque no arquivo para iniciar a instalação.

5. **Executar o Aplicativo:**

   Após a instalação, localize o aplicativo na lista de aplicativos do dispositivo Android e toque no ícone para executá-lo.

Certifique-se de seguir esses passos cuidadosamente para compilar e instalar ComicHub em seu dispositivo Android.
