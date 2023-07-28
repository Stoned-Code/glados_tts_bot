import torch
from glados_tts.utils.tools import prepare_text
from scipy.io.wavfile import write
import time
import sys
from sys import modules as mod

try:
    import winsound
except ImportError:
    from subprocess import call


class GLaDOS:
    def __init__(self, device = None, verbose = False, model_path = 'glados_tts/models/glados.pt', vocoder_path = 'glados_tts/models/vocoder-gpu.pt'):
        if device == None:
            if torch.is_vulkan_available():
                self.device = 'vulkan'

            if torch.cuda.is_available():
                self.device = 'cuda'

            else:
                self.device = 'cpu'
        else:
            self.device = device

        self.verbose = verbose

        self.model_path = model_path
        self.vocoder_path = vocoder_path

        self.init_model()

        print('Finished loading GLaDOS model.')

    def init_model(self):
        self.model = torch.jit.load(self.model_path)
        self.vocoder = torch.jit.load(self.vocoder_path, map_location=self.device)

        for i in range(4):
            init = self.model.generate_jit(prepare_text(str(i)))
            init_mel = init['mel_post'].to(self.device)
            init_vo = self.vocoder(init_mel)

    def announce_function(self, func):
        def wrapper(*args, **kwargs):
            message = 'Executing {} function.'.format(func.__name__)
            self.tts(message)
            result = func(*args, **kwargs)
            if result != None:
                return result
        
        return wrapper
    

    def tts(self, text, save_tts = False, output_path = 'output.wav', play_sound = False):

        x = prepare_text(text).to('cpu')

        with torch.no_grad():
            tts_output = self.model.generate_jit(x)
            if self.verbose:
                old_time = time.time()
                print("Forward Tacotron took " + str((time.time() - old_time) * 1000) + "ms")   
            
            mel = tts_output['mel_post'].to(self.device)
            audio = self.vocoder(mel)

            if self.verbose:
                old_time = time.time()
                print("HiFiGAN took " + str((time.time() - old_time) * 1000) + "ms")

            audio = audio.squeeze()
            audio = audio * 32768.0
            audio = audio.cpu().numpy().astype('int16')

            output_file = (output_path)
            if save_tts:
                write(output_file, 22050, audio)
            
            if play_sound:
                if 'winsound' in mod:
                    winsound.PlaySound(output_file, winsound.SND_FILENAME)
                else:
                    call(['aplay', './{}'.format(output_file[0])])
            
            return audio


    def announce_function(self, func):
        def wrapper(*args, **kwargs):
            message = 'Executing {} function.'.format(func.__name__)
            self.tts(message)
            result = func(*args, **kwargs)

            if result != None:
                return result
        
        return wrapper


if __name__ == '__main__':
    glados = GLaDOS()
    tts = glados.tts(sys.argv[-1], save_tts = True)
    print(type(tts))