import psycopg2
import sys
import time
import re
from configparser import ConfigParser

##################################################
### Text message operations ######################
##################################################
def read_text_msg(filename):
    text_msg = open(filename, "r")
    lines = text_msg.readlines()
    text_msg.close()
    sms_msg = {}
    sms_msg[0] = lines[0][7:].strip()
    sms_msg[1] = lines[13].strip()
    return sms_msg

def write_text_msg(filename, to, msg_body):
    text_msg = open("{0}{1}".format("/var/spool/sms/outgoing/", filename), "w")
    text_msg.write("To: 1")
    text_msg.write(str(to))
    text_msg.write("\n\n")
    text_msg.write(msg_body)
    text_msg.close()

def send_open_gate_msg():
    msg = open("{0}{1}".format("/var/spool/sms/gate/", int(time.time())), "w")
    msg.write("open")
    msg.close()

#################################################
### Database operations #########################
#################################################
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

def get_role_id_for_name(role_name):
    config = load_config()
    sql = "SELECT id FROM user_roles WHERE lower(role_name) = '{0}';".format(role_name)
    role_id = None
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchone()
                if rows:
                    role_id = rows[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return role_id

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
    user_role_id = 2 # Default to guest
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

def get_owners_for_property(house_number):
    config = load_config()
    sql = "SELECT u.phone_number FROM users u, property p WHERE u.user_role_id in (4, 5) AND u.property_id = p.id AND p.house_number = '{0}';".format(house_number)
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None

def add_inflight_operation(tn, property_id):
    config = load_config()
    sql = "INSERT INTO inflight (guest_tn, property_id) VALUES ('{0}', '{1}');".format(tn, property_id)
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_inflight_operations():
    config = load_config()
    sql = "SELECT DISTINCT guest_tn, property_id FROM inflight WHERE request_time > now() - INTERVAL '2 MINUTE';"
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return None

def clear_inflight_operations():
    config = load_config()
    sql = "TRUNCATE TABLE inflight;"
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def add_history(user_id, property_id, gate_msg_tn, gate_msg_text, action_id):
    ensure_history_partition_is_active()
    date = get_partition_date()
    config = load_config()
    if not user_id:
        user_id = 1
    if not property_id:
        property_id = 1
    sql = "INSERT INTO history (property_id, user_id, gate_msg_tn, gate_msg_text, action_id, event_date) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}') RETURNING id;".format(property_id, user_id, gate_msg_tn, gate_msg_text, action_id, date)
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

#################################################
### History partition operations ################
#################################################
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

#################################################
### User commands ###############################
#################################################
def open_gate(tn, command):
    """Ex: open"""
    send_open_gate_msg()
    filename = "{0}{1}{2}".format(tn, ".open.", int(time.time()))
    write_text_msg(filename, tn, "The gate is opening")
    add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 1)
    inflight_ops = get_inflight_operations()
    if inflight_ops:
        inflight_ops_property_id = inflight_ops[1]
        if get_property_id_for_user(tn) == inflight_ops_property_id:
            filename = "{0}{1}{2}".format(inflight_ops[0], ".guestopen.", int(time.time()))
            write_text_msg(filename, tn, "The gate is opening")
    clear_inflight_operations()

def access_list(tn, command):
    """Ex: access list"""
    config = load_config()
    sql = "SELECT DISTINCT u.phone_number, ur.role_name FROM users u, user_roles ur WHERE u.user_role_id = ur.id AND u.property_id = '{0}';".format(get_property_id_for_user(tn))
    to = tn
    body = "Phone Number,User Role"
    filename = "{0}{1}{2}".format(tn, ".list.", int(time.time()))
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = "{0}{1}".format(body, "\n{0},{1}".format(row[0], row[1]))
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 3)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_list_all(tn, command):
    """Ex: access list all"""
    config = load_config()
    sql = "SELECT DISTINCT u.phone_number, ur.role_name, p.house_number FROM users u, user_roles ur, property p WHERE p.id = u.property_id AND u.user_role_id = ur.id;"
    to = tn
    body = "Phone Number,User Role,House Number"
    filename = "{0}{1}{2}".format(tn, ".list_all.", int(time.time()))
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = "{0}{1}".format(body, "\n{0},{1},{2}".format(row[0], row[1], row[2]))
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 3)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_history(tn, command):
    """Ex: history"""
    config = load_config()
    sql = "SELECT DISTINCT u2.phone_number, event_time, gate_msg_tn, gate_msg_text, a.action_name FROM actions a, users u, users u2, history h WHERE a.id = h.action_id AND u.property_id = h.property_id AND u2.id = h.user_id AND u.property_id = '{0}' ORDER BY event_time;".format(get_property_id_for_user(tn))
    to = tn
    body = "Phone Number,Event Time,Gate Msg TN,Gate Msg Text,Action Performed"
    filename = "{0}{1}{2}".format(tn, ".history.", int(time.time()))
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = "{0}{1}".format(body, "\n{0},{1},{2},{3},{4}".format(row[0], row[1], row[2], row[3], row[4]))
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 4)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def access_history_all(tn, command):
    """Ex: history all"""
    config = load_config()
    sql = "SELECT DISTINCT u2.phone_number, event_time, gate_msg_tn, gate_msg_text, a.action_name, p.house_number FROM actions a, users u, users u2, history h, property p WHERE h.property_id = p.id AND a.id = h.action_id AND u.property_id = h.property_id AND u2.id = h.user_id ORDER BY event_time;"
    to = tn
    body = "Phone Number,Event Time,Gate Msg TN,Gate Msg Text,Action Performed,House Number"
    filename = "{0}{1}{2}".format(tn, ".history_all.", int(time.time()))
    try :
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    body = "{0}{1}".format(body, "\n{0},{1},{2},{3},{4},{5}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
        write_text_msg(filename, to, body)
        add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 4)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def add_access(tn, command):
    """Ex: add 4048675309 resident 3021"""
    command_parts = command.split()
    property_id = None
    new_user_role_id = None
    if len(command_parts) == 4:
        property_id = get_id_for_property(command_parts[3])
    elif len(command_parts) == 3:
        property_id = get_property_id_for_user(tn)
    elif len(command_parts) == 2:
        property_id = get_property_id_for_user(tn)
        new_user_role_id = get_role_id_for_name("RESIDENT".lower())
    else:
        return
    user_role_id = get_role_id_for_tn(tn)
    new_user_role_id = get_role_id_for_name(command_parts[2].lower())
    if not user_exists(command_parts[1]):
        if user_role_id >= new_user_role_id and new_user_role_id > 1:
            config = load_config()
            sql = "INSERT INTO users (phone_number, user_role_id, property_id) VALUES ('{0}', '{1}', '{2}');".format(command_parts[1], new_user_role_id, property_id)
            to = tn
            body = None
            filename = "{0}{1}{2}".format(tn, ".add_access.", int(time.time()))
            try :
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sql)
                        body = "{0} added as {1} to house number {2}".format(command_parts[1], get_role_name_for_id(new_user_role_id), get_house_number_for_property_id(property_id))
                write_text_msg(filename, to, body)
                add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 5)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

def remove_access(tn, command):
    """remove 4048675309 3021"""
    command_parts = command.split()
    property_id = None
    if len(command_parts) == 3:
        property_id = get_id_for_property(command_parts[2])
    elif len(command_parts) == 2:
        property_id = get_property_id_for_user(tn)
    else:
        return
    user_role_id = get_role_id_for_tn(tn)
    if user_role_id >= 2 and user_exists(command_parts[1]) and get_property_id_for_user(command_parts[1]) == property_id:
        config = load_config()
        sql = "DELETE FROM users WHERE id = '{0}';".format(get_id_for_user(command_parts[1]))
        to = tn
        body = None
        filename = "{0}{1}{2}".format(tn, ".remove_access.", int(time.time()))
        try :
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    body = "{0} removed from house number {1}".format(command_parts[1], get_house_number_for_property_id(property_id))
            write_text_msg(filename, to, body)
            add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 6)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def ban_access(tn, command):
    """ban 4048675309"""
    command_parts = command.split()
    if len(command_parts) != 2:
        return
    user_role_id = get_role_id_for_tn(tn)
    if user_role_id > 3 and not user_exists(command_parts[1]):
        config = load_config()
        sql = "INSERT INTO users (phone_number, user_role_id, property_id) VALUES ('{0}', 1, 1);".format(command_parts[1])
        to = tn
        body = None
        filename = "{0}{1}{2}".format(tn, ".banned.", int(time.time()))
        try :
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    body = "{0} banned from gate access".format(command_parts[1])
            write_text_msg(filename, to, body)
            add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 7)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    elif user_role_id > 3:
        config = load_config()
        sql = "UPDATE users SET user_role_id = 1, property_id = 1 WHERE phone_number = '{0}';".format(command_parts[1])
        to = tn
        body = None
        filename = "{0}{1}{2}".format(tn, ".banned.", int(time.time()))
        try :
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    body = "{0} banned from gate access".format(command_parts[1])
            write_text_msg(filename, to, body)
            add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 7)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def guest(tn, command):
    """Ex: 3021 This is George, please open the gate"""
    invalid_msg = "The message sent was invalid.  Acceptable messages begin with the house number of the property for which you are visiting, followed by a brief message to that property's owner(s)"
    house_number = None
    for mo in re.finditer(r'\d+(\d*)?', command):
        house_number = mo.group()
    if house_number:
        property_id = get_id_for_property(house_number)
        if property_id:
            home_owner_msg = re.sub(r'^.*?\s', "", command)
            filename = "{0}{1}{2}".format(tn, ".guest.", int(time.time()))
            for owner in get_owners_for_property(house_number):
                sent_from = " (sent from {0})".format(tn)
                write_text_msg(filename, owner[0], "{0}{1}".format(home_owner_msg, sent_from))
                add_history(get_id_for_user(owner[0]), property_id, tn, command, 8)
            add_inflight_operation(tn, property_id)
        else:
            filename = "{0}{1}{2}".format(tn, ".invalid_msg_response.", int(time.time()))
            write_text_msg(filename, tn, invalid_msg)
    else:
        filename = "{0}{1}{2}".format(tn, ".invalid_msg_response.", int(time.time()))
        write_text_msg(filename, tn, invalid_msg)


def help_response(tn, command, user_role_id):
    """Ex: help"""
    to = tn
    body = None
    filename = "{0}{1}{2}".format(tn, ".help.", int(time.time()))
    if user_role_id == 1: # Banned
        body = "This number is not allowed to access this system"
    elif user_role_id == 3: # Resident
        body = "The following options are available:\n\n- 'help' to see this message\n- 'open' to open the gate"
    elif user_role_id == 4: # Property owner
        body = "The following options are available:\n\n- 'help' to see this message\n- 'open' to open the gate\n- 'access list' to see the access configuration for your property\n- 'history' to see the usage history for your property\n- 'add <<tn>> <<role>>' adds a TN to access property (example: add 4048675309 resident)\n- 'remove <<tn>>' removes a TN from the system (example: remove 4048675309)"
    elif user_role_id == 5: # Admin
        body = "The following options are available:\n\n- 'help' to see this message\n- 'open' to open the gate\n- 'access list' to see the access configuration for your property\n- 'history' to see the usage history for your property\n- 'access list all' to see the access configuration for all properties\n- 'history all' to see the usage history for all properties\n- 'add <<tn>> <<role>> <<house number>>' adds a TN to access property (example: add 4048675309 resident 3012)\n- 'remove <<tn>>' removes a TN from the system (example: remove 4048675309)\n- 'ban <<tn>>' bans a TN from being able to interact with the system (example: ban 4048675309)"
    else:
        body = "Send a message like the provided example, be sure the house number for the property to which you are visiting is at the beginning of the message.\n\nExample:\n 3021 This is George, please open the gate"
    write_text_msg(filename, to, body)
    add_history(get_id_for_user(tn), get_property_id_for_user(tn), tn, command, 2)

#################################################
### Message handler #############################
#################################################
def handle_msg(tn, command, user_role_id):
    if user_role_id > 4: # ADMIN
        if command.lower() == "access list all":
            access_list_all(tn, command)
        if command.lower() == "access history all" or command.lower() == "history all":
            access_history_all(tn, command)
        if command.lower().startswith("ban"):
            ban_access(tn, command)
    if user_role_id > 3: # OWNER or higher
        if command.lower().startswith("add"):
            add_access(tn, command)
        if command.lower().startswith("remove"):
            remove_access(tn, command)
        if command.lower() == "access list":
            access_list(tn, command)
        if command.lower() == "access history" or command.lower() == "history":
            access_history(tn, command)
    if user_role_id > 2: # RESIDENT or higher
        if command.lower() == "open":
            open_gate(tn, command)
    if user_role_id > 1:
        if re.search(r'^[0-9]*?\s', command):
            guest(tn, command)
        if command.lower() == "help":
            help_response(tn, command, user_role_id)

#################################################
### Main ########################################
#################################################
if __name__ == '__main__':
    if sys.argv[1] == 'RECEIVED':
        msg = read_text_msg(sys.argv[2])
        handle_msg(msg[0], msg[1].strip(), get_role_id_for_tn(msg[0]))