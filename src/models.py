from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    favorites = db.Column(db.Integer())
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(50), nullable=True)
    #is_active = db.Column(db.Boolean(), unique=True, nullable=True)
    commentary = db.relationship('Commentary', lazy=True)
    observation = db.relationship('Observation', lazy=True)
    post = db.relationship('Post', lazy=True)
    collab_user = db.relationship('CollabUser', lazy=True)
     
    
    def __repr__(self):
        return '<User %r>' % self.first_name
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class CollabUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    og_user_id= db.Column(db.Integer(), db.ForeignKey(User.id))
    commentary = db.relationship('Commentary', lazy=True)
    observation = db.relationship('Observation', lazy=True)
    post = db.relationship('Post', lazy=True)
    collab = db.relationship('Collaboration', lazy=True)


    def __repr__(self):
        return '<Collabuser %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, its a security breach
        }



class Collaboration(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    mush_img =  db.Column(db.String(150))
    spore_img =  db.Column(db.String(150))
    description = db.Column(db.String(350))
    collab_user_id= db.Column(db.Integer(), db.ForeignKey(CollabUser.id))
    attribute = db.relationship('AttributeDescription', lazy=True)


    def __repr__(self):
        return '<Collaboration %r>' % self.description

    def serialize(self):
        return {
            "id": self.id,
            "mush_img": self.mush_img,
            "spore_img": self.spore_img,
            "description": self.description,
            # do not serialize the password, its a security breach
        }


class AttributeDescription(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    species = db.Column(db.String(50))
    location = db.Column(db.String(50))
    substrate = db.Column(db.String(50))
    gills = db.Column(db.String(50))
    pores = db.Column(db.String(50))
    pileus_diameter = db.Column(db.Integer())
    shape = db.Column(db.String(50))
    pileus_color = db.Column(db.String(50))
    margin = db.Column(db.Integer())
    height = db.Column(db.Integer())
    foot_color = db.Column(db.String(50))
    ring = db.Column(db.Boolean())
    foot_diameter = db.Column(db.Integer())
    volva = db.Column(db.Boolean())
    collaboration_id = db.Column(db.Integer(), db.ForeignKey(Collaboration.id))
    

    def __repr__(self):
        return '<AttributeDescription %r>' % self.species

    def serialize(self):
        return {
            "id": self.id,
            "location": self.location,
            "substrate": self.substrate,
            "gills": self.gills,
            "pores": self.pores,
            "pileus_diameter": self.pileus_diameter,
            "shape": self.shape,
            "pileus_color": self.pileus_color,
            "margin": self.margin,
            "height": self.height,
            "foot_color": self.foot_color,
            "ring": self.ring,
            "foot_diameter": self.foot_diameter,
            "volva": self.volva,
            # do not serialize the password, its a security breach
        }

class Observation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(150))
    img_url =  db.Column(db.String(150))
    collab_user_id = db.Column(db.Integer(), db.ForeignKey(CollabUser.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    mushrooms = db.relationship('Mushrooms', lazy=True)
    

    def __repr__(self):
        return '<Observation %r>' % self.Title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.Title,
            "body": self.body,
            "img_url": self.img_url,
            # do not serialize the password, its a security breach
        }


class Mushrooms(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    local_name = db.Column(db.String(150))
    scientific_name = db.Column(db.String(150))
    edible = db.Column(db.String(150))
    hallucinogen = db.Column(db.String(50))
    location = db.Column(db.String(80))
    data_description = db.Column(db.String(300))
    recipe = db.Column(db.String(300))
    viewers = db.Column(db.Integer())
    observation_id = db.Column(db.Integer(), db.ForeignKey(Observation.id))


    def __repr__(self):
        return '<Mushrooms %r>' % self.scientific_name

    def serialize(self):
        return {
            "id": self.id,
            "scientific_name": self.scientific_name,
            "location": self.location,
            # do not serialize the password, its a security breach
        }



class Commentary(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    likes = db.Column(db.Integer())
    pub_date = db.Column(db.Date())
    viewers = db.Column(db.Integer())
    body = db.Column(db.String(150))
    collab_user_id = db.Column(db.Integer(), db.ForeignKey(CollabUser.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    mushroom_id = db.Column(db.Integer(), db.ForeignKey(Mushrooms.id))
    

    def __repr__(self):
        return '<Commentary %r>' % self.Title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.Title,
            # do not serialize the password, its a security breach
        }



class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(150))
    pub_date = db.Column(db.Date())
    collab_user_id = db.Column(db.Integer(), db.ForeignKey(CollabUser.id))
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    

    def __repr__(self):
        return '<Post %r>' % self.Title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.Title,
            # do not serialize the password, its a security breach
        }

