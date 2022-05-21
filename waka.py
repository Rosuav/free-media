import matplotlib.pyplot as plt
for angle in range(0, 50, 5):
	plt.pie([1.0 - angle / 180], startangle=angle, colors=["#ccaa00", "#ddaa00"])
	plt.savefig("pie%02d.png" % angle)
	if angle: plt.savefig("pie%02d.png" % (100 - angle))
	plt.close()
# convert pie*.png pie.gif
