def mult_scalar(matrix, scale):
	scaled_matrix = []
	if len(matrix) > 0 and len(matrix[0]) > 0:
		for i in range(len(matrix)):
			scaled_matrix.append([])
			for j in range(len(matrix[0])):
				scaled_matrix[i].append(scale * matrix[i][j])
		return scaled_matrix
	else:
		return matrix

def mult_matrix(a, b):
	multiplied_matrix = []
	if len(a) * len(b) * len(b[0]) > 0 and len(a[0]) == len(b):
		for i in range(len(a)):
			multiplied_matrix.append([])
			for j in range(len(b[0])):
				result = 0
				for k in range(len(a[0])):
					result += a[i][k] * b[k][j]
				multiplied_matrix[i].append(result)
		return multiplied_matrix
	else:
		# if the inputs are invalid, return None
		return None
	
def euclidean_dist(a,b):
	if len(a) == 1 and len(a) == len(b) and len(a[0]) == len(b[0]):
		result = 0
		for i in range(len(a[0])):
			result += (a[0][i] - b[0][i])**2
		result = result**0.5
		return result
	else:
		# if the inputs are invalid, return -1
		return -1
