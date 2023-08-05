import os
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import json 
import scipy
import scipy.special
from scipy.stats import shapiro
import time
from progress.bar import Bar

class createSamplesCSV():
	def __init__(self,exp_data,n=100,projectName="S570_project"):
		self.exp_data=exp_data.iloc[:n]
		self.projectName=projectName
	def loadDefaultData(self):
		print("Load","DEFAULT DATA")
		GO_Voc_path=os.path.join(os.getcwd(),"Data","GO_Voc.json")
		GO_DescriptVoc_path=os.path.join(os.getcwd(),"Data","GO_DESCRIPT_VOC.json")
		with open(GO_Voc_path,"r") as f:
			self.GO_Voc=json.load(f)
		with open(GO_DescriptVoc_path,"r") as f:
			self.GO_DescriptVoc=json.load(f)
	def createCSV(self,big_index=1000):
		self.samples=list(self.exp_data.columns)
		self.outPutFolder=os.path.join(os.getcwd(),self.projectName,"SampleDescriptionCSV")
		os.mkdir(os.path.join(os.getcwd(),self.projectName))
		os.mkdir(self.outPutFolder)
		self.shapiroTest_Pvalue_VOC={}
		number_=0
		bar = Bar("Create samples _DESCRIPT.csv", max = len(list(self.samples)))
		for c in self.samples:
			exampleSample=self.exp_data[c]*big_index
			GO_ExpValueVoc={}
			number_+=1
			for i,k in enumerate(list(self.GO_Voc.keys())):
				indexProbID=set(exampleSample.index)&set(self.GO_Voc[k])
				if list(indexProbID)==[]:
					continue
				#print(c,i,k,float(exampleSample.loc[self.GO_Voc[k]].mean()))
				GO_ExpValueVoc[k]=float(exampleSample.loc[self.GO_Voc[k]].mean())
			expValue=[GO_ExpValueVoc[p] for p in list(GO_ExpValueVoc.keys())]
			zScoreExpValue=(np.array(expValue)-np.array(expValue).mean())/np.array(expValue).std()
			p_value = 1 - scipy.special.ndtr(np.abs(zScoreExpValue))
			GO_AnalyseDataFrame=pd.DataFrame()
			GO_AnalyseDataFrame["GO"]=list(GO_ExpValueVoc.keys())
			GO_AnalyseDataFrame["GO_ExpMeanValue"]=expValue
			GO_AnalyseDataFrame["GO_zScore"]=zScoreExpValue
			GO_AnalyseDataFrame["GO_pValue"]=p_value
			GO_AnalyseDataFrame.index=list(GO_ExpValueVoc.keys())
			categoryGO=[]
			shapiroTest_Pvalue=shapiro(expValue)[1]
			self.shapiroTest_Pvalue_VOC[c]=shapiroTest_Pvalue
			for a,b in zip(GO_AnalyseDataFrame.GO_zScore,GO_AnalyseDataFrame.GO_pValue):
				if a>0 and b<0.05:
					categoryGO.append("DP")
				elif a<0 and b<0.05:
					categoryGO.append("DN")
				else:
					categoryGO.append("DZ")
			GO_AnalyseDataFrame["GO_category"]=categoryGO
			EXP_GO=list(GO_AnalyseDataFrame.index)
			EXP_GO_type=[]
			for e in EXP_GO:
				try:
					EXP_GO_type.append(self.GO_DescriptVoc[e]["namespace"])
				except KeyError:
					EXP_GO_type.append("---")
			EXP_GO_descript=[]
			for e in EXP_GO:
				try:
					EXP_GO_descript.append(self.GO_DescriptVoc[e]["name"])
				except KeyError:
					EXP_GO_descript.append("---")
			GO_AnalyseDataFrame["GO_type"]=EXP_GO_type
			GO_AnalyseDataFrame["GO_name"]=EXP_GO_descript
			EXP_GO_probID_count=[len(self.GO_Voc[u]) for u in list(GO_AnalyseDataFrame.index)]
			GO_AnalyseDataFrame["GO_probID_count"]=EXP_GO_probID_count
			GO_AnalyseDataFrame.to_csv(os.path.join(self.outPutFolder,c+"_DESCRIPT.csv"))
			del GO_AnalyseDataFrame
			bar.next()
		bar.finish()
	def SampleEXP_value_shapiroTest(self):
		return self.shapiroTest_Pvalue_VOC
	def seeShapirotestPlot(self):
		pValue=[self.shapiroTest_Pvalue_VOC[c] for c in list(self.shapiroTest_Pvalue_VOC.keys())]
		plt.plot(pValue,self.samples)
		plt.subplots_adjust(left=0.245, right=0.64, top=0.995, bottom=0.09)
		plt.show(block=True)

class createDF_GO_csv():
	def __init__(self,CSV_folderPawth):
		self.CSV_folderPawth=CSV_folderPawth
	def createCSV(self):
		folderContentFiles=os.listdir(self.CSV_folderPawth)
		csvFiles=[ c for c in folderContentFiles if c[-4:]==".csv"]
		self.DF_GO_csv=pd.DataFrame()
		self.DF_GO_zScore=pd.DataFrame()
		a={"DZ":0,"DP":1,"DN":-1}
		for c in csvFiles:
			sampleDescriptDataset=pd.read_csv(os.path.join(self.CSV_folderPawth,c),index_col=0)
			sampleName=c.split(".")[0].split("_")[0]
			category=np.array([a[u] for u in list(sampleDescriptDataset["GO_category"])])
			zScore=np.array(sampleDescriptDataset["GO_zScore"])
			pValue=np.array(sampleDescriptDataset["GO_pValue"])
			self.DF_GO_csv[sampleName]=list(category*(1-pValue))
			self.DF_GO_zScore[sampleName]=list(zScore)
		self.DF_GO_csv.index=sampleDescriptDataset.index
		self.DF_GO_zScore.index=sampleDescriptDataset.index
		return "FINSHED create DF_GO_zScore,DF_GO_csv for get please example.*"
	def saveCSV(self,projectName):
		self.projectName=projectName
		os.mkdir(os.path.join(os.getcwd(),self.projectName,"sampleAnalyseCSV"))
		file_name_category="categoryDF.csv"
		file_name_zScore="zScoreDF.csv"
		self.DF_GO_csv.to_csv(os.path.join(os.getcwd(),self.projectName,"sampleAnalyseCSV",file_name_category))
		self.DF_GO_csv.to_csv(os.path.join(os.getcwd(),self.projectName,"sampleAnalyseCSV",file_name_zScore))
		return "Create sample DF_GO _CSV"

class createLabel_DF_csv():
	def __init__(self,sampleData):
		self.sampleData=sampleData 
	def getMetaData(self,metaDataPath):
		self.metaDataPath=metaDataPath
		self.metaData=pd.read_csv(self.metaDataPath,index_col=0)
		self.metaData=self.metaData.sort_values(by=["label"])
		return (self.metaData).columns
	def transforming(self):
		self.label_=list(self.metaData["GSM"])
		self.sampleData=self.sampleData[self.label_]
	def analyseSamplesData(self):
		label_set=list(set((self.metaData["label"])))
		meanLabel_Dataset=pd.DataFrame()
		for c in sorted(label_set):
			exampleLabel_GSM=self.metaData[self.metaData.label==c].GSM
			exampleLabel_Data=self.sampleData[list(exampleLabel_GSM)]
			meanLabel_Value=exampleLabel_Data.mean(axis=1)
			meanLabel_Dataset[c]=meanLabel_Value
			print(c)
		meanLabel_Dataset.index=exampleLabel_Data.index
		self.meanLabel_Dataset=meanLabel_Dataset
