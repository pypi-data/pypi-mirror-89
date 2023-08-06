

############################################### IMPORTANT ###############################################
#                          ANY CHANGE TO THIS FILE REQUIRES TESTING THE TARGET WEBSITES USING IT
#########################################################################################################



from python.TQapis_package.TQapis.TQConnection import Connection, Message
import python.TQapis_package.TQapis.TQRequests as TQRequests


def make_results(message, connection):
    if not message.is_OK:
        return [message.is_OK, connection.response.errors]
    else:
        return [message.is_OK, connection.response.results]


def connection_is_ok(connection):
    #
    # Check if we have connections
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_ip_return = TQRequests.request_ip_return()
    message = connection.send(request_ip_return)
    return make_results(message, connection)


def account_status(connection, user_email):
    #
    # check the status of the account
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_create = TQRequests.request_account_status(user_email)
    message = connection.send(request_account_create)
    return make_results(message, connection)


def account_create(connection, user_email, user_password, user_ip, callback_url, is_test):
    #
    # Creates a  account
    #
    #is_post = True  # True = use POST method, False = use GET method
    # connection = Connection(host_email, is_post, target_url)
    request_account_create = TQRequests.request_account_create(user_email, user_password, user_ip, callback_url,
                                                               is_test)
    message = connection.send(request_account_create)
    return make_results(message, connection)


def account_activation_key_status(connection, activation_key):
    #
    # Activates a  (disabled) account
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_activation_key_status = TQRequests.request_account_activation_key_status(activation_key)
    message = connection.send(request_account_activation_key_status)


    return make_results(message, connection)


def account_activate(connection,  activation_key, is_test):
    #
    # Activates a  (disabled) account
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_activate = TQRequests.request_account_activate(activation_key, is_test)
    message = connection.send(request_account_activate)
    return make_results(message, connection)


def account_send_activation_key(connection, user_email, callback_url, is_test):
    #
    # sends (resends) activation key
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_send_activation_key = TQRequests.request_account_send_activation_key(user_email, callback_url,
                                                                                         is_test)
    message = connection.send(request_account_send_activation_key)
    return make_results(message, connection)



def account_password_change(connection,user_email, password, _password, is_test):
    #
    # Changes the existing password
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_password_change = TQRequests.request_account_password_change(user_email, password, _password,
                                                                                 is_test)
    message = connection.send(request_account_password_change)
    return make_results(message, connection)


def account_ip_change(connection,user_email, password, _ip, is_test):
    #
    # Changes the registered IP
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_ip_change = TQRequests.request_account_ip_change(user_email, password, _ip, is_test)
    message = connection.send(request_account_ip_change)
    return make_results(message, connection)


def account_password_reset(connection,  activation_key, _password, is_test):
    #
    # Changes/resets the password 
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_password_reset_dict = TQRequests.request_account_password_reset(activation_key,
                                                                                    _password,
                                                                                    is_test)
    message = connection.send(request_account_password_reset_dict)
    return make_results(message, connection)


def account_password_ip_change(connection, user_email, password, new_password, new_ip, is_test):
    #
    # Changes password and IP at the same time
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_password_ip_change = TQRequests.request_account_password_ip_change(user_email, password,
                                                                                       new_password, new_ip,is_test)
    message = connection.send(request_account_password_ip_change)
    return make_results(message, connection)


def account_profile(connection, user_email, password):
    #
    # Changes/resets the password
    #
    #is_post = True  # True = use POST method, False = use GET method
    #connection = Connection(host_email, is_post, target_url)
    request_account_profile_dict = TQRequests.request_account_profile(user_email, password)
    message = connection.send(request_account_profile_dict)
    return make_results(message, connection)
