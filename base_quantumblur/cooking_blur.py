def onCook(scriptOp):
	qc = me.fetch('qc')
	b_a_img = me.fetch('b_a_img')
	if qc is None:
		print("everything set to None")
	elif b_a_img is None:
		print("blurred image not ready yet")
	else:
		scriptOp.copyNumpyArray(b_a_img)