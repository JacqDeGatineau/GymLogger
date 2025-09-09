def get_exercises():
    sql = """SELECT t.id, t.title, t.link,
             FROM exercises t,
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)