import fnmatch
import logging
import subprocess

from .base import Plugin
from .file_transfer import FileTransferPlugin
from ..common import *


class FileOpenPlugin(Plugin):
    """Open files or URLs from client"""
    MARK = b'open'
    NAME = 'FileOpenPlugin'
    MAIN_CONF = dict()
    DEVICE_CONFS = dict()
    CONFIG_SCHEMA = DictEntry('open.conf.json', 'Common configuration for open file plugin', False, entries=(
        IntEntry('uin', 'UIN of device for which config will be applied', True, 1, 0xFFFFFFF, None),
        DirEntry('download_directory', 'Directory to store files and data to show', False, '/tmp/dcnnt', True, False),
        TemplateEntry('default_open_cmd', 'Default command to open file', False, 0, 4096, 'xdg-open "{path}"',
                      replacements=(Rep('path', 'Path to saved file', True),))
    ))
    PART = FileTransferPlugin.PART

    def handle_open_file(self, request):
        """Receive and show file from client"""
        try:
            name, size = request.params['name'], request.params['size']
        except KeyError as e:
            self.log('KeyError {}'.format(e), logging.WARN)
        else:
            path = os.path.join(self.conf('download_directory'), name)
            self.log('Receiving {} bytes to file {}'.format(size, path))
            self.rpc_send(RPCResponse(request.id, dict(code=0, message='OK')))
            f = open(path, 'wb')
            wrote = 0
            while wrote < size:
                buf = self.read()
                if buf is None:
                    self.log('File receiving aborted ({} bytes received)'.format(wrote), logging.WARN)
                    return
                if len(buf) == 0:
                    req = self.rpc_read()
                    if req.method == "cancel":
                        self.log('File receiving canceled by client ({} bytes received)'.format(wrote), logging.INFO)
                        f.close()
                        self.rpc_send(RPCResponse(request.id, dict(code=1, message='Canceled')))
                        return
                wrote += len(buf)
                f.write(buf)
            f.close()
            self.log('File received ({} bytes)'.format(wrote), logging.INFO)
            self.rpc_send(RPCResponse(request.id, dict(code=0, message='OK')))
            on_download = self.conf('on_download')
            if isinstance(on_download, str):
                command = on_download.format(path=path)
                self.log('Execute: "{}"'.format(command))
                subprocess.call(command, shell=True)

    def main(self):
        while True:
            request = self.rpc_read()
            self.log(request)
            if request is None:
                self.log('[FileTransferPlugin] No more requests, stop handler')
                return
            if request.method == 'file':
                self.handle_list_shared(request)
            elif request.method == 'download':
                self.handle_download(request)
            elif request.method == 'upload':
                self.handle_upload(request)
