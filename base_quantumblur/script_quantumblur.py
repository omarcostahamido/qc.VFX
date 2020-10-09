# me - this DAT
# scriptOp - the OP which is cooking

# # press 'Setup Parameters' in the OP to call this function to re-create the parameters.
# def onSetupParameters(scriptOp):
# 	page = scriptOp.appendCustomPage('Custom')
# 	p = page.appendFloat('Valuea', label='Value A')
# 	p = page.appendFloat('Valueb', label='Value B')
# 	return

import sys
import quantumblur as qb
from PIL import Image
import numpy as np
import threading
import time
import copy
print('imported')

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
  return new_array [:, :, :1]
# def to_grey_array(array):
# 	H, W, _ = array.shape
# 	new_array = np.empty([H, W, 1])
# 	for i in range(H):
# 		for j in range(W):
# 			new_array[i][j][0] = np.sum(array[i][j], dtype='float32')/3
# 	return new_array
	
def prepare_img():
	global src, a_img, d_img, qc
	if src is None or (src != op('SRC').numpyArray(delayed = True)).any():
		print('prepared!')
		src = op('SRC').numpyArray(delayed = True)
		print("src.shape is: "+str(src.shape))
		a_img = timed_run(to_grey_array, "2ga", src)
		print("a_img.shape is: "+str(a_img.shape))
		# d_img = timed_run(array_to_dict, "a2d", a_img)
		qc = timed_run(qb.aheight2circuit, "h2c", a_img)
	
def timed_run(func, func_name, *args, **kargs):
	time1 = time.time()
	value = func(*args, **kargs)
	time2 = time.time()
	print(f"Time for {func_name}:", time2-time1)
	return value

def blurArrayImage():
	global a_img, d_img, qc
	new_qc = timed_run(copy.deepcopy, "copy_qc", qc)
	timed_run(partial_x, "partial_x", new_qc, op('blurconstant')['chan1'])
	# parent(2).op('blurconstant')['chan1']
	b_d_img = timed_run(qb.circuit2height, 'c2h', new_qc)
	b_a_img = timed_run(dict_to_array, "d2a", b_d_img, a_img.shape)
	return b_a_img

a_img = None
d_img = None
qc = None
src = None

def onCook(scriptOp):
	global a_img, d_img, qc, src
	prepare_img()
	r_a_img = blurArrayImage()
	scriptOp.copyNumpyArray(r_a_img)
