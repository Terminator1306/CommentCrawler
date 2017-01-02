#coding:utf-8
import pymongo
import MySQLdb
import json

mongodb = pymongo.MongoClient("127.0.0.1", 27017)["crawl"]
mysqldb = MySQLdb.Connection("127.0.0.1","root","12345","scrapy")
mysql_cursor = mysqldb.cursor()
mysql_cursor.execute('set names utf8')

mongodb_cursor = mongodb['comment'].find({})
for item in mongodb_cursor:
    try:
        # item = mongodb_cursor.next()
        sql = "insert into comment (product_id, comment_id, referenceName, creationTime, userlevel, usefulVoteCount, uselessVoteCount, userProvince, score, userRegisterTime, content) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(item['product_id'],
                    item['comment_id'],item['referenceName'],item['creationTime'],item['userlevel'],item['usefulVoteCount'],item['uselessVoteCount'],item['userProvince'],item['score'],item['userRegisterTime'],item['content'])
        mysql_cursor.execute(sql.encode("utf-8"))
        # mysqldb.commit()
        print item["product_id"],item["comment_id"]
    except Exception,e:
        print e
mysqldb.commit()