#!/usr/bin/env python3
import random
from random import randint, choice as rc



from app import app
from app import db, Hero,Power,HeroPower



with app.app_context():


    Hero.query.delete()
    hero_list=[
        { 'name': "Kamala Khan", 'super_name': "Ms. Marvel" },
        { 'name': "Doreen Green", 'super_name': "Squirrel Girl" },
        { 'name': "Gwen Stacy", 'super_name': "Spider-Gwen" },
        { 'name': "Janet Van Dyne", 'super_name': "The Wasp" },
        { 'name': "Wanda Maximoff", 'super_name': "Scarlet Witch" },
        { 'name': "Carol Danvers", 'super_name': "Captain Marvel" },
        { 'name': "Jean Grey", 'super_name': "Dark Phoenix" },
        { 'name': "Ororo Munroe", 'super_name': "Storm" },
        { 'name': "Kitty Pryde", 'super_name': "Shadowcat" },
        { 'name': "Elektra Natchios", 'super_name': "Elektra" }
    ]
    for hero in (hero_list):
        hero = Hero(
            name = hero['name'],
            super_name =  hero['super_name']
        )
        db.session.add(hero)
        db.session.commit()




    Power.query.delete()
    power_list=[
  { 'name': "super strength", 'description': "gives the wielder super-human strengths" },
  { 'name': "flight", 'description': "gives the wielder the ability to fly through the skies at supersonic speed" },
  { 'name': "super human senses", 'description': "allows the wielder to use her senses at a super-human level" },
  { 'name': "elasticity", 'description': "can stretch the human body to extreme lengths" }
]
    
    for power in (power_list):
        power = Power(
            name = power['name'],
            description =  power['description']
        )
        db.session.add(power)
        db.session.commit()



    HeroPower.query.delete()

    hero_power_list = []
    strength_list =['Strong', 'Weak', 'Average']
    for i in range(30):
        hero_power=HeroPower(
            strength = rc(strength_list),
            hero_id=rc([heroe.id for heroe in Hero.query.all()]),
            power_id=rc([power.id for power in Power.query.all()])
        )
        db.session.add(hero_power)
        db.session.commit()







    hero1=(Hero.query.all()[0])
    power1=(Power.query.all()[0])
    hr=(Hero.query.all())
    # print(hero1.powers)
    # print(power1.heroes)