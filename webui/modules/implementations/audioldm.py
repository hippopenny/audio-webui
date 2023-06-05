import gc
import os.path

import diffusers
import torch.cuda

model: diffusers.AudioLDMPipeline = None
loaded = False


def create_model(pretrained='cvssp/audioldm-m-full', device='cuda' if torch.cuda.is_available() else 'cpu'):
    if is_loaded():
        delete_model()
    global model, loaded
    model = diffusers.AudioLDMPipeline.from_pretrained(pretrained, cache_dir=os.path.join('data', 'models', 'audioldm')).to(device)
    loaded = True


def delete_model():
    global model, loaded
    del model
    gc.collect()
    torch.cuda.empty_cache()
    loaded = False


def is_loaded():
    return loaded


def generate(prompt='', negative_prompt='', steps=10, duration=5.0, cfg=2.5):
    if is_loaded():
        return 16000, model(prompt if prompt else None, negative_prompt=negative_prompt if negative_prompt else None,
                            audio_length_in_s=duration, num_inference_steps=steps, guidance_scale=cfg).audios[0]
    return 'No model loaded! Please load a model first.'