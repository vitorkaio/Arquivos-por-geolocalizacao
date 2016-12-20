# Include the Dropbox SDK
import dropbox

class ClienteDropbox:
    def __init__(self, key, secret, t):
        self.__app_key = key
        self.__app_secret = secret
        self.__token = t

        self.__flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.__app_key, self.__app_secret)
        self.__authorize_url = self.__flow.start()
        self.__access_token = self.__token
        self.__client = dropbox.client.DropboxClient(self.__access_token)

    def upar_arquivo(self, path_arquivo):
        try:
            f = open(path_arquivo, 'rb')
            response = self.__client.put_file('/' + path_arquivo, f)
            f.close()
            print '\n\n **** Ok: Upload feito com sucesso!!! \n\n\n'
            return True
        except Exception as err:
            print '\n\n **** Erro: ' + str(err) + '\n\n\n'
            return False

    def deletar_arquivo(self,path_arquivo):
        try:
            response = self.__client.file_delete('/' + path_arquivo)
            print '\n\n **** Ok: Deletado com sucesso!!! \n\n\n'
            return True
        except Exception as err:
            print '\n\n **** Erro: ' + str(err) + '\n\n\n'
            return False


    def baixar_arquivo(self, path_arquivo):
        try:
            f, metadata = client.get_file_and_metadata('/' + path_arquivo)
            out = open(path_arquivo, 'wb')
            out.write(f.read())
            out.close
        except:
            return False


drop = ClienteDropbox('1692g9q0jaw1wlc', 'prgrzslwkz3agx0', 'aX3GwV9NdSAAAAAAAAAACyJrla-sLiowwiT5sg3KbUT6fc8QbZdA0IWDwodinit0')

'''def baixar_arquivo(path_arquivo):
	f, metadata = client.get_file_and_metadata('/' + path_arquivo)
	out = open(path_arquivo, 'wb')
	out.write(f.read())
	out.close()
	print metadata


def upar_arquivo(path_arquivo):
	f = open(path_arquivo, 'rb')
	response = client.put_file('/' + path_arquivo, f)
	print "uploaded:", response

# Get your app key and secret from the Dropbox developer website
app_key = '1692g9q0jaw1wlc'
app_secret = 'prgrzslwkz3agx0'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()

access_token = 'aX3GwV9NdSAAAAAAAAAACyJrla-sLiowwiT5sg3KbUT6fc8QbZdA0IWDwodinit0'

client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

#folder_metadata = client.metadata('/')
#print "metadata:", folder_metadata


op = raw_input('1 - upar\n2 - download\nopcao: ')

if op == '1':
	upar_arquivo(raw_input('arquivo: '))

else:
	baixar_arquivo(raw_input('arquivo: '))'''
