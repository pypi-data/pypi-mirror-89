import copy

import torch.utils.data
from torch.nn import functional as F
from sklearn.cross_decomposition import CCA
from torch import optim
from torch.utils.data import TensorDataset, DataLoader

from CCA_methods_multi.DCCAE import DCCAE, DGCCAE
from CCA_methods_multi.DVCCA import DVCCA, DVCCA_p
from CCA_methods_multi.plot_utils import *


class Wrapper:

    def __init__(self, outdim_size=2, learning_rate=1e-3, epoch_num=1, batch_size=100,
                 reg_par=1e-5, use_all_singular_values=True, method='DCCAE', lam=0, both_encoders=False,
                 print_batch=False, patience=10):
        self.outdim_size = outdim_size
        self.learning_rate = learning_rate
        self.epoch_num = epoch_num
        # Default - may change during training due to needing batch size greater than 1
        self.batch_size = batch_size
        # the regularization parameter of the network
        # seems necessary to avoid the gradient exploding especially when non-saturating activations are used
        self.reg_par = reg_par
        self.use_all_singular_values = use_all_singular_values
        self.method = method
        self.lam = lam
        self.both_encoders = both_encoders
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.log_interval = 10
        self.print_batch = print_batch
        self.patience = patience

    def fit(self, X_train, Y_train):

        if self.method == 'DCCAE':
            self.model = DCCAE(input_size_1=X_train.shape[1], input_size_2=Y_train.shape[1], lam=self.lam,
                               outdim_size=self.outdim_size).double().to(self.device)
        if self.method == 'DGCCAE':
            self.model = DGCCAE(X_train.shape[1], Y_train.shape[1], lam=self.lam,
                                outdim_size=self.outdim_size).double().to(self.device)
        elif self.method == 'DVCCA':
            self.model = DVCCA(input_size_1=X_train.shape[1], input_size_2=Y_train.shape[1],
                               both_encoders=self.both_encoders, outdim_size=self.outdim_size).double().to(self.device)
        elif self.method == 'DVCCA_p':
            self.model = DVCCA_p(input_size_1=X_train.shape[1], input_size_2=Y_train.shape[1],
                                 both_encoders=self.both_encoders, outdim_size=self.outdim_size).double().to(
                self.device)
        num_subjects = X_train.shape[0]
        all_inds = np.arange(num_subjects)
        np.random.shuffle(all_inds)
        train_inds, val_inds = np.split(all_inds, [int(round(0.8 * num_subjects, 0))])
        X_val = X_train[val_inds]
        Y_val = Y_train[val_inds]
        X_train = X_train[train_inds]
        Y_train = Y_train[train_inds]
        # Demeaning
        self.X_mean = X_train.mean(axis=0)
        self.Y_mean = Y_train.mean(axis=0)
        X_train -= self.X_mean
        Y_train -= self.Y_mean
        X_val -= self.X_mean
        Y_val -= self.Y_mean

        tensor_x_train = torch.DoubleTensor(X_train)  # transform to torch tensor
        tensor_y_train = torch.DoubleTensor(Y_train)
        train_dataset = TensorDataset(tensor_x_train, tensor_y_train)  # create your datset
        train_dataloader = DataLoader(train_dataset, batch_size=len(train_dataset))
        tensor_x_val = torch.DoubleTensor(X_val)  # transform to torch tensor
        tensor_y_val = torch.DoubleTensor(Y_val)
        val_dataset = TensorDataset(tensor_x_val, tensor_y_val)  # create your datset
        val_dataloader = DataLoader(val_dataset, batch_size=len(val_dataset))

        while X_train.shape[0] % self.batch_size < 10 or Y_train.shape[0] % self.batch_size < 10:
            self.batch_size += 1

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        min_val_loss = 0
        early_stop = False
        epoch_train_loss = []
        epoch_val_loss = []

        for epoch in range(self.epoch_num):
            if early_stop == False:
                self.model.train()
                train_loss = 0
                for batch_idx, (x, y) in enumerate(train_dataloader):
                    self.optimizer.zero_grad()
                    x, y = x.to(self.device), y.to(self.device)
                    self.optimizer.zero_grad()
                    model_outputs = self.model(x, y)
                    loss = self.model.loss(x, y, *model_outputs)
                    loss.backward()
                    train_loss += loss.item()
                    self.optimizer.step()

                print('====> Epoch: {} Average train loss: {:.4f}'.format(
                    epoch, train_loss / len(train_dataloader)))

                self.model.eval()
                with torch.no_grad():
                    val_loss = 0
                    for batch_idx, (x, y) in enumerate(val_dataloader):
                        x, y = x.to(self.device), y.to(self.device)
                        model_outputs = self.model(x, y)
                        loss = self.model.loss(x, y, *model_outputs)
                        val_loss += loss.item()

                    print('====> Epoch: {} Average val loss: {:.4f}'.format(
                        epoch, val_loss / len(val_dataloader)))

                if val_loss < min_val_loss:
                    min_val_loss = val_loss
                    best_model = copy.deepcopy(self.model.state_dict())
                    print('Min loss %0.2f' % min_val_loss)
                    epochs_no_improve = 0

                else:
                    epochs_no_improve += 1
                    # Check early stopping condition
                    if epochs_no_improve == self.patience:
                        print('Early stopping!')
                        early_stop = True
                        self.model.load_state_dict(best_model)

                epoch_train_loss.append(train_loss / len(train_dataloader))
                epoch_val_loss.append(val_loss / len(val_dataloader))
        plot_training_loss(epoch_train_loss, epoch_val_loss)

        if self.method == 'DCCAE':
            self.train_correlations = self.predict_corr(X_train, Y_train, train=True)

        self.train_recon_loss_x, self.train_recon_loss_y = self.predict_recon(X_train, Y_train)

        return self

    def predict_corr(self, X_test, Y_test, train=False):
        tensor_x_test = torch.DoubleTensor(X_test).to(self.device)  # transform to torch tensor
        tensor_y_test = torch.DoubleTensor(Y_test).to(self.device)
        test_dataset = TensorDataset(tensor_x_test, tensor_y_test)  # create your datset
        test_dataloader = DataLoader(test_dataset, batch_size=100)
        z_x = np.empty((0, self.outdim_size))
        z_y = np.empty((0, self.outdim_size))
        with torch.no_grad():
            for batch_idx, (x, y) in enumerate(test_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                if self.method == 'DCCAE':
                    z_x_batch, z_y_batch, recon_x_batch, recon_y_batch = self.model(x, y)
                elif self.method == 'DVCCA':
                    if self.both_encoders:
                        recon_batch_1, recon_batch_2, z_x_batch, logvar_x, z_y_batch, logvar_y = self.model(
                            tensor_x_test.to(self.device),
                            tensor_y_test.to(self.device))
                    else:
                        print('No correlation method for single encoding')
                        return
                z_x = np.append(z_x, z_x_batch.detach().cpu().numpy(), axis=0)
                z_y = np.append(z_y, z_y_batch.detach().cpu().numpy(), axis=0)
        if train:
            self.cca = CCA(n_components=self.outdim_size)
            view_1, view_2 = self.cca.fit_transform(z_x, z_y)
        else:
            view_1, view_2 = self.cca.transform(np.array(z_x), np.array(z_y))
        correlations = np.diag(np.corrcoef(view_1, view_2, rowvar=False)[:self.outdim_size, self.outdim_size:])
        return correlations

    def predict_recon(self, X_test, Y_test):
        tensor_x_test = torch.DoubleTensor(X_test).to(self.device)  # transform to torch tensor
        tensor_y_test = torch.DoubleTensor(Y_test).to(self.device)
        test_dataset = TensorDataset(tensor_x_test, tensor_y_test)  # create your datset
        test_dataloader = DataLoader(test_dataset, batch_size=100)
        with torch.no_grad():
            recon_loss_x = 0
            recon_loss_y = 0
            for batch_idx, (x, y) in enumerate(test_dataloader):
                x, y = x.to(self.device), y.to(self.device)
                if self.method == 'DCCAE':
                    z_x, z_y, recon_x, recon_y = self.model(x, y)
                elif self.method == 'DVCCA':
                    if self.both_encoders:
                        recon_x, recon_y, mu_x, logvar_x, mu_y, logvar_y = self.model(x, y)
                    else:
                        recon_x, recon_y, mu_x, logvar_x = self.model(x, y)

            recon_loss_x += F.mse_loss(recon_x, x, reduction='sum').detach().cpu().numpy() / \
                            tensor_x_test.size()[0]
            recon_loss_y += F.mse_loss(recon_y, y, reduction='sum').detach().cpu().numpy() / \
                            tensor_y_test.size()[0]
        return recon_loss_x, recon_loss_y

    def transform_view(self, X_new=None, Y_new=None):
        if X_new is not None:
            X_new -= self.X_mean
        if Y_new is not None:
            Y_new -= self.Y_mean

        if self.method == 'DCCAE':
            if X_new is not None:
                U_new = self.model.encode_1(X_new)
            if Y_new is not None:
                V_new = self.model.encode_2(Y_new)
        elif self.method == 'DVCCA':
            if X_new is not None:
                U_new = self.model.encode_1(X_new)[0]
            if Y_new is not None:
                V_new = self.model.encode_2(Y_new)[0]
        if X_new is not None and Y_new is not None:
            return U_new / np.linalg.norm(U_new, axis=0, keepdims=True), V_new / np.linalg.norm(V_new, axis=0,
                                                                                                keepdims=True)
        if X_new is not None and Y_new is None:
            return U_new / np.linalg.norm(U_new, axis=0, keepdims=True), None
        if X_new is None and Y_new is not None:
            return None, V_new / np.linalg.norm(V_new, axis=0, keepdims=True)

    # def predict_view(self, X_new=None, Y_new=None):
    #    U_new, V_new = self.transform_view(X_new=X_new, Y_new=Y_new)
    #    if U_new is None and V_new is not None:
    #        self.score_regression = LinearRegression().fit(self.cca.V.T, self.U.T)
    #        U_pred = self.score_regression.predict(V_new)
    #        return U_pred @ pinv2(self.W.T)
    #    elif V_new is None and U_new is not None:
    #        self.score_regression = LinearRegression().fit(self.V.T, self.U.T)
    #        V_pred = self.score_regression.predict(U_new)
    #        return V_pred @ pinv2(self.C.T)
