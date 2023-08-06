#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import random
import os
from os.path import isfile
import numpy as np
import tensorflow as tf
import json as js
import matplotlib.pyplot as plt
import argh
import argparse


def extrctDt_excel(excelNm, skpRws):
    IO = os.getcwd() + '/{}'.format(excelNm)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    data = pd.read_excel(io=IO, skiprows=skpRws, index_col=0)
    return data


def Merge2number(dtClmns):
    # 几列对勾形式整合成一列序号形式
    # print(dtClmns.iloc[0, 0])
    indx = dtClmns.shape[0]
    clmn = dtClmns.shape[1]
    # ndarray 装数字
    mrgdata = np.zeros(indx)
   # 取得数字
    for i in range(indx):  # index 循环
        for c in range(clmn):  # column 循环
            if dtClmns.iloc[i, c] == '√': mrgdata[i] = c+1
    # 插入dtClmns
    dtClmns.insert(0, 'mrg', mrgdata)
    # print(dtClmns)
    return dtClmns


def getData(excelNm='Characteristics531.xls',
            inData=[['Unnamed: 5'],
                    ['Unnamed: 6'],
                    ['Unnamed: 7'],
                    ['Unnamed: 8']],
            outData=['Unnamed: 44']):
    skpRws = 22
    data = extrctDt_excel(excelNm, skpRws)
    #    print(data)
    # for key in data:
    #    print(key)
    # print(data[['Planar-layered ', 'Wavelike layered','Cross stacking', 'Mixed stacking']])
    # 合并 Packing types
    PckTyp = Merge2number(data[['Planar-layered ', 'Wavelike layered','Cross stacking', 'Mixed stacking']])['mrg']
    data['Packing types'] = PckTyp  # 末尾新增列
    # 合并 Molecular backbones
    # MolBkbn = Merge2number(data[['Homocyclic ', 'Heterocyclic', 'Heterocyclic.1', 'Cage-like', 'Unnamed: 24', 'Unnamed: 25']])['mrg']
    # data['Molecular backbones'] = MolBkbn  # 末尾新增列
    # print('\n * data \n',data.columns)   # show all columns in DataFrame

    dfx = []
    for col in inData:
        dfx.append(data[col])

    dfy    = data[outData]
    dfName = list(dfy.index)

    v = []
    for d in dfx:
        v.append(np.squeeze(d.values))
    y = np.squeeze(dfy.values)

    values   = []
    rowName  = []
    y_       = []

    for i,dn in enumerate(dfName):
        nanVaule = False
        for v_ in v:
            if np.isnan(v_[i]):
               nanVaule = True 

        if nanVaule: 
           continue
        else:
           rowName.append(dn)
           values.append([v_[i] for v_ in v])
           y_.append(y[i])
    return rowName,np.array(values),np.array(y_)


class Linear(tf.keras.Model):
    def __init__(self,J='WeightAndBias.json',HLayer=1,inLayer=None,outLayer=None):
        super().__init__()
        self.inLayer  = inLayer
        self.outLayer = outLayer
        self.hl       = HLayer # hidden layer
        self.wh       = []
        self.bh       = []
        self.wbf      = 'WeightAndBias.json' if J is None else J
        # print('inLayer:',self.inLayer)
        if not isfile(J):
           self.wi  = tf.Variable(tf.random.normal(self.inLayer,stddev=0.2),name='wi')
           self.bi  = tf.Variable(tf.random.normal([self.inLayer[1]],stddev=0.2),name='bi')
           
           for i in range(self.hl):
               self.wh.append(tf.Variable(tf.random.normal([self.inLayer[1],self.inLayer[1]],
                                stddev=0.2),name='wh_%d' %i))
               self.bh.append(tf.Variable(tf.random.normal([self.inLayer[1]],
                                stddev=0.2),name='bh_%d' %i))

           self.wo  = tf.Variable(tf.random.normal(self.outLayer,stddev=0.2),name='wo')
           self.bo  = tf.Variable(tf.random.normal([self.outLayer[1]],stddev=0.2),name='bo')
        else:
           with open(J,'r') as lf:
                j = js.load(lf)
           hl_ = len(j['wh'])

           self.wi  = tf.Variable(j['wi'],name='wi')
           self.bi  = tf.Variable(j['bi'],name='bi')

           for i in range(self.hl):
               if i <=hl_-1:
                  self.wh.append(tf.Variable(j['wh'][i],name='wh_%d' %i))
                  self.bh.append(tf.Variable(j['bh'][i],name='bh_%d' %i))
               else:
                  self.wh.append(tf.Variable(tf.random.normal([self.inLayer[1],self.inLayer[1]],
                                 stddev=0.2),name='wh_%d' %i))
                  self.bh.append(tf.Variable(tf.random.normal([self.inLayer[1]],
                                 stddev=0.2),name='bh_%d' %i))

           self.wo  = tf.Variable(j['wo'],name='wo')
           self.bo  = tf.Variable(j['bo'],name='bo')


    def call(self, x):
        o  = []
        o.append(tf.sigmoid(tf.matmul(x,self.wi)+self.bi))
        # print('output 1 shape: ',o[-1].shape)
        for i in range(self.hl):
            o.append(tf.sigmoid(tf.matmul(o[-1],self.wh[i])+self.bh[i]))
            # print('output %d shape: ' %(i+1),o[-1].shape)
        output   = tf.sigmoid(tf.matmul(o[-1],self.wo)+self.bo)
        return tf.squeeze(output)


    def save(self):
        with open(self.wbf,'w') as fj:
             j = {}
             wh = []
             bh = []
             for i in range(self.hl):
                 wh.append(self.wh[i].numpy().tolist())
                 bh.append(self.bh[i].numpy().tolist())

             j['wi'] = self.wi.numpy().tolist()
             j['bi'] = self.bi.numpy().tolist()
             j['wh'] = wh
             j['bh'] = bh
             j['wo'] = self.wo.numpy().tolist()
             j['bo'] = self.bo.numpy().tolist()
             js.dump(j,fj,sort_keys=True,indent=2)


def learn(dN,x,y,interactive=True,total_step=50000,
          normalizeFactor_x = [3.0,100.0,1.0,100.0],
          normalizeFactor_y = 10.0,
          training=True,
          learning_rate=0.001,
          criteria=0.001,
          test=0.2,
          wbf='WeightAndBias.json',
          label='Detonation velocity',
          m=10,n=8):
    ''' neural network size 8*10 '''

    nSet = len(y)
    pool = [i for i in range(nSet)]
    nTest = int(nSet*test)
    if nTest==0: nTest = 1
    testIndex  = random.sample(pool,nTest) 
    trainIndex = list(set(pool).difference(set(testIndex)))

    xTest = x[testIndex]
    yTest = y[testIndex]
    x     = x[trainIndex]
    y     = y[trainIndex]  

    x = np.expand_dims(x,axis=1)
    ni= x.shape[-1]

    x_ = np.divide(x,normalizeFactor_x)
    xTest_ = np.divide(xTest,normalizeFactor_x)

    # neural network layers
    model = Linear(J=wbf,HLayer=m,inLayer=[ni,n],outLayer=[n,1])

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    if interactive: plt.ion()
    X = list(range(len(y)))
    XTest = list(range(len(yTest)))
    y_pred = model(x_)
    yTest_ = model(xTest_)
    Loss,Loss_ = [],[]

    if training:
       step = 0
       # for step in range(total_step):
       while True:        
           # train and net output
           with tf.GradientTape() as tape:
               y_pred = model(x_)
               # loss = tf.reduce_mean(tf.square(y_pred*normalizeFactor_y - y))
               loss = tf.losses.mean_squared_error(y,y_pred*normalizeFactor_y )
               # loss = tf.nn.l2_loss(y_pred*normalizeFactor_y - y,name='loss')
               # loss = tf.nn.l2_loss(tf.exp(y_pred*3.0+5.0) - y,name='loss') 
               # loss = tf.nn.l2_loss(tf.exp((y_pred+2.0)*2.5) - y,name='loss') 
               # loss = tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y_pred,name='loss'))

           grads = tape.gradient(loss, model.variables)   
           optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))
           
           if step % 10 == 0:
              yTest_ = model(xTest_)
              loss_ = tf.losses.mean_squared_error(yTest,yTest_*normalizeFactor_y)
              Loss.append(loss)
              Loss_.append(loss_)

              if interactive:
                 plt.cla()
                 plt.plot(Loss,label=r'$Training set}$', color='blue', linewidth=1)
                 plt.plot(Loss_,label=r'$Testing set}$', color='red', linewidth=1)
                 # plt.text(0.0, min(y), 'Step: %d Loss=%.4f' %(step,loss), fontdict={'size': 20, 'color': 'red'})
                 plt.legend(loc='best',edgecolor='yellowgreen')
                 plt.pause(0.1)
              else:
                 print('Step: %d Loss=%.4f Loss_=%.4f' %(step,loss,loss_))

              if (loss_-loss)>0.0001 and step>2000 :
                 print(' * Over fitting points reached!')
                 break

           if step %1000==0:
              model.save()

           if loss<criteria:
              print(' * Convergence Occurred.')
              break
           step += 1
    model.save()

    if interactive: plt.ioff()

    ##            performence on Training DataSet
    plt.figure()
    plt.scatter(X,y,c='none',edgecolors='blue',linewidths=1,
                marker='o',s=32,label=label,
                alpha=1.0)
    yp = y_pred*normalizeFactor_y
    err= y - yp
    # for i,e in enumerate(err):
    #     e_ = e.numpy()
    # if abs(e_)>0.3:
    #    print(dN[i],e_)
    plt.errorbar(X,yp,yerr=err,
                 fmt='s',ecolor='r',color='r',ms=6,markerfacecolor='none',mec='r',
                 elinewidth=2,capsize=2,label='Prediction')
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('LearningResults.pdf')
    plt.close()

    ##            performence of Test DataSet
    plt.figure()   
    plt.scatter(XTest,yTest,c='none',edgecolors='blue',linewidths=1,
                marker='o',s=32,label=label,
                alpha=1.0)

    yp = yTest_*normalizeFactor_y
    err= yTest - yp

    # for i,e in enumerate(err):
    #     e_ = e.numpy()
    #  if abs(e_)>0.3:
    #     print(dN[i],e_)
    plt.errorbar(XTest,yp,yerr=err,
                 fmt='s',ecolor='r',color='r',ms=6,markerfacecolor='none',mec='r',
                 elinewidth=2,capsize=2,label='Prediction')
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('LearningResultsTestSet.pdf')


def he(step=5000):
    rowName,x,y = getData(excelNm='Characteristics.xlsx',
                      inData=[['Unnamed: 5'],
                              ['Unnamed: 6'],
                              ['Unnamed: 7'],
                              ['Unnamed: 8']],
                      outData=['Unnamed: 48'])
    # 44 detonation velocity
    # 48 Heat of explosion
    print(y)
    y_ = np.log(y)/2.5 -2.0
    # print(y_)
    # print(np.min(y_),np.max(y_))
    yp = np.exp((y_+2.0)*2.5) 
    print(yp)

    learn(rowName,x,y_,interactive=False,
          total_step=1000,
          normalizeFactor_x = [2.5,100.0,1.0,100.0],
          normalizeFactor_y = 1.0,
          training=False,
          learning_rate=0.0001,
          criteria=0.003,
          wbf='Heat.json',
          label='Heat of explosion',
          m=3,n=32)


def dv(step=5000):
    rowName,x,y = getData(excelNm='Characteristics.xlsx',
                          inData=[['Unnamed: 5'],
                                 ['Unnamed: 6'],
                                 ['Unnamed: 7'],
                                 ['Unnamed: 8']],
                          outData=['Unnamed: 44'])
    learn(rowName,x,y,interactive=False,
          total_step=step,
          normalizeFactor_x = [2.5,100.0,1.0,100.0],
          normalizeFactor_y = 10.0,
          training=False,
          learning_rate=0.0001,
          criteria=0.003,
          wbf='Velocity.json',
          label='Detonation Velecity',
          test=0.2,
          m=3,n=32)


def le(step=5000):
    rowName,x,y = getData(excelNm='Characteristics.xlsx',
                          inData=[['HB amount']],
                          outData=['LE'])

    # print(x)
    # print(y)
    # print(np.max(y))
    learn(rowName,x,y,interactive=False,
          total_step=step,
          normalizeFactor_x = [100.0],
          normalizeFactor_y = 150.0,
          training=True,
          learning_rate=0.0001,
          criteria=0.003,
          wbf='LatticeEnergy.json',
          label='Detonation Velecity',
          test=0.2,
          m=3,n=32)


if __name__ == '__main__':
   ''' use commond like ./emnn.py dv --step=5000 to run it'''
   parser = argparse.ArgumentParser()
   argh.add_commands(parser, [le,dv,he])
   argh.dispatch(parser)

