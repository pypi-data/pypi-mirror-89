from fastai.vision.all import *
from timm import create_model

def create_timm_body(arch:str, pretrained=True, cut=None):
    from timm import create_model
    model = create_model(arch, pretrained=pretrained)
    if cut is None:
        ll = list(enumerate(model.children()))
        cut = next(i for i,o in reversed(ll) if has_pool_type(o))
    if isinstance(cut, int): return nn.Sequential(*list(model.children())[:cut])
    elif callable(cut): return cut(model)
    else: raise NamedError("cut must be either integer or function")


def preprocess(input_data):
    # convert the input data into the float32 input
    img_data = input_data.astype('float32')

    #normalize
    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])
    norm_img_data = np.zeros(img_data.shape).astype('float32')
    for i in range(img_data.shape[0]):
        norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]

    #add batch channel
    norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
    return norm_img_data

def softmax(x):
    x = x.reshape(-1)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def postprocess(result):
    return softmax(np.array(result)).tolist()

# onnx-export
from fastai.learner import Learner
from fastcore.all import *
import torch
from torch import tensor, Tensor
#from fastinference.onnx import *
import onnxruntime as rt

# onnx-export
@patch
def to_onnx(x:Learner, fname='export', path=Path('.')):
    "Export model to `ONNX` format"
    orig_bs = x.dls[0].bs
    x.dls[0].bs=1
    dummy_inp = next(iter(x.dls[0]))
    x.dls[0].bs = orig_bs
    names = inspect.getfullargspec(x.model.forward).args[1:]
    dynamic_axes = {n:{0:'batch_size'} for n in names}
    dynamic_axes['output'] = {0:'batch_size'}
    torch.onnx.export(x.model, dummy_inp[:-1], path/f'{fname}.onnx',
                     input_names=names, output_names=['output'],
                     dynamic_axes=dynamic_axes)
    data_exp = x.dls.new_empty()
    data_exp.loss_func = x.loss_func
    torch.save(data_exp, path/f'{fname}.pkl', pickle_protocol=2)
