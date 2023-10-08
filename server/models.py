from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData



metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    # serialize_rules = ('-rest_pizza_association.restaurants','pizzas',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    

    # relationship
    hero_power_association = db.relationship('HeroPower', back_populates='hero',cascade='all, delete-orphan')
    powers = association_proxy('hero_power_association','power')




    # ---------------------------------------validations
    # @validates('super_name')
    # def name_validation(self, key, super_name):
    #     if super_name in [h.super_name for h in Hero.query.all()]:
    #         raise ValueError('super_name already exists in the database')
    #     return super_name
    


    def __repr__(self):
        return f'(id: {self.id}, name: {self.name}. super_name: {self.super_name} )'


class HeroPower(db.Model):
    __tablename__='heropowers'

    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    hero_id = db.Column('hero_id',db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column('power_id',db.Integer, db.ForeignKey("powers.id"))

    hero = db.relationship('Hero', back_populates='hero_power_association')
    power = db.relationship('Power', back_populates='hero_power_association')


 

    # # ------------------------------------------validations
    @validates('strength')
    def price_validation(self, key, strength):
        if strength not  in ['Average','Weak','Strong']:
            raise ValueError(' strength must be one of the following : Strong, Weak or Average')
        return strength
    
    
    
    


    

    def __repr__(self):
        return f'(id: {self.id}, strength: {self.strength}, hero_id:{self.hero_id}, power_id:{self.power_id})'



class Power(db.Model):
    __tablename__ = 'powers'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # # relationship
    hero_power_association = db.relationship('HeroPower', back_populates='power')
    heroes = association_proxy('hero_power_association','hero')


    

  # ------------------------------------------validations
    @validates('description')
    def price_validation(self, key, description):
        if len(description) < 20:
            raise ValueError('description  must be present and at least 20 characters long')
        return description
    
    
 

    def __repr__(self):
        return f'(id: {self.id}, name: {self.name}, description: {self.description}, created_at: {self.created_at})'


