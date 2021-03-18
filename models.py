from mics import dp
import config
import datetime
import asyncio
import asyncpg
async def create_pool():       
    return await asyncpg.create_pool(
                user= config.POSTGRES_USER,
                password = config.POSTGRES_PASSWORD,
                database = config.POSTGRES_BASE_NAME,
                host = config.POSTGRES_ADRESS
                )
                
db = dp.loop.run_until_complete(create_pool())

class Database:
    pool = db
    
    
    async def create_item_table(self):
        sql = '''create table if not exists items(
            item_name varchar(50),
            category varchar(50),
            photo_id text ,
            description text,
            cost int)
            '''
        async with self.pool.acquire() as connect:
            await connect.execute(sql)
            
    async def create_users_table(self):
        sql = '''create table if not exists users(
            user_id int,
            name varchar(100),
            balance numeric(10, 2) default 0,
            cashback numeric(10, 2) default 0,
            sex varchar(50),
            age varchar(50),
            refid int,
            referals int,
            colors text array)
            '''
        async with self.pool.acquire() as connect:
            await connect.execute(sql)
            
    async def create_table_backet(self):
        sql = '''create table if not exists bascket(
            user_id int,
            item_name varchar,
            cost int,
            photo_id text,
            qty int default 1)
            '''
        async with self.pool.acquire() as connect:        
           item_product = await connect.execute(sql)  
           
    async def get_bascket_item_by_name_for_user(self, id , item_name):
        sql = 'select * from bascket where user_id = $1 and item_name = $2'
        async with self.pool.acquire() as connect:
           item_product = await connect.fetchrow(sql, *(id, item_name))      
           return item_product
           
    async def update_bascket_item_qty(self, user_id, item_name, qty):
        sql = 'update bascket set qty = qty + $1 where user_id = $2 and item_name = $3'
        async with self.pool.acquire() as connect:                
           item_product = await connect.execute(sql, *(qty, user_id , item_name))      
      
           
    async def add_item_to_backet(self,id, item_name, cost, photo):
        sql = 'insert into bascket values($1 ,$2, $3, $4)'
        async with self.pool.acquire() as connect:        
           item_product = await connect.execute(sql, *(id, item_name, cost, photo))      
           return item_product        
           
    async def get_all_user_id(self):
        sql = 'select user_id from users'
        async with self.pool.acquire() as connect:        
           users = await connect.fetch(sql) 
           return users
    async def get_item_in_backet_by_user_id(self , id, pos=1):
        sql = 'select * from bascket where user_id = $1'
        async with self.pool.acquire() as connect:        
           item_products = await connect.fetch(sql, id) 
           if item_products:
              return item_products[pos-1]
           return None

    async def get_all_item_in_backet_by_user_id(self , id, pos=1):
        sql = 'select * from bascket where user_id = $1'
        async with self.pool.acquire() as connect:        
           item_products = await connect.fetch(sql, id) 
           return item_products
         
            
    async def get_last_position_bascket(self , id):
        sql = 'select * from bascket where user_id = $1'
        async with self.pool.acquire() as connect:        
           item_products = await connect.fetch(sql, id) 
           last_pos = len(item_products)
           return last_pos
                     
           
           
    async def get_sum_cost_bascket(self, id):
        sql = 'select sum(cost * qty) from bascket where user_id = $1'
        async with self.pool.acquire() as connect:        
           order_cost = await connect.fetchval(sql, id) 
           return order_cost    
           
           
           
           
           
           
           
           
           
    async def create_item(self, item_name, category,  description,cost,photo_id = True ):
         sql = 'insert into items values ($1,$2,$3,$4, $5)'
         async with self.pool.acquire() as connect:
            await connect.execute(sql, *(item_name,category, photo_id, description, int(cost))) 
            
            
    async def get_item_by_category(self, category_name, pos):
        sql = 'select * from items where category = $1'
        async with self.pool.acquire() as connect:
            items = await connect.fetch(sql, category_name)
            return items[pos-1]
            
    async def get_cost_by_item_name(self,item_name):        
        sql = 'select cost from items where item_name =$1'
        async with self.pool.acquire() as connect:
            cost = await connect.fetchval(sql, item_name)
            return cost

    async def get_photo_by_item_name(self,item_name):        
        sql = 'select photo_id from items where item_name =$1'
        async with self.pool.acquire() as connect:
            photo = await connect.fetchval(sql, item_name)
            return photo

    async def delete_item_from_bascket(self, id, item_name):
       sql = 'delete from bascket where user_id = $1 and item_name = $2'
       async with self.pool.acquire() as connect:
           await connect.execute(sql, *(id, item_name))    
           
    async def delete_table(self):            
        sql = 'drop table bascket'
        async with self.pool.acquire() as connect:
            await connect.execute(sql)       
            
   
    async def authentication(self, id, name, refid = None):
        if await self.get_info(id):
            return True
        else:
            await self.registration( id , name)
    
    
    async def registration(self, id, name, refid = None):
        
        if refid :
            sql = 'insert into users(user_id, refid, name ) values($1, $2, $3)'
            await self.update_referals(int(refid))
            args = (id, refid,name)
        else:    
            sql = 'insert into users(user_id, refid,name) values($1, $2,$3)'
            args = (id, refid, name)
        async with self.pool.acquire() as connect:
           await connect.execute(sql , *args) 


    async def get_info(self, id):
        sql = 'select * from users where user_id = $1'
        async with self.pool.acquire() as connect:
            select = await connect.fetchrow(sql ,id)
            return select

    async def update_user_sex(self, id , sex):
        sql = 'update users set sex = $1'
        async with self.pool.acquire() as connect:
           await connect.execute(sql , sex)
           
    async def update_user_age(self, id , age):
        sql = 'update users set age = $1'
        async with self.pool.acquire() as connect:
           await connect.execute(sql , age) 
           
    async def update_user_favorite_colors(self, id , colors):
        sql = 'update users set colors = $1'
        async with self.pool.acquire() as connect:
           await connect.execute(sql , colors) 
           
    async def get_user_favorite_colors(self, id):
        sql = 'select colors from users where user_id = $1'
        async with self.pool.acquire() as connect:
           colors = await connect.fetchval(sql, id)    
           if colors:
               return colors

           return []
           
     