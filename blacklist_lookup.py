import threading
import dns.resolver
import queue
import pymongo 

class blacklist_lookup:
    __record = str()

    def getLookup(self, ip, blacklist):
        self.ip = ip
        self.blacklist = blacklist
        myIP = ip
        bl = blacklist
        result=[]
        try:
            query = '.'.join(reversed(str(myIP).split("."))) + "." + bl

            answer = dns.resolver.query(query, "A")
            answer_txt = dns.resolver.query(query, "TXT")
            result.append("ip_blacklist_status{blacklist="+ '"' + bl+ '"' + "} 1 ")
        except dns.resolver.NXDOMAIN:
            result.append("ip_blacklist_status{blacklist="+ '"' + bl+ '"' + "} 0 ")
        except dns.resolver.NoAnswer:
            result.append("ip_blacklist_status{blacklist="+ '"' + bl+ '"' + "} 0 ")
        except dns.resolver.NoNameservers:
            result.append("ip_blacklist_status{blacklist="+ '"' + bl+ '"' + "} 0 ")
        except dns.exception.Timeout:
            result.append("ip_blacklist_status{blacklist="+ '"' + bl+ '"' + "} 0 ")
        return result

    def setAnswerJsonFormat(self, lookupresult):
        self.lookupresult = lookupresult
        jsonAnswer = []
        for res in lookupresult:
            bresult = {
                #'blacklist':str(res).replace("[","").replace("]","").replace("\"","").replace("'", "")
                'blacklist':str(res).replace("[","").replace("]","").replace("'", "")
            }
            jsonAnswer.append(bresult)
        return jsonAnswer

    def setLookupParam(self, record):
        self.record = record
        record = record
        threads = []
        my_queue = queue.Queue()
        blresult = []
        for bl in blacklists:
            bl = str(bl).replace("('","").replace("',)","")
            process = threading.Thread(target=my_queue.put(self.getLookup(record, bl)))
            threads.append(process)
            process.start()
            process.join()
        while not my_queue.empty():
            blresult.append(str(my_queue.get()))

        #return self.setAnswerJsonFormat(blresult)
        return (blresult)