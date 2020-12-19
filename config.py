class Conf(object):
    @staticmethod
    def get_sql_conf(conf='local'):
        if conf=='ecs':
            return 'postgresql://postgres:11111111qQ@47.101.151.73:5432/bookstore'
        elif conf=='local':
            return 'postgresql://postgres:1@localhost:5432/bookstore'
        elif conf=='local_w':
            return 'postgresql://postgres:amyamy@localhost:5433/bookstore'
        elif conf=='local_y':
            return 'postgresql://postgres:990814@[2001:da8:8005:4056:81e9:7f6c:6d05:fe47]:5432/bookstore'


