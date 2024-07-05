import psycopg2
import sys
import time
import RPi.GPIO as GPIO
from time import sleep
from configparser import ConfigParser

def read_text_msg(filename):
    text_msg = open(filename, "r")
    lines = text_msg.readlines()
    text_msg.close()
    sms_msg = {}
    sms_msg[0] = lines[0][7:].strip()
    sms_msg[1] = lines[13].strip()
    return sms_msg

def write_text_msg(filename, to, msg_body):
    text_msg = open(filename, "w")
    text_msg.write("To: 1")
    text_msg.write(to)
    text_msg.write("\n\n")
    text_msg.write(msg_body)
    text_msg.close()

def load_config(filename='/var/spool/sms/gate.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def get_id_for_property(house_number):
    config = load_config()
    sql = "SELECT id FROM property WHERE house_number = '{0}';".format(house_number)
    property_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    property_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return property_id

def get_role_name_for_id(role_id):
    config = load_config()
    sql = "SELECT role_name FROM user_roles WHERE id = '{0}';".format(role_id)
    role_name = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    role_name = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return role_name

def get_house_number_for_property_id(property_id):
    config = load_config()
    sql = "SELECT house_number FROM property WHERE id = '{0}';".format(property_id)
    house_number = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    house_number = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return house_number

def get_property_id_for_user(phone_number):
    config = load_config()
    sql = "SELECT property_id FROM users WHERE phone_number = '{0}';".format(phone_number)
    user_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_id

def get_id_for_user(phone_number):
    config = load_config()
    sql = "SELECT id FROM users WHERE phone_number = '{0}';".format(phone_number)
    user_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_id

def get_id_for_user_role(role_name):
    config = load_config()
    sql = "SELECT id FROM user_roles WHERE role_name = '{0}';".format(role_name)
    user_role_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_role_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_role_id

def get_role_name_for_user_id(user_id):
    config = load_config()
    sql = "SELECT ur.role_name FROM user_roles ur, users u WHERE ur.id = u.user_role_id AND u.id = '{0}';".format(user_id)
    user_role_name = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_role_name = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_role_name

def get_role_id_for_tn(tn):
    config = load_config()
    sql = "SELECT user_role_id FROM users WHERE phone_number = '{0}';".format(tn)
    user_role_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_role_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_role_id

def get_id_for_action(action_name):
    config = load_config()
    sql = "SELECT id FROM actions WHERE action_name = '{0}';".format(action_name)
    action_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    action_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return action_id

def add_user(tn, role, property):
    config = load_config()
    sql = "INSERT INTO users (phone_number, user_role, property_id) VALUES ('{0}', '{1}', '{2}') RETURNING id;".format(tn, role, property)
    user_id = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    user_id = rows[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return user_id

def update_user(id, tn, role, property):
    config = load_config()
    sql = "UPDATE users SET phone_number = '{0}', user_role = '{1}', property_id = '{2}' WHERE id = '{3}';".format(tn, role, property, id)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return id

def delete_user(id):
    config = load_config()
    sql = "DELETE FROM users WHERE id = '{0}';".format(id)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return id

def add_history(user_id, property_id, guest_tn, gate_msg_text, action_id):
    ensure_history_partition_is_active()
    date = get_partition_date()
    config = load_config()
    sql = "INSERT INTO history (property_id, user_id, guest_tn, gate_msg_text, action_id, event_date) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}') RETURNING id;".format(property_id, user_id, guest_tn, gate_msg_text, action_id, date)
    history_id = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    history_id = rows[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return history_id

def get_partition_date():
    config = load_config()
    sql = "SELECT current_date;"
    date = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    date = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return date
    
def ensure_history_partition_is_active():
    status = check_history_partition_status()
    if status == "detached":
        attach_history_partition()
    elif status == "does_not_exist":
        create_history_partition()
        attach_history_partition()

def soft_delete_history_partition():
    status = check_history_partition_status()
    if status == "attached":
        detach_history_partition()

def delete_history_partition():
    status = check_history_partition_status()
    if status == "attached":
        detach_history_partition()
        delete_history_partition_table()
    elif status == "detached":
        delete_history_partition_table()

def check_history_partition_status():
    config = load_config()
    partition_table_name = "history_{0}".format(get_partition_date()).replace("-", "_")
    sql = "SELECT relispartition FROM pg_class WHERE relname = '{0}';".format(partition_table_name)
    status = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    if rows[0]:
                        status = "attached"
                    else:
                        status = "detached"
                else:
                    status = "does_not_exist"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return status

def create_history_partition():
    partition_table_name = "history_{0}".format(get_partition_date()).replace("-", "_")
    config = load_config()
    sql = "CREATE TABLE IF NOT EXISTS {0} (LIKE {1} INCLUDING DEFAULTS INCLUDING CONSTRAINTS);".format(partition_table_name, "history")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def attach_history_partition():
    date = get_partition_date()
    partition_table_name = "history_{0}".format(date).replace("-", "_")
    config = load_config()
    sql = "ALTER TABLE {0} ATTACH PARTITION {1} FOR VALUES IN ('{2}');".format("history", partition_table_name, date)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def detach_history_partition():
    partition_table_name = "history_{0}".format(get_partition_date()).replace("-", "_")
    config = load_config()
    sql = "ALTER TABLE {0} DETACH PARTITION {1};".format("history", partition_table_name)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_history_partition_table():
    partition_table_name = "history_{0}".format(get_partition_date()).replace("-", "_")
    config = load_config()
    sql = "DROP TABLE {0};".format(partition_table_name)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def open_gate(tn, command):
    print("Opening gate!")
    GPIO.output(17, True)
    add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 1)
    sleep(2)
    GPIO.output(17, False)

def access_list(tn, command):
    config = load_config()
    sql = "SELECT u.phone_number, ur.role_name FROM users u, user_roles ur WHERE u.user_role_id = ur.id AND u.property_id = '{0}';".format(get_property_id_for_user(tn))
    to = tn
    body = None
    filename = tn, ".list.", int(time.time())
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = body, "\n{0},{1}".format(row[0], row[1])
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 3)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_list_all(tn, command):
    config = load_config()
    sql = "SELECT u.phone_number, ur.role_name FROM users u, user_roles ur WHERE u.user_role_id = ur.id;"
    to = tn
    body = None
    filename = tn, ".list_all.", int(time.time())
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = body, "\n{0},{1}".format(row[0], row[1])
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 3)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_history(tn, command):
    config = load_config()
    sql = "SELECT u2.phone_number, event_time, guest_tn, gate_msg_text, a.action_name FROM actions a, users u, users u2, history h WHERE a.id = h.action_id AND u.property_id = h.property_id AND u2.id = h.user_id AND u.property_id = '{0}';".format(get_property_id_for_user(tn))
    to = tn
    body = None
    filename = tn, ".history.", int(time.time())
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = body, "\n{0},{1},{2},{3},{4}".format(row[0], row[1], row[2], row[3], row[4])
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 4)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_history_all(tn, command):
    config = load_config()
    sql = "SELECT u2.phone_number, event_time, guest_tn, gate_msg_text, a.action_name FROM actions a, users u, users u2, history h WHERE a.id = h.action_id AND u.property_id = h.property_id AND u2.id = h.user_id;"
    to = tn
    body = None
    filename = tn, ".history_all.", int(time.time())
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = body, "\n{0},{1},{2},{3},{4}".format(row[0], row[1], row[2], row[3], row[4])
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 4)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def user_exists(tn):
    config = load_config()
    sql = "SELECT 1 FROM users WHERE phone_number = '{0}';".format(tn)
    exists = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    exists = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return exists

def add_access(tn, command, new_tn, role_id, property_id):
    if not user_exists(new_tn):
        config = load_config()
        sql = "INSERT INTO users (phone_number, user_role_id, property_id) VALUES ({0}, {1}, {2});".format(new_tn, role_id, property_id)
        to = tn
        body = None
        filename = tn, ".add_access.", int(time.time())
        try :
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    body = "{0} added as {1} to house number {2}".format(new_tn, get_role_name_for_id(role_id), get_house_number_for_property_id(property_id))
            write_text_msg(filename, to, body)
            add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 4)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def remove_access(tn, command, old_tn, property_id):
    if not user_exists(old_tn):
        config = load_config()
        sql = "DELETE FROM users WHERE id = '{0}';".format(user_id)
        to = tn
        body = None
        filename = tn, ".remove_access.", int(time.time())
        try :
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    body = "{0} removed from house number {1}".format(old_tn, get_house_number_for_property_id(property_id))
            write_text_msg(filename, to, body)
            add_history(get_id_for_user(tn), get_property_id_for_user(tn), -1, command, 4)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def guest(tn, command):
    print("TODO")

def help_response(tn, command, user_role_id):
    to = tn
    body = None
    filename = tn, ".help.", int(time.time())
    if user_role_id == 1: # Banned
        body = "This number is not allowed to access this system"
    elif user_role_id == 2: # Resident
        body = "The following options are available:\n\n'help' to see this message\n'open' - to open the gate"
    elif user_role_id == 3: # Property owner
        body = "The following options are available:\n\n'help' to see this message\n'open' - to open the gate\n'access list' - to see the access configuration for your property\n'history' - to see the usage history for your property"
    elif user_role_id == 4: # Admin
        body = "The following options are available:\n\n'help' to see this message\n'open' - to open the gate\n'access list' - to see the access configuration for your property\n'history' - to see the usage history for your property\n'access list all' - to see the access configuration for all properties\n'history all' - to see the usage history for all properties"
    else:
        body = "Send a message like the provided example, be sure the house number for the property to which you are visiting is at the beginning of the message.\n\nExample '3021 This is George, please open the gate'"
    write_text_msg(filename, to, body)
    add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 2)

def initGPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, False)

def handle_msg(tn, command, user_role_id):
    if user_role_id > 3: #ADMIN
        if command == "access list all":
            access_list_all(tn, command)
        if command == "access history all":
            access_history_all(tn, command)
    if user_role_id > 2: #PROPERTY_OWNER or higher
        if command == "add ...":
            #add_access(tn, command, new_tn, role_id, get_property_id_for_user(tn))
            print("TODO")
        if command == "remove ...":
            #remove_access(tn, command, old_tn, get_property_id_for_user(tn))
            print("TODO")
        if command == "access list":
            access_list(tn, command)
        if command == "access history":
            access_history(tn, command)
    if user_role_id > 1: #RESIDENT or higher
        if command == "open":
            open_gate(tn, command)
    if command == "<house number> This is <guest name>, please open the gate.":
        guest(tn, command)
    if command == "help":
        help_response(tn, command, user_role_id)

if __name__ == '__main__':
    initGPIO()
    if sys.argv[1] == 'RECEIVED':
        msg = read_text_msg(sys.argv[2])
        handle_msg(msg[0], msg[1].strip().lower(), get_role_id_for_tn(msg[0]))