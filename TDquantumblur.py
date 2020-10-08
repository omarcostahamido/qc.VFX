import sys
# replace with your path to QuantumBlur
sys.path.insert(1, 'C:/Users/Chris/Documents/GitHub/QuantumBlur')
import quantumblur as qb
from PIL import Image
import numpy as np
import threading

def partial_x(qc,fraction):
    for j in range(qc.num_qubits):
        qc.rx(np.pi*fraction,j)
        
def array_to_IMG(array):
	return Image.fromarray(np.uint8(array * 255) , 'L')
	
def array_to_dict(array):
	d = {}
	M, N, _ = array.shape
	for i in range(M):
		for j in range(N):
			d[(i, j)] = array[i][j][0]
	return d

def dict_to_array(d, shape):
	array = np.empty(shape, dtype='float32')
	for k, v in d.items():
		i, j = k
		array[i][j][0] = np.float32(v)
	return array
	
def to_grey_array(array):
	H, W, _ = array.shape
	new_array = np.empty([H, W, 1])
	for i in range(H):
		for j in range(W):
			new_array[i][j][0] = np.sum(array[i][j], dtype='float32')/3
	return new_array

def blurArrayImage(a_img):
	# a_img = array image
	# d_img = dictionary (height) image
	d_img = array_to_dict(a_img)
	qc = qb.height2circuit(d_img)
	partial_x(qc, op('blurconstant')['chan1'])
	b_d_img = qb.circuit2height(qc)
	b_a_img = dict_to_array(b_d_img, a_img.shape)
	return b_a_img
	
def onCook(scriptOp):
	a_img = to_grey_array(op('SRC').numpyArray(delayed = True))
	r_a_img = blurArrayImage(a_img)
	scriptOp.copyNumpyArray(r_a_img)
