import copy
import sys
# replace with your path to QuantumBlur
#sys.path.insert(1, 'C:/Users/Chris/Documents/GitHub/qc.VFX/QuantumBlur')
import quantumblur as qb
from PIL import Image
import numpy as np
import threading
import time

def timed_run(func, func_name, *args, **kargs):
	print()
	print(f"Running {func_name}...")
	time1 = time.time()
	value = func(*args, **kargs)
	time2 = time.time()
	print(f"Time for {func_name}:", time2-time1)
	print()
	return value
        
def array_to_IMG(array):
	return Image.fromarray(np.uint8(array * 255) , 'L')
	
def array_to_dict(array):
	d = {}
	M, N, _ = array.shape
	for i in range(M):
		for j in range(N):
			d[(i, j)] = array[i][j][0]
	return d

def to_grey_array(array):
	return array[:, :, :1]

def partial_x(qc,fraction):
    for j in range(qc.num_qubits):
        qc.rx(np.pi*fraction,j)
        
def dict_to_array(d, shape):
	array = np.empty(shape, dtype='float32')
	for k, v in d.items():
		i, j = k
		array[i][j][0] = np.float32(v)
	return array
	
def build_and_blur(src, a_img, d_img, qc, current_img, parameter):
	if src is None or (src != current_img).any() or \
	any(i is None for i in [src, a_img, d_img, qc]):
		print('prepared!')
		src = current_img
		a_img = timed_run(to_grey_array, "2ga", src)
		#d_img = timed_run(array_to_dict, "a2d", a_img)
		qc = timed_run(qb.aheight2circuit, "h2c", a_img)
		me.parent().store("src", src)
		me.parent().store("a_img", a_img)
		me.parent().store("d_img", d_img)
		me.parent().store("qc", qc)
		print('circuit preparation done')
	else:
		print('circuit preparation skipped')
	if qb.simple_python:
		new_qc = timed_run(copy.deepcopy, "deepcopy qc", qc)
	else:
		new_qc = timed_run(qc.copy, "qc.copy")
	timed_run(partial_x, "partial_x", new_qc, parameter)
	b_a_img = timed_run(qb.acircuit2height, 'c2h', new_qc)
	#b_a_img = timed_run(dict_to_array, "d2a", b_d_img, a_img.shape)
	me.parent().store("b_a_img", b_a_img)
	print("build and blur done")

src = me.fetch('src')
a_img = me.fetch('a_img')
d_img = me.fetch('d_img') 
qc = me.fetch('qc')
threading.Thread(target=build_and_blur, args=(src, a_img, d_img, qc,\
 op('SRC').numpyArray(delayed = False), op('blurconstant')['chan1'])).start()
