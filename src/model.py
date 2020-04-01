import io
import torch
import torch.nn as nn
from PIL import Image
from collections import OrderedDict
from torch.utils import model_zoo
from torchvision import transforms

MODEL_URLS = "http://ml.cs.tsinghua.edu.cn/~chenxi/pytorch-models/mnist-b07bb66b.pth"

trained_model_transformers = transforms.Compose(
    [
        # transforms.Resize(255),
        # transforms.CenterCrop(224),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


class MLP(nn.Module):
    def __init__(self, input_dims, n_hiddens, n_class):
        super(MLP, self).__init__()
        assert isinstance(input_dims, int), "Please provide int for input_dims"
        self.input_dims = input_dims
        current_dims = input_dims
        layers = OrderedDict()

        if isinstance(n_hiddens, int):
            n_hiddens = [n_hiddens]
        else:
            n_hiddens = list(n_hiddens)
        for i, n_hidden in enumerate(n_hiddens):
            layers["fc{}".format(i + 1)] = nn.Linear(current_dims, n_hidden)
            layers["relu{}".format(i + 1)] = nn.ReLU()
            layers["drop{}".format(i + 1)] = nn.Dropout(0.2)
            current_dims = n_hidden
        layers["out"] = nn.Linear(current_dims, n_class)
        self.model = nn.Sequential(layers)

    def forward(self, input):
        input = input.view(input.size(0), -1)
        assert input.size(1) == self.input_dims
        return self.model.forward(input)


def get_model():
    model = MLP(784, [256, 256], 10)
    m = model_zoo.load_url(
        MODEL_URLS, model_dir="instance", map_location=torch.device("cpu")
    )
    state_dict = m.state_dict() if isinstance(m, nn.Module) else m
    assert isinstance(state_dict, (dict, OrderedDict)), type(state_dict)
    model.load_state_dict(state_dict)
    return model


def process_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return trained_model_transformers(image)


def predict(trained_model, image_bytes):
    datas = process_image(image_bytes)
    output = trained_model(datas)
    prediction_ranked = output.data.sort(1, descending=True)[1]
    prediction_first = prediction_ranked[:, :1].flatten().item()
    return prediction_first
