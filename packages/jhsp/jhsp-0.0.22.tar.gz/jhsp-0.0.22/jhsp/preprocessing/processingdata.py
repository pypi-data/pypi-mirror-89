import pandas as pd

class ProcessingData():

    def __init__(self, old_dir):
        self.data = self.data = pd.read_excel(old_dir,header=0)   # 第一行默认为表头，数据第一行必须有表头
        self.save_dir = os.path.dirname(old_dir)       # 默认保存路径为原数据同一目录

    def selecting_variance(self,percentage):
        from sklearn.feature_selection import VarianceThreshold
        vt = VarianceThreshold(threshold=(percentage*(1-percentage)))               # 布尔特征是伯努利随机变量，方差为 p(1-p)

    def selecting_lasso(self):
        save_path = os.path.join(self.save_dir,'lasso_weight.xlsx')

        from sklearn.linear_model import LassoCV
        from sklearn.preprocessing import StandardScaler
        import numpy as np

        x, y = self.x, self.y
        x = StandardScaler().fit_transform(x)  # lasso必须先标准化


        lasso = LassoCV(cv=5) # 最优alpha竟然是0.00012463621602719477，所有千万不要自己设置字典，就用自动的才行
        lasso.fit(x, y)
        weight = lasso.coef_
        lasso_weight =  pd.DataFrame(data=weight, index=self.data.iloc[:,:-1].columns.values,columns=['weight'])
        lasso_weight.to_excel(save_path)





