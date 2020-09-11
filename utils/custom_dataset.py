import numpy as np
import os
import torch
import torchvision
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset
from torchvision import transforms


## Custom PyTorch Dataset Class wrapper
class CustomDataset(Dataset):
    def __init__(self, data, target, device=None, transform=None):       
        self.transform = transform
        if device is not None:
            # Push the entire data to given device, eg: cuda:0
            self.data = torch.from_numpy(data.astype('float32'))#.to(device)
            self.targets = torch.from_numpy(target)#.to(device)
        else:
            self.data = data.astype('float32')
            self.targets = target

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()        
        sample_data = self.data[idx]
        label = self.targets[idx]
        if self.transform is not None:
            sample_data = self.transform(sample_data)
        return (sample_data, label) #.astype('float32')

class CustomDataset_act(Dataset):
    def __init__(self, data, target, transform=None):       
        self.transform = transform
        self.data = data #.astype('float32')
        self.targets = target
        self.X = self.data
        self.Y = self.targets

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()        
        sample_data = self.data[idx]
        label = self.targets[idx]
        if self.transform is not None:
            sample_data = self.transform(sample_data)
        return sample_data, label,idx #.astype('float32')


## Utility function to load datasets from libsvm datasets
def libsvm_file_load(path,dim, save_data=False):
    data = []
    target = []
    with open(path) as fp:
       line = fp.readline()
       while line:
        temp = [i for i in line.strip().split(",")]
        target.append(int(float(temp[-1]))) # Class Number. # Not assumed to be in (0, K-1)
        temp_data = [0]*dim
        count = 0
        for i in temp[:-1]:
            #ind, val = i.split(':')
            temp_data[count] = float(i)
            count += 1
        data.append(temp_data)
        line = fp.readline()
    X_data = np.array(data, dtype=np.float32)
    Y_label = np.array(target)
    if save_data:
        # Save the numpy files to the folder where they come from
        data_np_path = path + '.data.npy'
        target_np_path = path + '.label.npy'
        np.save(data_np_path, X_data)
        np.save(target_np_path, Y_label)
    return (X_data, Y_label)

def census_load(path,dim, save_data=False):
    
    enum=enumerate(['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 
        'Never-worked'])
    workclass = dict((j,i) for i,j in enum)

    enum=enumerate(['Bachelors', 'Some-college', '11th, HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', 
        '12th, Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'])
    education = dict((j,i) for i,j in enum)

    enum=enumerate(['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'])
    marital_status = dict((j,i) for i,j in enum)

    enum=enumerate(['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners',
        'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'])
    occupation = dict((j,i) for i,j in enum)

    enum=enumerate(['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'])
    relationship = dict((j,i) for i,j in enum)

    enum=enumerate(['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'])
    race = dict((j,i) for i,j in enum)

    sex ={0:'Female',1:'Male'}

    enum=enumerate(['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)',
     'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 
     'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 
     'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 
     'Holand-Netherlands'])
    native_country = dict((j,i) for i,j in enum)

    data = []
    target = []
    with open(path) as fp:
       line = fp.readline()
       while line:
        temp = [i for i in line.strip().split(",")]

        if temp[-1].strip() == "<=50K":
            target.append(0) # Class Number. # Not assumed to be in (0, K-1)
        else:
            target.append(1)
        
        temp_data = [0]*dim
        count = 1
        for i in temp[:-1]:

            if count == 2:
                temp_data[count] =  workclass[i.strip()]
            elif count == 4:
                temp_data[count] =  education[i.strip()]
            elif count == 6:
                temp_data[count] =  marital_status[i.strip()]
            elif count == 7:
                temp_data[count] =  occupation[i.strip()]
            elif count == 8:
                temp_data[count] =  relationship[i.strip()]
            elif count == 9:
                temp_data[count] =  race[i.strip()]
            elif count == 10:
                temp_data[count] =  sex[i.strip()]
            elif count == 14:
                temp_data[count] =  native_country[i.strip()]
            else:
                temp_data[count] = float(i)
            count += 1
        
        data.append(temp_data)
        line = fp.readline()
    X_data = np.array(data, dtype=np.float32)
    Y_label = np.array(target)
    if save_data:
        # Save the numpy files to the folder where they come from
        data_np_path = path + '.data.npy'
        target_np_path = path + '.label.npy'
        np.save(data_np_path, X_data)
        np.save(target_np_path, Y_label)
    return (X_data, Y_label)


## Utility function to load datasets from libsvm datasets
## path = input file path
def libsvm_to_standard(path, dim):
    data = []
    target = []
    with open(path) as fp:
       line = fp.readline()
       while line:
        temp = [i for i in line.strip().split(" ")]
        row_vector = [0] * (dim+1) # +1 for the y label
        row_label = int(temp[0])
        target.append(row_label) # Class Number. # Not assumed to be in (0, K-1)
        # row_vector[0] = row_label
        temp_data = [0] * dim        
        for i in temp[1:]:
            ind,val = i.split(':')
            temp_data[int(ind)-1] = float(val)
        # insert class label as the 1st column
        temp_data.insert(0, row_label)
        data.append(temp_data)
        line = fp.readline()
    
    all_data = np.array(data,dtype=np.float32)
    np.savetxt(path + ".trf", all_data, fmt='%.3f')   # entire data
    # return all_data




## Function to load a discrete UCI dataset and make it ordinal.
def clean_uci_ordinal_data(inp_fname, out_fname):
    # trn, val, tst split: 0.8, 0.1, 0.1
    data = np.genfromtxt(inp_fname, delimiter=',', dtype='str')
    enc = OrdinalEncoder(dtype=int)
    enc.fit(data)
    transformed_data = enc.transform(data)
    np.random.shuffle(transformed_data)     # randomly shuffle the data points
    
    N = transformed_data.shape[0]
    N_trn = int(N * 0.8)
    N_val = int(N * 0.1)
    N_tst = int(N * 0.1)
    data_trn = transformed_data[: N_trn]
    data_val = transformed_data[N_trn : N_trn + N_val]
    data_tst = transformed_data[N_trn + N_val :]

    np.savetxt(out_fname + ".full", transformed_data, fmt='%.0f')   # entire data
    np.savetxt(out_fname + ".trn", data_trn, fmt='%.0f')
    np.savetxt(out_fname + ".val", data_val, fmt='%.0f')
    np.savetxt(out_fname + ".tst", data_tst, fmt='%.0f')



## Utility function to save numpy array for knnSB
## Used in: KnnSubmod Selection
def write_knndata(datadir, dset_name):
    fullset, valset, testset, num_cls  = load_dataset_numpy(datadir, dset_name)
    
    x_trn, y_trn = fullset
    x_val , y_val = valset
    x_tst, y_tst = testset
    ## Create VAL data
    #x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
    trndata = np.c_[x_trn, y_trn]
    valdata = np.c_[x_val, y_val]
    tstdata = np.c_[x_tst, y_tst]
    # Write out the trndata
    trn_filepath = os.path.join(datadir, 'knn_' + dset_name + '.trn')
    val_filepath = os.path.join(datadir, 'knn_' + dset_name + '.val')
    tst_filepath = os.path.join(datadir, 'knn_' + dset_name + '.tst')
    np.savetxt(trn_filepath, trndata, fmt='%.6f')
    np.savetxt(val_filepath, valdata, fmt='%.6f')
    np.savetxt(tst_filepath, tstdata, fmt='%.6f')
    return

## Takes in a dataset name and returns a PyTorch Dataset Object
def load_dataset_pytorch_sep_val(datadir, dset_name,device):
    if dset_name == "dna":
        trn_file = os.path.join(datadir, 'dna.scale.trn')
        val_file = os.path.join(datadir, 'dna.scale.val')
        tst_file = os.path.join(datadir, 'dna.scale.tst')
        data_dims = 180
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        y_trn -= 1  # First Class should be zero
        y_val -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        return fullset, valset, testset, data_dims,num_cls 

    elif dset_name == "sensit_seismic":
        trn_file = os.path.join(datadir, 'sensit_seismic.trn')
        tst_file = os.path.join(datadir, 'sensit_seismic.tst')
        data_dims = 50
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        return fullset, valset, testset, data_dims,num_cls 

    elif dset_name == "protein":
        trn_file = os.path.join(datadir, 'protein.trn')
        val_file = os.path.join(datadir, 'protein.val')
        tst_file = os.path.join(datadir, 'protein.tst')
        data_dims = 357
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        return fullset, valset, testset, data_dims,num_cls

    elif dset_name == "shuttle":
        trn_file = os.path.join(datadir, 'shuttle.trn')
        val_file = os.path.join(datadir, 'shuttle.val')
        tst_file = os.path.join(datadir, 'shuttle.tst')
        data_dims = 9
        num_cls = 7
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero

        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)

        return fullset, valset, testset, data_dims,num_cls

    elif dset_name == "sensorless":
        trn_file = os.path.join(datadir, 'sensorless.scale.trn')
        tst_file = os.path.join(datadir, 'sensorless.scale.val')
        data_dims = 48
        num_cls = 11
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)

        return fullset, valset, testset, data_dims, num_cls

    elif dset_name == "connect_4":
        trn_file = os.path.join(datadir, 'connect_4.trn')

        data_dims = 126
        num_cls = 3

        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        # The class labels are (-1,0,1). Make them to (0,1,2)
        y_trn[y_trn < 0] = 2

        x_trn, x_tst, y_trn, y_tst = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)

        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)

        return fullset, valset, testset, data_dims,num_cls


    elif dset_name == "letter":
        trn_file = os.path.join(datadir, 'letter.scale.trn')
        val_file = os.path.join(datadir, 'letter.scale.val')
        tst_file = os.path.join(datadir, 'letter.scale.tst')
        data_dims = 16
        num_cls = 26 
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))

        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        
        return fullset, valset, testset, data_dims,num_cls
   
    elif dset_name == "pendigits":
        trn_file = os.path.join(datadir, 'pendigits.trn_full')
        tst_file = os.path.join(datadir, 'pendigits.tst')
        data_dims = 16
        num_cls = 10
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)

        sc = StandardScaler()
        
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        
        return fullset, valset, testset, data_dims,num_cls
    

    elif dset_name == "satimage":
        trn_file = os.path.join(datadir, 'satimage.scale.trn')
        val_file = os.path.join(datadir, 'satimage.scale.val')
        tst_file = os.path.join(datadir, 'satimage.scale.tst')
        data_dims = 36
        num_cls = 6
        
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        
        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        
        return fullset, valset, testset, data_dims,num_cls

    elif dset_name == "svmguide1":
        trn_file = os.path.join(datadir, 'svmguide1.trn_full')
        tst_file = os.path.join(datadir, 'svmguide1.tst')
        data_dims = 4
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst, device)
        return fullset, valset, testset, data_dims,num_cls
    
    elif dset_name == "usps":
        trn_file = os.path.join(datadir, 'usps.trn_full')
        tst_file = os.path.join(datadir, 'usps.tst')
        data_dims = 256
        num_cls = 10
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst, device)
        return fullset, valset, testset, data_dims,num_cls
    
    elif dset_name == "ijcnn1":
        trn_file = os.path.join(datadir, 'ijcnn1.trn')
        val_file = os.path.join(datadir, 'ijcnn1.val')
        tst_file = os.path.join(datadir, 'ijcnn1.tst')
        data_dims = 22
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        
        # The class labels are (-1,1). Make them to (0,1)
        y_trn[y_trn < 0] = 0
        y_val[y_val < 0] = 0
        y_tst[y_tst < 0] = 0
       
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        
        fullset = CustomDataset(x_trn, y_trn,device)
        valset = CustomDataset(x_val, y_val,device)
        testset = CustomDataset(x_tst, y_tst,device)
        
        return fullset, valset, testset, data_dims,num_cls
    elif dset_name == "mnist":
        mnist_transform = transforms.Compose([
            transforms.Grayscale(3),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
            (0.1307,), (0.3081,))
        ])
        num_cls = 10
        fullset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=mnist_transform)
        testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=mnist_transform)
        return fullset, testset, num_cls
    elif dset_name == "sklearn-digits":
        data, target = datasets.load_digits(return_X_y=True)
        # Test data is 10%
        x_trn, x_tst, y_trn, y_tst = train_test_split(data, target, test_size=0.1, random_state=42)

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        num_cls = 10
        fullset = CustomDataset(x_trn, y_trn, device)
        valset = CustomDataset(x_val, y_val, device)
        testset = CustomDataset(x_tst, y_tst, device)
        return fullset, valset, testset, x_trn.shape[1], num_cls
    elif dset_name == "bc":
        data, target = datasets.load_breast_cancer(return_X_y=True)
        
        x_trn, x_tst, y_trn, y_tst = train_test_split(data, target, test_size=0.1, random_state=42)
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        num_cls = 2
        
        fullset = CustomDataset(x_trn, y_trn, device)
        valset = CustomDataset(x_val, y_val, device)
        testset = CustomDataset(x_tst, y_tst, device)
        return fullset, valset, testset, x_trn.shape[1], num_cls


## Takes in a dataset name and returns a Tuple of ((x_trn, y_trn), (x_tst, y_tst))
def load_dataset_numpy(datadir, dset_name):
    if dset_name == "dna":
        trn_file = os.path.join(datadir, 'dna.scale.trn')
        val_file = os.path.join(datadir, 'dna.scale.val')
        tst_file = os.path.join(datadir, 'dna.scale.tst')
        data_dims = 180
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        y_trn -= 1  # First Class should be zero
        y_val -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "linsep":
        trn_file = os.path.join(datadir, 'linsep.trn')
        val_file = os.path.join(datadir, 'linsep.val')
        tst_file = os.path.join(datadir, 'linsep.tst')
        data_dims = 2
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "class_imb_linsep_2":
        trn_file = os.path.join(datadir, 'class_imb_linsep_2.trn')
        val_file = os.path.join(datadir, 'class_imb_linsep_2.val')
        tst_file = os.path.join(datadir, 'class_imb_linsep_2.tst')
        data_dims = 2
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "class_imb_linsep_4":
        trn_file = os.path.join(datadir, 'class_imb_linsep_4.trn')
        val_file = os.path.join(datadir, 'class_imb_linsep_4.val')
        tst_file = os.path.join(datadir, 'class_imb_linsep_4.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "linsep_4":
        trn_file = os.path.join(datadir, 'linsep_4.trn')
        val_file = os.path.join(datadir, 'linsep_4.val')
        tst_file = os.path.join(datadir, 'linsep_4.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "large_linsep_4":
        trn_file = os.path.join(datadir, 'large_linsep_4.trn')
        val_file = os.path.join(datadir, 'large_linsep_4.val')
        tst_file = os.path.join(datadir, 'large_linsep_4.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "noise_large_linsep_2":
        trn_file = os.path.join(datadir, 'noise_large_linsep_2.trn')
        val_file = os.path.join(datadir, 'noise_large_linsep_2.val')
        tst_file = os.path.join(datadir, 'noise_large_linsep_2.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "noise_large_linsep_4":
        trn_file = os.path.join(datadir, 'noise_large_linsep_4.trn')
        val_file = os.path.join(datadir, 'noise_large_linsep_4.val')
        tst_file = os.path.join(datadir, 'noise_large_linsep_4.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "gauss_2":
        trn_file = os.path.join(datadir, 'gauss_2.trn')
        val_file = os.path.join(datadir, 'gauss_2.val')
        tst_file = os.path.join(datadir, 'gauss_2.tst')
        data_dims = 2
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "clf_2":
        trn_file = os.path.join(datadir, 'clf_2.trn')
        val_file = os.path.join(datadir, 'clf_2.val')
        tst_file = os.path.join(datadir, 'clf_2.tst')
        data_dims = 2
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name in ['prior_shift_clf_2', 'prior_shift_gauss_2','conv_shift_clf_2', 'conv_shift_gauss_2']:
        
        trn_file = os.path.join(datadir, dset_name+'.trn')
        val_file = os.path.join(datadir, dset_name+'.val')
        tst_file = os.path.join(datadir, dset_name+'.tst')
        data_dims = 2
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name in ['prior_shift_large_linsep_4','conv_shift_large_linsep_4','red_large_linsep_4','expand_large_linsep_4',
    'shrink_large_linsep_4','red_conv_shift_large_linsep_4']:
        
        trn_file = os.path.join(datadir, dset_name+'.trn')
        val_file = os.path.join(datadir, dset_name+'.val')
        tst_file = os.path.join(datadir, dset_name+'.tst')
        data_dims = 2
        num_cls = 4
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        # x_trn = np.concatenate((x_trn, x_val))
        # y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls
        

    elif dset_name == "sensit_seismic":
        trn_file = os.path.join(datadir, 'sensit_seismic.trn')
        tst_file = os.path.join(datadir, 'sensit_seismic.tst')
        data_dims = 50
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "covertype":
        trn_file = os.path.join(datadir, 'covertype.data')

        data_dims = 54
        num_cls = 7
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
       
        y_trn -= 1  # First Class should be zero
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        x_trn, x_tst, y_trn, y_tst = train_test_split(x_trn, y_trn, test_size=0.2, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "census":
        trn_file = os.path.join(datadir, 'adult.data')
        tst_file = os.path.join(datadir, 'adult.test')

        data_dims = 14
        num_cls = 2

        x_trn, y_trn = census_load(trn_file, dim=data_dims)
        x_tst, y_tst = census_load(tst_file, dim=data_dims)
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "protein":
        trn_file = os.path.join(datadir, 'protein.trn')
        val_file = os.path.join(datadir, 'protein.val')
        tst_file = os.path.join(datadir, 'protein.tst')
        data_dims = 357
        num_cls = 3
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "shuttle":
        trn_file = os.path.join(datadir, 'shuttle.trn')
        val_file = os.path.join(datadir, 'shuttle.val')
        tst_file = os.path.join(datadir, 'shuttle.tst')
        data_dims = 9
        num_cls = 7
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero

        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "sensorless":
        trn_file = os.path.join(datadir, 'sensorless.scale.trn')
        tst_file = os.path.join(datadir, 'sensorless.scale.val')
        data_dims = 48
        num_cls = 11
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "connect_4":
        trn_file = os.path.join(datadir, 'connect_4.trn')

        data_dims = 126
        num_cls = 3

        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        # The class labels are (-1,0,1). Make them to (0,1,2)
        y_trn[y_trn < 0] = 2

        x_trn, x_tst, y_trn, y_tst = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)

        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "letter":
        trn_file = os.path.join(datadir, 'letter.scale.trn')
        val_file = os.path.join(datadir, 'letter.scale.val')
        tst_file = os.path.join(datadir, 'letter.scale.tst')
        data_dims = 16
        num_cls = 26 
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))

        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "pendigits":
        trn_file = os.path.join(datadir, 'pendigits.trn_full')
        tst_file = os.path.join(datadir, 'pendigits.tst')
        data_dims = 16
        num_cls = 10
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)

        sc = StandardScaler()
        
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "satimage":
        trn_file = os.path.join(datadir, 'satimage.scale.trn')
        val_file = os.path.join(datadir, 'satimage.scale.val')
        tst_file = os.path.join(datadir, 'satimage.scale.tst')
        data_dims = 36
        num_cls = 6
        
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        #x_trn = np.concatenate((x_trn, x_val))
        #y_trn = np.concatenate((y_trn, y_val))
        
        y_trn -= 1  # First Class should be zero
        y_val -= 1
        y_tst -= 1  # First Class should be zero
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "svmguide1":
        trn_file = os.path.join(datadir, 'svmguide1.trn_full')
        tst_file = os.path.join(datadir, 'svmguide1.tst')
        data_dims = 4
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "usps":
        trn_file = os.path.join(datadir, 'usps.trn_full')
        tst_file = os.path.join(datadir, 'usps.tst')
        data_dims = 256
        num_cls = 10
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        y_trn -= 1  # First Class should be zero
        y_tst -= 1  # First Class should be zero

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "ijcnn1":
        trn_file = os.path.join(datadir, 'ijcnn1.trn')
        val_file = os.path.join(datadir, 'ijcnn1.val')
        tst_file = os.path.join(datadir, 'ijcnn1.tst')
        data_dims = 22
        num_cls = 2
        x_trn, y_trn = libsvm_file_load(trn_file, dim=data_dims)
        x_val, y_val = libsvm_file_load(val_file, dim=data_dims)
        x_tst, y_tst = libsvm_file_load(tst_file, dim=data_dims)
        
        # The class labels are (-1,1). Make them to (0,1)
        y_trn[y_trn < 0] = 0
        y_val[y_val < 0] = 0
        y_tst[y_tst < 0] = 0    

        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "mnist":
        mnist_transform = transforms.Compose([            
            torchvision.transforms.ToTensor(),
            transforms.Grayscale(3),
            torchvision.transforms.Normalize(
            (0.1307,), (0.3081,))
        ])
        num_cls = 10
        fullset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=mnist_transform)
        testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=mnist_transform)
        return fullset, testset, num_cls        
    elif dset_name == "sklearn-digits":
        data, target = datasets.load_digits(return_X_y=True)
        # Test data is 10%
        x_trn, x_tst, y_trn, y_tst = train_test_split(data, target, test_size=0.1, random_state=42)

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        num_cls = 10

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls

    elif dset_name == "bc":
        data, target = datasets.load_breast_cancer(return_X_y=True)
        # Test data is 10%
        x_trn, x_tst, y_trn, y_tst = train_test_split(data, target, test_size=0.1, random_state=42)

        x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, test_size=0.1, random_state=42)
        sc = StandardScaler()
        x_trn = sc.fit_transform(x_trn)
        x_val = sc.transform(x_val)
        x_tst = sc.transform(x_tst)
        num_cls = 2

        fullset = (x_trn, y_trn)
        valset = (x_val, y_val)
        testset = (x_tst, y_tst)
        return fullset, valset, testset, num_cls



def get_toydata(num_samples, num_features, num_classes, class_separation, plot_savepath):        

    data, target = make_classification(n_samples=num_samples, n_features=num_features, 
        n_informative=num_features, n_redundant=0, n_classes=num_classes, 
        n_clusters_per_class=1, class_sep=class_separation, random_state=42)
    
    x_trn, x_tst, y_trn, y_tst = train_test_split(data, target, 
        test_size=0.1, random_state=42)

    x_trn, x_val, y_trn, y_val = train_test_split(x_trn, y_trn, 
        test_size=0.1, random_state=42)
    
    sc = StandardScaler()
    x_trn = sc.fit_transform(x_trn)
    x_val = sc.transform(x_val)
    x_tst = sc.transform(x_tst)

    trnset = (x_trn, y_trn)
    valset = (x_val, y_val)
    tstset = (x_tst, y_tst)

    # Plot only if the data is 2-D
    if num_features == 2:
        X_0 = x_trn[y_trn == 0]
        X_1 = x_trn[y_trn == 1]

        V_0 = x_val[y_val == 0]
        V_1 = x_val[y_val == 1]

        T_0 = x_tst[y_tst == 0]
        T_1 = x_tst[y_tst == 1]

        plt.figure()
        plt.scatter(X_0[:,0], X_0[:,1], color='blue', label='trn 0')
        plt.scatter(X_1[:,0], X_1[:,1], color='red', label='trn 1')

        plt.scatter(V_0[:,0], V_0[:,1], color='#CEF6F5', label='val 0')
        plt.scatter(V_1[:,0], V_1[:,1], color='#F5A9BC', label='val 1')

        plt.scatter(T_0[:,0], T_0[:,1], color='#8181F7', label='tst 0')
        plt.scatter(T_1[:,0], T_1[:,1], color='#8A0868', label='tst 1')
        
        plt.legend()
        plot_title = '2DtoyData' + '_' + str(num_samples) + '_' + str(num_classes) + '_' + str(class_separation) 
        plt.title(plot_title)
        plt.savefig(plot_savepath)
    
    return trnset, valset, tstset, num_classes