import web
import json
import threading

urls = ('/(.*)', 'API')
app = web.application(urls, globals())

db = {}
nextid = 0

# Very simple REST API application built with web.py
class API():
    def GET(self, id=None):
        data = web.input(switch_id='', status='', action='read')
        print data.module_id
        print data.switch_id
        print data.status
        
        if(len(id) == 0):
            return web.notfound()
        elif(id == 'config'):
            return json.dumps({'config': 1})
        elif(id == 'module'):
            return json.dumps({'module': 1})
        elif(id == 'switch'):
            return json.dumps({'switch': '1'})

        return web.notfound()

    def POST(self, id=None):
        global db, nextid
        
        db[nextid] = json.loads(web.data())
        nextid += 1
        return json.dumps({'created': nextid - 1})

    def DELETE(self, id):
        global db, nextid

        if(int(id) in db):
            db.pop(int(id))
            return json.dumps({'deleted': int(id)})
        else:
            return web.notfound()

    def PUT(self, id):
        global db, nextid

        if(int(id) in db):
            db[int(id)] = json.loads(web.data())
            return json.dumps({'updated': int(id)})
        else:
            return web.notfound()

def run_server():
    thread = threading.Thread(target = app.run)
    thread.start()
    return thread

if __name__ == '__main__':
    run_server()
