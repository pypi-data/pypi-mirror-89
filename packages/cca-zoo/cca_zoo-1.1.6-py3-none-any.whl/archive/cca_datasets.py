import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset
import torch.utils.data
from torchvision import datasets, transforms
import PIL
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from mvlearn.datasets import load_UCImultifeature
import warnings

warnings.filterwarnings("ignore")
plt.ion()


def OH_digits(digits):
    b = np.zeros((digits.size, digits.max() + 1))
    b[np.arange(digits.size), digits] = 1
    return b


class CCA_Dataset(Dataset):
    def __init__(self, *args, labels=None, train=True):
        self.train = train
        self.views = [MinMaxScaler().fit_transform(view) if len(view.shape)==2 else view for view in args]
        if labels is None:
            self.labels = np.zeros(len(self.views[0]))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        label = self.labels[idx]
        views = [view[idx] for view in self.views]
        return tuple(views), label

    def to_numpy(self, indices):
        labels = self.labels[indices]
        views = [view[indices] for view in self.views]
        OH_labels = OH_digits(labels.astype(int))
        return *views, OH_labels, labels


class Noisy_MNIST_Dataset(Dataset):
    def __init__(self, mnist_type='MNIST', train=True):

        if mnist_type == 'MNIST':
            self.dataset = datasets.MNIST('../../data', train=train, download=True)
        elif mnist_type == 'FashionMNIST':
            self.dataset = datasets.FashionMNIST('../../data', train=train, download=True)
        elif mnist_type == 'KMNIST':
            self.dataset = datasets.KMNIST('../../data', train=train, download=True)

        self.data = self.dataset.data
        self.base_transform = transforms.ToTensor()
        self.a_transform = transforms.Compose([transforms.ToTensor(),  # first, convert image to PyTorch tensor
                                               transforms.ToPILImage()
                                               #                 transforms.Normalize((self.mean,), (self.std,)) # normalize inputs
                                               ])
        self.b_transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Lambda(lambda x: x + torch.rand(28, 28)),
             transforms.Lambda(lambda x: self.__threshold_func__(x))])
        self.targets = self.dataset.targets
        self.filtered_classes = []
        self.filtered_nums = []
        for i in range(10):
            self.filtered_classes.append(self.data[self.targets == i])
            self.filtered_nums.append(self.filtered_classes[i].shape[0])

    def __threshold_func__(self, x):
        x[x > 1] = 1
        return x

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x_a = self.a_transform(self.data[idx].numpy())
        rot_a = torch.rand(1) * 90 - 45
        x_a = transforms.functional.rotate(x_a, rot_a.item(), resample=PIL.Image.BILINEAR)
        x_a = self.base_transform(x_a)  # convert from PIL back to pytorch tensor

        label = self.targets[idx]
        # get random index of image with same class
        random_index = np.random.randint(self.filtered_nums[label])
        x_b = Image.fromarray(self.filtered_classes[label][random_index, :, :].numpy(), mode='L')
        x_b = self.b_transform(x_b)
        OH_label = OH_digits(label.astype(int))
        return (x_a, x_b, rot_a, OH_label), label

    def to_numpy(self, N=1000):
        view_1 = np.zeros((N, 784))
        view_2 = np.zeros((N, 784))
        labels = np.zeros(N).astype(int)
        rotations = np.zeros(N)
        for n in range(N):
            sample = self[n]
            view_1[n] = sample[0][0].numpy().reshape((-1, 28 * 28))
            view_2[n] = sample[0][1].numpy().reshape((-1, 28 * 28))
            rotations[n] = sample[0][2].numpy()
            labels[n] = sample[1].numpy().astype(int)
        OH_labels = OH_digits(labels.astype(int))
        return view_1, view_2, rotations, OH_labels, labels


class Tangled_MNIST_Dataset(Dataset):
    def __init__(self, mnist_type='MNIST', train=True, fixed=False):

        if mnist_type == 'MNIST':
            self.dataset = datasets.MNIST('../../data', train=train, download=True)
        elif mnist_type == 'FashionMNIST':
            self.dataset = datasets.FashionMNIST('../../data', train=train, download=True)
        elif mnist_type == 'KMNIST':
            self.dataset = datasets.KMNIST('../../data', train=train, download=True)

        self.data = self.dataset.data
        self.mean = torch.mean(self.data.float())
        self.std = torch.std(self.data.float())
        self.transform = transforms.Compose([transforms.ToTensor(),  # first, convert image to PyTorch tensor
                                             #                     transforms.Lambda(lambda x: x/255.),
                                             #                 transforms.Normalize((self.mean,), (self.std,)) # normalize inputs
                                             ])
        self.targets = self.dataset.targets
        self.fixed = fixed
        self.filtered_classes = []
        self.filtered_nums = []
        for i in range(10):
            self.filtered_classes.append(self.data[self.targets == i])
            self.filtered_nums.append(self.filtered_classes[i].shape[0])
        if fixed:
            self.view_b_indices = []
            for i in range(10):
                self.view_b_indices.append(np.random.permutation(np.arange(len(self.data))[self.targets == i]))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # get first image from idx and second of same class
        label = self.targets[idx]
        x_a = Image.fromarray(self.data[idx].numpy(), mode='L')
        # get random index of image with same class
        random_index = np.random.randint(self.filtered_nums[label])
        x_b = Image.fromarray(self.filtered_classes[label][random_index, :, :].numpy(), mode='L')
        # get random angles of rotation
        rot_a, rot_b = torch.rand(2) * 90 - 45
        x_a_rotate = transforms.functional.rotate(x_a, rot_a.item(), resample=PIL.Image.BILINEAR)
        x_b_rotate = transforms.functional.rotate(x_b, rot_b.item(), resample=PIL.Image.BILINEAR)
        # convert images to tensors
        x_a_rotate = self.transform(x_a_rotate)
        x_b_rotate = self.transform(x_b_rotate)

        return (x_a_rotate, x_b_rotate, rot_a, rot_b), label

    def to_numpy(self, N=1000):
        view_1 = np.zeros((N, 784))
        view_2 = np.zeros((N, 784))
        labels = np.zeros(N).astype(int)
        rotation_1 = np.zeros(N)
        rotation_2 = np.zeros(N)
        for n in range(N):
            sample = self[n]
            view_1[n] = sample[0][0].numpy().reshape((-1, 28 * 28))
            view_2[n] = sample[0][1].numpy().reshape((-1, 28 * 28))
            rotation_1[n] = sample[0][2].numpy()
            rotation_2[n] = sample[0][3].numpy()
            labels[n] = sample[1].numpy().astype(int)
        OH_labels = OH_digits(labels.astype(int))
        return view_1, view_2, rotation_1, rotation_2, OH_labels, labels


class UCI_Dataset(Dataset):
    def __init__(self, train=True):
        full_data, self.labels = load_UCImultifeature()
        self.train = train
        self.view_1, self.view_2, self.view_3, self.view_4, self.view_5, self.view_6 = full_data
        self.view_1 = MinMaxScaler().fit_transform(self.view_1)
        self.view_2 = MinMaxScaler().fit_transform(self.view_2)
        self.view_3 = MinMaxScaler().fit_transform(self.view_3)
        self.view_4 = MinMaxScaler().fit_transform(self.view_4)
        self.view_5 = MinMaxScaler().fit_transform(self.view_5)
        self.view_6 = MinMaxScaler().fit_transform(self.view_6)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        label = self.labels[idx]
        view_1 = self.view_1[idx]
        view_2 = self.view_2[idx]
        view_3 = self.view_3[idx]
        view_4 = self.view_4[idx]
        view_5 = self.view_5[idx]
        view_6 = self.view_6[idx]
        return (view_1, view_2, view_3, view_4, view_5, view_6), label

    def to_numpy(self, indices):
        labels = self.labels[indices]
        view_1 = self.view_1[indices]
        view_2 = self.view_2[indices]
        view_3 = self.view_3[indices]
        view_4 = self.view_4[indices]
        view_5 = self.view_5[indices]
        view_6 = self.view_6[indices]
        OH_labels = OH_digits(labels.astype(int))
        return view_1, view_2, view_3, view_4, view_5, view_6, OH_labels, labels
