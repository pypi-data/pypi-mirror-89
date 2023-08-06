import math
import matplotlib.pyplot as plt
from .Generaldietribution import Distribution

class Gaussian(Distribution):
	
	def __init__(self, mu=0, sigma=1):
		Distribution.__init__(self,mu,sigma)

	def calculate_mean(self):
		avg =1.0*sum(self.data)/len(self.data)
		self.mean=avg
		return self.mean

	def calculate_stdev(self,sample=True):
		"""
		样本(bool):数据是否代表样本或总体
		"""
		if sample:
			n=len(self.data)-1
		else:
			n=len(self.data)

		mean=self.calculate_mean()
		sigma =0
		for d in self.data:
			sigma+=(d-mean)**2

		sigma=math.sqrt(sigma/n)
		self.stdev=sigma
		return self.stdev

	def plot_histogram(self):
		"""
		画直方图
		"""
		plt.hist(self.data)
		plt.title('Histogram of Data')
		plt.xlabel('data')
		plt.ylabel('count')

	def pdf(self,x):
		"""
		高斯分布的密度函数：如下公式
		"""
		return (1.0/(self.stdev*math.sqrt(2*math.pi)))*math.exp(-0.5*((x-self.mean)/self.stdev)**2)

	def plot_histogram_pdf(self,n_spaces=50):
		"""
		画密度函数直方图
		"""
		mu =self.mean
		sigma =self.stdev

		min_range=min(self.data)
		max_range=max(self.data)

		interval=1.0*(max_range-min_range)/n_spaces
		x=[]
		y=[]
		for i in range(n_spaces):
			tmp=min_range+interval*i
			x.append(tmp)
			y.append(self.pdf(tmp))

		fig,axes =plt.subplots(2,sharex=True)
		fig.subplts_adjust(hspace=.5)
		axes[0].hist(self.data,density=True)
		axes[0].set_title('Normed Histogram of Data')
		axes[0].set_ylabel('Density')

		axes[1].plot(x,y)
		axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
		axes[1].set_ylabel('Density')
		plt.show()

		return x,y

	def __add__(self, other):
		"""
		两个高斯分布
		"""
		result =Gaussian()
		result.mean=self.mean+other.mean
		result.stdev=math.sqrt(self.stdev**2+other.stdev**2)

		return result

	def __repr__(self):
		"""
		输出结果
		"""
		return "mean {}, standeard deviation {}".format(self.mean, self.stdev)



