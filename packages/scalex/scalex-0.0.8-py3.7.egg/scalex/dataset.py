#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Wed 26 Dec 2018 03:46:19 PM CST
# File Name: batch.py
# Description:
"""

import os
import numpy as np
import pandas as pd
import scipy
from tqdm import tqdm

import torch
from torch.utils.data import Dataset
from torch.utils.data.sampler import Sampler
from torch.utils.data import DataLoader

from anndata import AnnData
import scanpy as sc
from sklearn.utils.sparsefuncs import inplace_row_scale, inplace_column_scale
from multiprocessing import Pool, cpu_count

from glob import glob
import psutil # TEST

np.warnings.filterwarnings('ignore')
DATA_PATH = os.path.expanduser("~")+'/.scalex/'
CHUNK_SIZE = 100000


def read_mtx(path):
    """
    Read mtx format data folder
    """
    for filename in glob(path+'/*'):
        if ('count' in filename or 'matrix' in filename or 'data' in filename) and ('mtx' in filename):
            adata = sc.read_mtx(filename).T
    for filename in glob(path+'/*'):
        if 'barcode' in filename:
            barcode = pd.read_csv(filename, sep='\t', header=None).iloc[:, -1].values
            adata.obs = pd.DataFrame(index=barcode)
        if 'gene' in filename or 'peaks' in filename:
            gene = pd.read_csv(filename, sep='\t', header=None).iloc[:, -1].values
            adata.var = pd.DataFrame(index=gene)
        elif 'feature' in filename:
            gene = pd.read_csv(filename, sep='\t', header=None).iloc[:, 1].values
            adata.var = pd.DataFrame(index=gene)
    return adata


def load_file(path):  
    if os.path.exists(DATA_PATH+path+'.h5ad'):
        adata = sc.read_h5ad(DATA_PATH+path+'.h5ad')
    elif os.path.isdir(path): # mtx format
        adata = read_mtx(path)
    elif os.path.isfile(path):
        if path.endswith(('.csv', '.csv.gz')):
            adata = sc.read_csv(path).T
        elif path.endswith(('.txt', '.txt.gz', '.tsv', '.tsv.gz')):
            df = pd.read_csv(path, sep='\t', index_col=0).T
            adata = AnnData(df.values, dict(obs_names=df.index.values), dict(var_names=df.columns.values))
        elif path.endswith('.h5ad'):
            adata = sc.read_h5ad(path)
    else:
        raise ValueError("File {} not exists".format(path))
        
    if type(adata.X) == np.ndarray:
        adata.X = scipy.sparse.csr_matrix(adata.X)
    adata.var_names_make_unique()
    return adata


def load_files(root):
    """
    Load single cell dataset based-on the path
    """
    if root.split('/')[-1] == '*':
        adata = []
        for root in sorted(glob(root)):
            adata.append(load_file(root))
        return AnnData.concatenate(*adata, batch_key='sub_batch', index_unique=None)
    else:
        return load_file(root)
    
    
def concat_data(
        data_list, 
        batch_categories=None, 
        join='inner',             
        batch_key='batch', 
        index_unique=None, 
        save=None
    ):
    """
    Concat multiple datasets
    """
    if len(data_list) == 1:
        return load_files(data_list[0])
    elif isinstance(data_list, str):
        return load_files(data_list)
    adata_list = []
    for root in data_list:
        adata = load_files(root)
        adata_list.append(adata)
        
    if batch_categories is None:
        batch_categories = list(map(str, range(len(adata_list))))
    else:
        assert len(adata_list) == len(batch_categories)
    [print(b, adata.shape) for adata,b in zip(adata_list, batch_categories)]
    concat = AnnData.concatenate(*adata_list, join=join, batch_key=batch_key,
                                batch_categories=batch_categories, index_unique=index_unique)  
    if save:
        concat.write(save, compression='gzip')
    return concat
        
    
def preprocessing(adata, 
        min_genes=600, 
        min_cells=3, 
        target_sum=1e4, 
        n_top_genes=2000, # or gene list
        chunk_size=CHUNK_SIZE,
    ):
    """
    preprocessing
    """
    print('Preprocessing')
    if type(adata.X) == np.ndarray:
        adata.X = scipy.sparse.csr_matrix(adata.X)
    
    adata = adata[:, [gene for gene in adata.var_names 
                  if not str(gene).startswith(tuple(['ERCC', 'MT-', 'mt-']))]]
    
    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    for chunk, start, end in adata.chunked_X(chunk_size):
        adata.X[start:end] = sc.pp.normalize_total(adata[start:end], target_sum=target_sum, exclude_highly_expressed=True, inplace=False)['X']
#     sc.pp.normalize_total(adata, target_sum=target_sum, exclude_highly_expressed=True)
    sc.pp.log1p(adata, chunked=True, chunk_size=chunk_size)
    if type(n_top_genes) == int and n_top_genes>0:
        sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, batch_key='batch', inplace=False, subset=True)
    else:
        adata = reindex(adata, n_top_genes)
    return batch_scale(adata, chunk_size=chunk_size)
    

def batch_scale(adata, chunk_size=CHUNK_SIZE):
    """
    Batch-specific scale data
    """
    for b in adata.obs['batch'].unique():
        idx = np.where(adata.obs['batch']==b)[0]
        scale_ = adata.X[idx].toarray().max(0)
        adata.var['max_'+str(b)] = scale_
        scale_ += (scale_ == 0)
        for chunk, start, end in adata[idx].chunked_X(chunk_size):
            adata.X[idx][start:end] = inplace_column_scale(chunk, scale_)
    return adata
        

def reindex(adata, genes):
    """
    Reindex AnnData with gene list
    """
    idx = [i for i, g in enumerate(genes) if g in adata.var_names]
    print('There are {} gene in selected genes'.format(len(idx)))
    new_X = scipy.sparse.csr_matrix((adata.shape[0], len(genes)))
    new_X[:, idx] = adata[:, genes[idx]].X
    adata = AnnData(new_X, obs=adata.obs, var={'var_names':genes}) 
    return adata


class BatchSampler(Sampler):
    """
    Batch-specific Sampler
    sampled data of each batch is from the same dataset.
    """
    def __init__(self, batch_size, batch_id, drop_last=False):
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.batch_id = batch_id

    def __iter__(self):
        batch = {}
        sampler = np.random.permutation(len(self.batch_id))
        for idx in sampler:
            c = self.batch_id[idx]
            if c not in batch:
                batch[c] = []
            batch[c].append(idx)

            if len(batch[c]) == self.batch_size:
                yield batch[c]
                batch[c] = []

        for c in batch.keys():
            if len(batch[c]) > 0 and not self.drop_last:
                yield batch[c]
            
    def __len__(self):
        if self.drop_last:
            return len(self.batch_id) // self.batch_size
        else:
            return (len(self.batch_id)+self.batch_size-1) // self.batch_size
        
    
class SingleCellDataset(Dataset):
    """
    Dataset for dataloader
    """
    def __init__(self, adata):
        self.adata = adata
        self.shape = adata.shape
        
    def __len__(self):
        return self.adata.X.shape[0]
    
    def __getitem__(self, idx):
        x = self.adata.X[idx].toarray().squeeze()
        domain_id = self.adata.obs['batch'].cat.codes[idx]
        return x, domain_id, idx


def load_dataset(
        data_list, 
        batch_categories=None, 
        join='inner', 
        batch_key='batch', 
        batch_name='batch',
         min_genes=600, 
        min_cells=3, 
        n_top_genes=2000, 
        batch_size=64, 
        chunk_size=CHUNK_SIZE
    ):
    """
    Load dataset with preprocessing
    """
    adata = concat_data(data_list, batch_categories, join=join, batch_key=batch_key)
    print('Raw dataset shape: {}'.format(adata.shape))
    if batch_name!='batch':
        adata.obs['batch'] = adata.obs[batch_name]
    if 'batch' not in adata.obs:
        adata.obs['batch'] = 'batch'
    adata.obs['batch'] = adata.obs['batch'].astype('category')
    
    adata = preprocessing(
        adata, 
        min_genes=min_genes, 
        min_cells=min_cells, 
        n_top_genes=n_top_genes,
        chunk_size=chunk_size,
    )
    scdata = SingleCellDataset(adata)
    trainloader = DataLoader(
        scdata, 
        batch_size=batch_size, 
        drop_last=True, 
        shuffle=True, 
        num_workers=4
    )
    batch_sampler = BatchSampler(batch_size, adata.obs['batch'], drop_last=False)
    testloader = DataLoader(scdata, batch_sampler=batch_sampler)
    
    return adata, trainloader, testloader 