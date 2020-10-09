import sys

spacer = "- " * 5

for each in sys.path:
	print(each)

print(spacer)

python_ext = tdu.expandPath(ipar.ExtPython.Target)

sys.path.insert(0,python_ext)
if python_ext not in sys.path:
	sys.path.append(python_ext)

for each in sys.path:
	print(each)

print(spacer)