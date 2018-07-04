# 导出数据结果
import datetime

import pandas as pd

head = ["instance", "machine"]
data = [["ss","aa" ],["ss","aa" ],["ss","aa" ],["ss","aa" ]]

df = pd.DataFrame(data, columns=head)
df.to_csv(("../submit/submit_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"), header=None, index=False)
