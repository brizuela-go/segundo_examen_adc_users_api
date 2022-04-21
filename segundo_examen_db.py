import datetime
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dataclasses import dataclass

app = Flask(__name__)
# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)


@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    primer_apellido = db.Column(db.String(255))
    segundo_apellido = db.Column(db.String(255))
    email = db.Column(db.String(255))
    usuario = db.Column(db.String(255))
    ultimo_acceso = db.Column(db.String(255))
    departamento = db.Column(db.String(255))
    turno = db.Column(db.String(255))
    RFFID = db.Column(db.Integer)
    personal_externo = db.Column(db.Boolean)
    RRHH = db.Column(db.Boolean)
    profile_picture = db.Column(db.String(255))

    def __init__(
        self,
        name,
        primer_apellido,
        segundo_apellido,
        email,
        usuario,
        ultimo_acceso,
        departamento,
        turno,
        RFFID,
        personal_externo,
        RRHH,
        profile_picture,
    ):
        self.name = name
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.email = email
        self.usuario = usuario
        self.ultimo_acceso = ultimo_acceso
        self.departamento = departamento
        self.turno = turno
        self.RFFID = RFFID
        self.personal_externo = personal_externo
        self.RRHH = RRHH
        self.profile_picture = profile_picture

    def __repr__(self):
        return "User %i: %s %s %s" % (
            self.id,
            self.name,
            self.primer_apellido,
            self.segundo_apellido,
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()

usuarios = [
    {
        "id": 1,
        "name": "Juan Eduardo",
        "primer_apellido": "Brizuela",
        "segundo_apellido": "González",
        "email": "jebg@gmail.com",
        "usuario": "juan_brizuela",
        "ultimo_acceso": datetime.datetime.now(),
        "departamento": "IT",
        "turno": "normal",
        "RFFID": 3456456,
        "personal_externo": True,
        "RRHH": False,
        "profile_picture": "https://st.depositphotos.com/2931363/3703/i/950/depositphotos_37034497-stock-photo-young-black-man-smiling-at.jpg",
    }
]


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "primer_apellido",
            "segundo_apellido",
            "email",
            "usuario",
            "ultimo_acceso",
            "departamento",
            "turno",
            "RFFID",
            "personal_externo",
            "RRHH",
            "profile_picture",
        )


user_schema = UserSchema()
user_schema = UserSchema(many=True)


@app.route("/")
def hello_world():
    return "Hello, World!"


uri = "/api/users/"

all_users = User.query.all()
print(all_users)


@app.route(uri, methods=["GET"])
def get_users():
    return jsonify({"users": all_users})


@app.route(uri + "<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"user": User.as_dict(user)})


@app.route(uri, methods=["POST"])
def create_user():
    if not request.json:
        abort(404)
    new_user = User(
        name=request.json["name"],
        primer_apellido=request.json["primer_apellido"],
        segundo_apellido=request.json["segundo_apellido"],
        email=request.json["email"],
        usuario=request.json["usuario"],
        ultimo_acceso=datetime.datetime.now(),
        departamento=request.json["departamento"],
        turno=request.json["turno"],
        RFFID=request.json["RFFID"],
        personal_externo=request.json["personal_externo"],
        RRHH=request.json["RRHH"],
        profile_picture=request.json["profile_picture"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"user": User.as_dict(new_user)}), 201


@app.route(uri + "<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.json:
        abort(400)

    user = User.query.get_or_404(user_id)

    user.name = request.json["name"]
    db.session.commit()

    user.primer_apellido = request.json["primer_apellido"]
    db.session.commit()

    user.segundo_apellido = request.json["segundo_apellido"]
    db.session.commit()

    user.email = request.json["email"]
    db.session.commit()

    user.usuario = request.json["usuario"]
    db.session.commit()

    user.ultimo_acceso = datetime.datetime.now()
    db.session.commit()

    user.departamento = request.json["departamento"]
    db.session.commit()

    user.RFFID = request.json["RFFID"]
    db.session.commit()

    user.turno = request.json["turno"]
    db.session.commit()

    user.personal_externo = request.json["personal_externo"]
    db.session.commit()

    user.RRHH = request.json["RRHH"]
    db.session.commit()

    user.profile_picture = request.json["profile_picture"]
    db.session.commit()

    if "name" in request.json and type(request.json.get("name")) is not str:
        abort(400)

    if (
        "primer_apellido" in request.json
        and type(request.json.get("primer_apellido")) is not str
    ):
        abort(400)

    if (
        "segundo_apellido" in request.json
        and type(request.json.get("segundo_apellido")) is not str
    ):
        abort(400)

    if "email" in request.json and type(request.json.get("email")) is not str:
        abort(400)

    if "usuario" in request.json and type(request.json.get("usuario")) is not str:
        abort(400)

    if (
        "departamento" in request.json
        and type(request.json.get("departamento")) is not str
    ):
        abort(400)

    if "turno" in request.json and type(request.json.get("turno")) is not str:
        abort(400)

    if "RFFID" in request.json and type(request.json.get("RFFID")) is not int:
        abort(400)

    if (
        "personal_externo" in request.json
        and type(request.json.get("personal_externo")) is not bool
    ):
        abort(400)

    if "RRHH" in request.json and type(request.json.get("RRHH")) is not bool:
        abort(400)

    if (
        "profile_picture" in request.json
        and type(request.json.get("profile_picture")) is not str
    ):
        abort(400)

    return jsonify({"user": User.as_dict(user)}), 201


@app.route(uri + "<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)
