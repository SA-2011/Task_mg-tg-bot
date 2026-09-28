from connection import connection

async def get_user(telegram_id):
    try:
        con = await connection()
        users = await con.fetchrow("""
        select * from users1 where telegram_id = $1
        """, str(telegram_id))
        return users
    except Exception as error:
        print(f"Getting user error: {error}")
    finally:
        await con.close()

async def save_user(telegram_id , username , full_name):
    try:
        con = await connection()
        await con.execute("""
        insert into users1(user_name , full_name , telegram_id) values 
        ($1, $2, $3)
        """, username, full_name, str(telegram_id))
        print("User saved")
    except Exception as error:
        print(f"Error in saving user: {error}")
    finally:
        await con.close()

async def show_users(user_name , full_name , telegram_id):
    try:
        con = await connection()
        users = await con.fetchrow("""
        select * from users1 where user_name = $1 and full_name = $2 and telegram_id = $3
        """, user_name, full_name, str(telegram_id))
        return users
    except Exception as error:
        print(f"Error in showing users: {error}")
    finally:
        await con.close()

async def add_task(task_name, task_description, telegram_id):
    try:
        con = await connection()
        await con.execute("""
        insert into tasks (task_name , task_description , telegram_id) values
        ($1 , $2 , $3)
        """ , task_name , task_description , str(telegram_id))
    except Exception as error:
        print(f"Error in creating task: {error}")
    finally:
        await con.close()

async def show_your_tasks(tg_id):
    try:
        con = await connection()
        show_all = await con.fetch("""
        select * from tasks where telegram_id = $1
        """ , str(tg_id))
        return show_all
    except Exception as error:
        print(f"Error in dhowing tasks: {error}")
    finally:
        await con.close()

async def update_task(t_id , t_name , t_description , t_status , tg_id):
    try:
        con = await connection()
        await con.execute("""
        update tasks
        set task_name = $2 , task_description = $3 , task_status = $4
        where telegram_id = $5 and task_id = $1
        """ , int(t_id) , t_name , t_description , bool(t_status) , str(tg_id))
        print("Update finished")
    except Exception as error:
        print(f"Error in updating {error}")
    finally:
        await con.close()