# -*- coding: utf-8 -*-
import json,urllib2

textmod={"guides":[],"source":{"nodes":[{"shape":"customNode","x":110,"y":40,"anchorPoints":[[0.5,1]],"id":"11","title":"hiveTable","nodeOpts":{"optsEntity":{"dbname":"default","tablename":"sample_svm_data2"},"comName":"hiveTable","comCode":"hiveTable"}},{"shape":"customNode","x":110,"y":150,"anchorPoints":[[0.5,0],[0.5,1]],"id":"22","title":"随机森林","nodeOpts":{"optsEntity":{"featuresCol":"f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16","labelCol":"label"},"comName":"随机森林","comCode":"randomForestCom"}},{"shape":"customNode","x":160,"y":260,"anchorPoints":[[0.25,0],[0.5,0],[0.5,1]],"id":"33","title":"预测","nodeOpts":{"optsEntity":{"probabilityCol":"probability","featuresCol":"f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16","predictionCol":"prediction"},"comName":"预测","comCode":"predictionCom"}},{"shape":"customNode","x":280,"y":40,"anchorPoints":[[0.5,1]],"id":"44","title":"hiveTable","nodeOpts":{"optsEntity":{"dbname":"default","tablename":"sample_svm_data2"},"comName":"hiveTable","comCode":"hiveTable"}}],"edges":[{"sourceAnchor":"out1","targetAnchor":"in1","shape":"polyLineFlow","source":"11","id":"80492c4f","controlPoints":[{"x":150,"y":80.5},{"x":150,"y":149.5}],"target":"22"},{"sourceAnchor":"out1","targetAnchor":"in1","shape":"polyLineFlow","source":"22","id":"ac9cd7f7","controlPoints":[{"x":150,"y":190.5},{"x":179.75,"y":259.5}],"target":"33"},{"sourceAnchor":"out1","targetAnchor":"in2","shape":"polyLineFlow","source":"44","id":"c2d54467","controlPoints":[{"x":320,"y":80.5},{"x":200,"y":259.5}],"target":"33"}]}}
textmod = json.dumps(textmod)
print(textmod)
#输出内容:{"params": {"password": "zabbix", "user": "admin"}, "jsonrpc": "2.0", "method": "user.login", "auth": null, "id": 1}
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
url='http://localhost:5000/tasks/test'
req = urllib2.Request(url=url,data=textmod,headers=header_dict)
res = urllib2.urlopen(req)
res = res.read()
print(res)