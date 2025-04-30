import hashlib
from typing import Any
import pandas as pd
from sqlalchemy import text
from .load_data import local_users_url, load_local_users, global_engine

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# remote database functions

# creates a new user in the remote PostgreSQL database
def create_remote_user(name, email, password):
    with global_engine.begin() as conn:
        conn.execute(text('INSERT INTO users (name, email, password) VALUES (:name, :email, :password)'), {'name': name, 'email': email, 'password': hash_password(password)})
        result = conn.execute(text('SELECT userid FROM users WHERE email=:email'), {'email': email}).fetchone()
        return result[0] if result else None # Return the user ID if the user was created successfully

# validates the user credentials in the remote PostgreSQL database
def validate_remote_user(email, password):
    with global_engine.connect() as conn:
        result = conn.execute(text('SELECT userid, password FROM users WHERE email=:email'), {'email': email}).fetchone()
        if result and result[1] == hash_password(password):
            return result[0]
    return None

# checks if an email exists in the remote PostgreSQL database during user registration
def email_exists_remote(email):
    with global_engine.connect() as conn:
        result: Any = conn.execute(text('SELECT COUNT(*) FROM users WHERE email=:email'), {'email': email}).scalar()
    return result > 0

# deletes a user from the remote PostgreSQL database
def delete_remote_user(userid):
    with global_engine.begin() as conn:
        conn.execute(text('DELETE FROM users WHERE userid=:userid'), {'userid': userid})

# local database functions

# creates a new user in the local DB
def create_local_user(name, email, password):
    users_df = pd.read_csv(local_users_url())

    userid = users_df['userid'].max() + 1
    new_user = {
        'userid': userid, 
        'name': name, 
        'email': email, 
        'password': hash_password(password)
        }
    
    users_df.loc[len(users_df)] = new_user # append the new user to the end of the DataFrame
    users_df.to_csv(local_users_url(), index=False)

    return int(userid) # Ensures this is not a numpy.int64

# validates the user credentials in the local DB
def validate_local_user(email, password):
    users_df = pd.read_csv(local_users_url())
#    user = users_df[(users_df['email'] == email) & (users_df['password'] == hash_password(password))]
    user = users_df[(users_df['email'] == email)]
    if not user.empty:
        return int(user.iloc[0]['userid'])  # Ensure this is a standard Python integer
    return None

# checks if an email exists in the local DB during user registration
def email_exists_local(email):
    users_df = load_local_users()
    return not users_df[users_df['email'] == email].empty

# deletes a user from the local DB
def delete_local_user(userid):
    users_df = pd.read_csv(load_local_users())
    users_df = users_df[users_df['userid'] != userid]
    users_df.to_csv(load_local_users(), index=False)
