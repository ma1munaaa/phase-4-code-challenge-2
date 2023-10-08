#!/usr/bin/env python3
from flask import Flask, jsonify,request,make_response,abort
from flask_restx import Api,Resource,Namespace,fields,abort
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.exc import NoResultFound
# from flask_cors import CORS

from models import db, Hero,Power,HeroPower


app = Flask(__name__)
# CORS(app)
# CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] =True
migrate = Migrate(app, db)

db.init_app(app)

# Instantiate Marshmallow
ma = Marshmallow(app)
'''---------------API_initialization---------------'''
api = Api()
api.init_app(app)
Hero_api=Namespace('Hero_Api')
Power_api=Namespace('Power_Api')
Hero_Power_api=Namespace('Hero_Power_api')
api.add_namespace(Hero_api)
api.add_namespace(Power_api)
api.add_namespace(Hero_Power_api)





# '''------------------------ROURCE MODELS----------------------'''

powers_model = api.model('Powers',{
    'id':fields.Integer    ,
    'name':fields.String,
    'description':fields.String,

})  

heroes_model = api.model('Heroes',{
    'id':fields.Integer    ,
    'name':fields.String,
    'super_name':fields.String,
    'powers':fields.List(fields.Nested(powers_model))

})

  

power_model = api.model('Power_by_id',{
    'id':fields.Integer    ,
    'name':fields.String,
    'description':fields.String,
    # 'heroes':fields.List(fields.Nested(heroes_model))


})  

hero_model = api.model('Hero_by_id',{
    'id':fields.Integer,
    'name':fields.String,
    'super_name':fields.String,
    # 'powers':fields.List(fields.Nested(powers_model))

})

hero_post= api.model('post_hero',{
    'name':fields.String,
    'super_name':fields.String

})

hero_update = api.model('update_hero',{
    'super_name':fields.String
})


power_post = api.model('POST_power',{
    'name':fields.String,
    'description':fields.String
})

power_update = api.model('update_power',{
    'name':fields.String,
    'description':fields.String

})

hero_power_model = api.model('hero_power',{
    'id':fields.Integer,
    'strength':fields.String,
    'hero_id':fields.Integer,
    'power_id':fields.Integer,
    # 'hero':fields.List(fields.Nested(heroes_model))

})
hero_power_post=api.model('post_hero_power',{
    'strength':fields.String,
    'hero_id':fields.Integer,
    'power_id':fields.Integer,
})
hero_power_update = api.model('update_hero_power',{
    'strength':fields.String
})


'''--------------- M A R S H A M A L L O W  -----------------------------'''

class PowerSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = Power
        ordered = True
        exclude = ('created_at', 'updated_at')
    
    id= ma.auto_field()
    name= ma.auto_field()
    description= ma.auto_field()
    # heroes = ma.List(ma.Nested(lambda: HeroSchema(only=('id','name','super_name'))))
    heroes = ma.List(ma.Nested('HeroSchema',only=('id','name','super_name')))
power_schema = PowerSchema()
powers_schema = PowerSchema(exclude=['heroes'],many =True)


class HeroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hero
        ordered = True
        exclude = ('created_at', 'updated_at')
        
    id = ma.auto_field()
    name = ma.auto_field()
    super_name = ma.auto_field()
    powers = ma.List(ma.Nested('PowerSchema',only=('id','name','description',)))


heroe_schema = HeroSchema()
heroes_schema = HeroSchema(exclude=['powers'],many=True)


class HeroPowerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model= HeroPower
        ordered = True
        exclude = ('created_at', 'updated_at')
        
    id = ma.auto_field()
    hero_id = ma.auto_field()
    power_id = ma.auto_field()

hero_power_schema = HeroPowerSchema()
heros_powers_schema = HeroPowerSchema(exclude =['created_at','updated_at'],many=True)

'''------------------RESOURCE ROUTES-------------------------'''

@Hero_api.route('/heroes')
class Heroes(Resource):

    def get(self):      
        heroes = Hero.query.all()
        if heroes:
            return make_response(heroes_schema.dump(heroes),200)
        else:

            response =  make_response(
                {'message':'no heros in the area'}
                ,404)
            return response
     
    @Hero_api.expect(hero_post)
    def post(self):
        heroes = Hero.query.all()
        #data is in the payload
        hero = Hero(
            name= Hero_api.payload['name'],
            super_name= Hero_api.payload['super_name'],
        )
       
        if hero.super_name not in  [ h.super_name for h in heroes]:
            db.session.add(hero)
            db.session.commit()

            return make_response(heroe_schema.dump(hero),201)
        else:
            response = make_response(
                {'error':'validation error',
                 'message':'hero  super_name already exists'}
                ,404
            )

            return response




@Hero_api.route('/hero/<int:id>')
class Hero_by_id(Resource):

    def get(self,id):  
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            return make_response(heroe_schema.dump(hero))
        else:
            response = make_response(
                {'error':'Hero not found, please choose another one'}
                ,404
            )

            return response
            
      

    
    '''----------------------Hero D E L E T I O N --------------------'''
    def delete(self,id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            db.session.delete(hero)
            db.session.commit()
            return  make_response(
                {
                    'deleted':True,
                 'message':"hero deleted successfully"
                 } ,200)
        

        return {'ERROR!': 'hero you are trying to delete does not exist'}

    '''U P D A T E ----- H E R O--------------------'''
    @Hero_api.expect(hero_update)
    @Hero_api.marshal_with(hero_model)
    def put(self,id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero.super_name =Hero_api.payload['super_name']
            db.session.commit()
            return hero, 200
       
        else:
            return make_response(
                    {'error':'hero you are updating  does not exist '}
                    ,400)
            



        


@Power_api.route('/powers')
class POWERS(Resource):

    def get(self):      
        powers = Power.query.all()
        if powers:
            return make_response(powers_schema.dump(powers),200)
        else:

            response =  make_response(
                {'message':'no powers in the available'}
                ,404)
            return response
     
    @Hero_api.expect(power_post)
    def post(self):
     
        #data is in the payload
        power = Power(
            name= Hero_api.payload['name'],
            description= Hero_api.payload['description'],
        )
       
        if power.name not in  [ h.name for h in Power.query.all()]:
            if len(power.description)>=20:
                db.session.add(power)
                db.session.commit()

                return make_response(power_schema.dump(power),201)
            else:
                return make_response({'error':'validation error',
                                      'message':'description  must be present and at least 20 characters long'})
        else:
            response = make_response(
                {'error':'validation error',
                 'message':'power  name already exists'}
                ,404
            )

            return response



@Power_api.route('/power/<int:id>')
class Power_by_id(Resource):

    def get(self,id):   
        power = Power.query.filter_by(id=id).first()

        if power:
            return make_response(power_schema.dump(power))
        else:
            return make_response({'error':'power not found in the database'},404)

      
     
    '''----------------------Hero D E L E T I O N --------------------'''
    def delete(self,id):
        power = Power.query.filter_by(id=id).first()
        if power:
            db.session.delete(power)
            db.session.commit()
            return  make_response(
                {
                    'deleted':True,
                 'message':"power deleted successfully"
                 } ,200)
        

        return {'ERROR!': 'power you are trying to delete does not exist'}
    


    '''-----------------U P D A T I N G --------------------'''
    @Power_api.expect(power_update)
    @Power_api.marshal_with(power_model)
    def put(self,id):
        power = Power.query.filter_by(id=id).first()
        if power:
            # updatet the super_name
            power.name =Power_api.payload['name']
            power.description =Power_api.payload['description']
            #check if the super_name exists
            db.session.commit()
            return power ,200
         
        else:
            return make_response(
                    {'error':'power you are updating  does not exist '}
                    ,400)
            


    
@Hero_Power_api.route('/hero_powers')
class HeroPowers(Resource):
    def get(self):
        hero_power = HeroPower.query.all()
        if  hero_power:
            return heros_powers_schema.dump( hero_power), 200
        return make_response({'notFound':'No powers in the database'},200)
    
    @Hero_Power_api.expect(hero_power_post)
    # @Hero_Power_api.marshal_with(heroes_model)
    def post(self):

        hero_power = HeroPower(
            strength=Hero_Power_api.payload['strength'],
            hero_id=Hero_Power_api.payload['hero_id'],
            power_id=Hero_Power_api.payload['power_id'],
        )

        db.session.add(hero_power)
        db.session.commit()

        #use the hero id to get the hero
        hero = Hero.query.filter_by(id = hero_power.hero_id).first()
        return make_response(heroe_schema.dump(hero),200)

    






@Hero_Power_api.route('/heroPower/<int:id>')
class HeroPower_by_id(Resource):

    def get(self,id):   
        hero_power = HeroPower.query.filter_by(id=id).first()

        if hero_power:
            return make_response(hero_power_schema.dump(hero_power),200)
        else:
            return make_response({'error':'power not found in the database'},404)

      
     
    '''----------------------Hero D E L E T I O N --------------------'''
    def delete(self,id):
        hero_power = HeroPower.query.filter_by(id=id).first()
        if hero_power:
            db.session.delete(hero_power)
            db.session.commit()
            return  make_response(
                {
                    'deleted':True,
                 'message':"hero_power deleted successfully"
                 } ,200)
        

        return {'ERROR!': 'hero_power you are trying to delete does not exist'}
    


    '''-----------------U P D A T I N G --------------------'''

    @Hero_Power_api.expect(hero_power_update)
    @Hero_Power_api.marshal_with(hero_power_model)
    def put(self,id):
        hero_power = HeroPower.query.filter_by(id=id).first()
        if hero_power:
            for attr in Hero_Power_api.payload:
                setattr(hero_power, attr, Hero_Power_api.payload[attr])
            # hero_power.strength = Hero_Power_api.payload['strength']
            db.session.add(hero_power)
            db.session.commit()
            return hero_power ,200
         
        else:
            return make_response(
                    {'error':'hero_power you are updating  does not exist '}
                    ,400)
            




if __name__ == '__main__':
    app.run(port=5555, debug=True)
