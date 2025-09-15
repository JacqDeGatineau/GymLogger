import db

def get_exercises():
    sql = """SELECT t.id, t.title, t.link
             FROM exercises t
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_exercises_by_ids(selected_exercises):
    if not selected_exercises:
        return []

    placeholders = ', '.join(['?'] * len(selected_exercises))
    print(placeholders)
    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id IN ({placeholders})"""
    
    return db.query(sql, selected_exercises)