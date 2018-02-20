import pymysql
db=pymysql.connect('localhost','root','192837','zhihu_comments')
# 使用cursor()方法获取操作游标
cursor = db.cursor()


item={'article_id':996}

# SQL 更新语句
sql="insert into commnet1 VALUES({article_id}," \
            "{column_id},{comments_author},{pin_id},{question_id}," \
            "{roundtable_id},{thanks_count},{time},{title}," \
            "{topics},{type},{url_token},{user_id},{voteup_count})".format(
            article_id=item.get('article_id','Null'),
            column_id=item.get('column_id','Null'),
            comments_author=item.get('comments_author','Null'),
            pin_id=item.get('pin_id','Null'),
            question_id=item.get('question_id','Null'),
            roundtable_id=item.get('roundtable_id','Null'),
            thanks_count=item.get('thanks_count','Null'),
            time=item.get('time','Null'),
            title= item.get('title','Null'),
            topics= item.get('topics','Null'),
            type= item.get('type','Null'),
            url_token= item.get('url_token','Null'),
            user_id=item.get('user_id','Null'),
            voteup_count=item.get('voteup_count','Null'))
sql1="insert into commnet1 VALUES({article_id}," \
            "{column_id},{comments_author},{pin_id},{question_id}," \
            "{roundtable_id},{thanks_count},{time},{title}," \
            "{topics},{type},{url_token},{user_id},{voteup_count})".format(
            article_id=998,
            column_id=item.get('column_id','Null'),
            comments_author=item.get('comments_author','Null'),
            pin_id=item.get('pin_id','Null'),
            question_id=item.get('question_id','Null'),
            roundtable_id=item.get('roundtable_id','Null'),
            thanks_count=item.get('thanks_count','Null'),
            time=item.get('time','Null'),
            title= item.get('title','Null'),
            topics= item.get('topics','Null'),
            type= item.get('type','Null'),
            url_token= item.get('url_token','Null'),
            user_id=item.get('user_id','Null'),
            voteup_count=item.get('voteup_count','Null'))
#try:
# 执行SQL语句
cursor.execute(sql)
cursor.execute(sql1)
# 提交到数据库执行
db.commit()
#except:
    # 发生错误时回滚
 #   db.rollback()

# 关闭数据库连接
db.close()