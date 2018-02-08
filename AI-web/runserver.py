#!/storeage/glzheng/anaconda3/envs/python27_glzheng/bin/python

# -*- coding: utf-8 -*-
from poseidon import app
##
if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', debug=True, threaded=True)
#    app.run(debug=True, use_debugger=False, use_reloader=False)
