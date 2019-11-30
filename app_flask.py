from flask import Flask, request, jsonify, render_template, Response
#from jinja2 import Environment, FileSystemLoader

from blacklist_lookup import *
#from middleware import setup_metrics

app = Flask(__name__)
#setup_metrics(app)

@app.route('/monitor')
def test():
    ip = request.args.get('ip')
    print(ip)
    if (ip is None):
        return "Exporter"
    blacklist = blacklist_lookup()
    blacklist = blacklist.setLookupParam(ip)
    #results = {'results': blacklist}

    t = "# HELP ip_blacklist history\n# TYPE ip_blacklist gauge\n"
    for b in blacklist:
        t += str(b).replace("[","").replace("]","").replace("'", "") + "\n"
    print(t)

    #return render_template('return.html', result=results )
    return Response(t, mimetype='text/plain')
@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

if __name__ == '__main__':
   app.run(debug=False,host='0.0.0.0', port=5002)