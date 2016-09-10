#!/usr/bin/python

import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.htm")
        print 'received a request'


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        uni_id = ''
        try:
            uni_id = self.request.headers['Uni_id']
        except Exception as error:
            print "UploadHandler cannot get Uni_id in Request's header"
		
        print 'Uploader =', uni_id
		
        file_contents = self.request.files['file'][0].body
        file_ori_name = self.request.files['file'][0].filename

        print 'get', file_ori_name

        print self.request.uri

        with open(u"uploads/"+file_ori_name, "wb") as f:
            f.write(file_contents)
        self.finish()


if __name__ == "__main__":
    handers = [
                    (r"/file-upload", UploadHandler),
                    (r"/", MainHandler),
                    (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
                ]
    settings = dict(
                        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                        debug=True
                    )

    application = tornado.web.Application(handers, **settings)

    application.listen(8964)
    tornado.ioloop.IOLoop.instance().start()
