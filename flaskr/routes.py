import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .models import Composer, Performer, User
from . import db
from flask import request, abort, jsonify, render_template
import requests
from flask_cors import CORS, cross_origin  # type: ignore
from flask import Blueprint
# from .forms import ComposerForm
from typing import List, Optional, Dict, Any, Union
from .auth.auth import AuthError, jwt_required
from bucketControl import generate_presigned_url


api = Blueprint('api', __name__)  # type: ignore


ITEMS_PER_PAGE: int = 10


load_dotenv()

PORT = os.getenv("PORT", 5001)


def paginate_results(
    request,  # type: ignore
    selection: List[Union[Composer, Performer]]
) -> List[dict]:
    page: int = request.args.get("page", 1, type=int)
    start: int = (page - 1) * ITEMS_PER_PAGE
    end: int = start + ITEMS_PER_PAGE

    items: list = [i.format() for i in selection]
    current_items: list = items[start:end]

    return current_items


def create_dict(arr: List[Dict[str, Any]]) -> dict:
    cats_dict: Dict[Any, Any] = {}
    for x in arr:
        k = list(x.items())[0][1]
        v = list(x.items())[1][1]
        cats_dict[k] = v
    return cats_dict


# IMPLEMENT CROSS-ORIGIN RESOURCE SHARING FOR ALL ORIGINS
# CORS(api, origins=["*"])
CORS(api)


@api.after_request
def after_request(response):  # type: ignore
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response  # type: ignore

# ----------------------------HOME PAGE ROUTES-----------------------------------------#


@api.route("/")
def index() -> str:
    c_sltcn: List[Composer] = Composer.query.order_by(Composer.id).all()
    p_sltcn: List[Performer] = Performer.query.order_by(Performer.id).all()
    curr_composers_list: List[Dict[str, Any]
                              ] = paginate_results(request, c_sltcn)
    curr_performers_list: List[Dict[str, Any]
                               ] = paginate_results(request, p_sltcn)
    data: Dict[str, List[Dict[str, Any]]] = {"composers": curr_composers_list,
                                             "performers": curr_performers_list}

    return jsonify(
        {
            "success": True,
            "peformers": curr_performers_list,
            "total_performers": len(p_sltcn),
            "composers": curr_composers_list,
            "total_composers": len(c_sltcn),
        }
    )


@api.route("/composers")
@cross_origin()
def get_composers() -> str:
    sltcn = Composer.query.order_by(Composer.id).all()
    print(f"get slctn {sltcn}")
    current_slctn = paginate_results(request, sltcn)
    print(f"get current_slctn {current_slctn}")
    # cats = Category.query.all()

    # formatted_cats = [cat.format() for cat in cats]
    # cats_dict = create_dict(formatted_cats)
    if len(current_slctn) == 0:
        abort(404)

    # return render_template("composers.jinja-html", composers=current_slctn)

    return jsonify(
        {
            "success": True,
            "composers": current_slctn,
            "total_composers": len(sltcn),
            "current_category": 'all'
            # "categories": cats_dict
        }
    )


# @api.route("/composers/create")
# def show_form() -> str:
#     form = ComposerForm()  # type: ignore
#     return render_template('add_composer.jinja-html', form=form)

# @api.route("/admin/title")
# def show_form() -> str:
#     form = TitleForm()  # type: ignore
#     return render_template('add_title.jinja-html', form=form)


@api.route("/composers/create", methods=['POST'])
@jwt_required(allowed_roles=["user", "admin"])
def create_composer():
    try:
        # extract form data from the request object
        composer_name = request.form.get('name')
        year_born = request.form.get('born')
        year_deceased = request.form.get('deceased')
        nationality = request.form.get('nationality')

        composer = Composer(name=composer_name, year_born=year_born,
                            year_deceased=year_deceased, nationality=nationality)

        composer.insert()

        slctn = Composer.query.order_by(Composer.id).all()
        current_slctn = paginate_results(request, slctn)

        data = {
            'success': True,
            'created': composer.id,
            'composers': current_slctn,
            'total_Composers': len(slctn)
        }

        return jsonify(data)

    except Exception as e:
        print(e)
        return abort(400)

    # render_template("composers.jinja-html", data=data)

    return jsonify({
        'success': True,
        'created': composer.id,
        'composers': current_slctn,
        'total_Composers': len(slctn)
    })  # type: ignore


@api.route("/composers/<int:composer_id>")
def get_Composer(composer_id):
    # print(f"composer id {composer_id}")
    # composer = Composer.query.get(composer_id)
    composer = db.session.get(Composer, composer_id)

    formatted_composer = composer.format()

    return jsonify({
        'success': True,
        'composer': formatted_composer
    })  # type: ignore


@api.route("/composers/<int:pkey_id>", methods=['DELETE'])
@jwt_required(allowed_roles=["admin"])
def delete_composer(pkey_id):
    composer = Composer.query.filter(Composer.id == pkey_id).one_or_none()
    # print(f"composer is {composer.id}")

    if composer is None:
        abort(404)

    composer.delete()

    total = Composer.query.order_by(Composer.id).all()
    current_view = paginate_results(request, total)

    return jsonify({
        'success': True,
        'deleted': pkey_id,
        'composer': current_view,
        'total_composers': len(total)
    })  # type: ignore


"""Performer routes"""


@api.route("/performers")
def get_performers():
    total = Performer.query.order_by(Performer.id).all()
    current_view = paginate_results(request, total)

    return jsonify({
        "success": True,
        "performers": current_view,
        "total_performers": len(total),
        "current_category": 'all'
    })  # type: ignore


# @api.route('/performers/create', methods=['GET'])
# def create_performer_form():
#     from .forms import PerformerForm
#     # form = VenueForm(genres_choices=choices)
#     form = PerformerForm()
# #   form.genres.choices = models.get_choices()
#     # type: ignore
#     return render_template('forms/new_performer.html', form=form)


@api.route("/performers/create", methods=['POST'])
@jwt_required(allowed_roles=["user", "admin"])
def create_performer():
    req_body = request.get_json()
    # printf" loads json {json.loads("
    print(f"req body {req_body} type : {type(req_body)}")
    name = req_body.get("name")
    year_born = req_body.get("born")
    year_deceased = req_body.get("deceased", None)
    nationality = req_body.get("nationality")
    titles = req_body.get("titles", [])

    performer = Performer(
        name=name,
        year_born=year_born,
        year_deceased=year_deceased,
        nationality=nationality,
        titles=titles
    )
    performer.insert()
#     db.session.add(performer)
#     db.session.commit()

    total = Performer.query.order_by(Performer.id).all()
    current_view = paginate_results(request, total)

    return jsonify({
        "success": True,
        "created": performer.id,
        "performers": current_view,
        "total_performers_count": len(total)  # type: ignore
    })


@api.route('/performers/<int:pkey_id>')
def get_performer_by_id(pkey_id):
    try:
        performer = Performer.query.filter(
            Performer.id == pkey_id).one_or_none()

        formatted_performer = performer.format()

        return jsonify({
            'success': True,
            'performer': formatted_performer
        })  # type: ignore
    except:
        abort(404)  # type: ignore


@api.route("/performers/<int:pkey_id>", methods=['DELETE'])
@jwt_required(allowed_roles=["admin"])
def delete_performer(pkey_id):
    performer = Performer.query.filter(Performer.id == pkey_id).one_or_none()
    if performer is None:
        abort(404)  # type: ignore

    performer.delete()

    total = Performer.query.order_by(Performer.id).all()
    current_view = paginate_results(request, total)

    return jsonify({
        'success': True,
        'deleted': pkey_id,
        'current_performers': current_view,
        'total_Performerss': len(total)
    })  # type: ignore


@api.route('/presigned-url/<path:object_key>')
@cross_origin(origins="https://localhost:3000", allow_headers=["Content-Type", "Authorization"])
def get_presigned_url(object_key):
    bucket_name = 'mt-music-history'
    presigned_url = generate_presigned_url(bucket_name, object_key)

    if presigned_url is None:
        return jsonify({'error': 'Error generating pre-signed URL'}), 500

    return jsonify({'url': presigned_url})


@api.route("/exchange_for_token", methods=["POST"])
@cross_origin(origins="https://localhost:3000", allow_headers=["Content-Type", "Authorization"])
def exchange_for_token():
    # print("I can hear you")
    try:
        client_id = request.args.get("client_id")
        code = request.args.get("code")
        redirect_uri = request.args.get("redirect_uri")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        google_response = requests.post(
            "https://oauth2.googleapis.com/token",
            params={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }
        )

        access_token = google_response.json()["access_token"]
        
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        # Get user data from Google
        user_data = user_info_response.json()
        
        # Check if the user exists in your database
        user = User.query.filter_by(oauth_id=user_data["id"]).first()

        # If the user doesn't exist, create a new user record
        if user is None:
            user = User(
                oauth_provider="google",
                oauth_id=user_data["id"],
                email=user_data["email"],
                first_name=user_data["given_name"],
                last_name=user_data["family_name"],
                avatar_url=user_data["picture"],
                role="user",  # Assign a default role here or use logic to determine the role
            )
            user.insert()
        # Generate a JWT token for the user with the necessary claims
        jwt_token = generate_jwt_token(user)

        # Return the user data and JWT token to the frontend
        return jsonify({"user": user.format(), "token": jwt_token}), 200

    except Exception as error:
        print(error)
        return jsonify({"error": "Failed to exchange code for token"}), 500


def generate_jwt_token(user: User) -> str:
    # Read your JWT secret key from the environment
    jwt_secret = os.getenv("JWT_SECRET")
    if jwt_secret is None:
        raise ValueError("JWT_SECRET is not set in the environment")

    # Define the JWT token expiration time
    token_expiration = datetime.utcnow() + timedelta(hours=24)

    # Define the payload for the JWT token
    payload = {
        "sub": user.id,  # subject (user ID)
        "role": user.role,  # user role
        "exp": token_expiration,  # expiration time
    }

    # Encode and sign the JWT token
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    return token


def decode_jwt_token(encoded_jwt):
    jwt_secret = os.getenv("JWT_SECRET")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_secret, algorithms=["HS256"])
    return decoded_jwt

# ----------------------ADD PAGE-------------------------------#


# @api.route("/categories")
# def get_all_categories():
#     cats = Category.query.order_by(Category.id).all()
#     formatted_categories = [cat.format() for cat in cats]
#     cats_dict = create_dict(formatted_categories)

#     if len(cats) == 0:
#         abort(500)
#     return jsonify({
#         "success": True,
#         "categories": cats_dict
#     })


# @api.route('/quizzes', methods=['POST'])
# def play_quiz():
#     body = request.get_json()

#     previous_Composers_ids = body.get('previous_Composers', None)
#     quiz_category = body.get('quiz_category', None)
#     category = quiz_category['type']
#     Composers = Composer.query.all()

#     if quiz_category['type'] != "All":
#         Composers = Composer.query.filter(
#             Composer.category_id == quiz_category['id']).all()

#     if Composers:
    #     rand_index_num = random.randrange(len(Composers))
    # else:
    #     return jsonify({
    #         'success': True,
    #         'currentComposer': None
    #     })
    # rtrnObj = {}
    # current_Composer = None

    # if len(previous_Composers_ids) > 0:
    #     prevRange = []
    #     while Composers[rand_index_num].id in previous_Composers_ids:
    #         prevRange.append(rand_index_num)
    #         qsAvailable = [i for i in range(
    #             len(Composers)) if i not in prevRange]
    #         if qsAvailable:
    #             rand_index_num = choice(qsAvailable)
    #         else:
    #             break
    #     else:
    #         current_Composer = Composers[rand_index_num]
    # else:
    #     current_Composer = Composers[rand_index_num]
    # if not current_Composer:
    #     rtrnObj = {
    #         'success': True,
    #         'currentComposer': None
    #     }
    # else:
    #     rtrnObj = {
    #         'success': True,
    #         'currentComposer': current_Composer.format(),
    #     }
    # return jsonify(rtrnObj)


@api.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400,
                "message": "Bad request"}),
        400,
    )  # type: ignore


@api.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                "message": "resource not found"}),
        404,
    )  # type: ignore


@api.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405,
                "message": "method not allowed"}),
        405,
    )  # type: ignore


@api.errorhandler(422)
def unproccessable_entity(error):
    return (
        jsonify({"success": False, "error": 422,
                "message": "unproccessable entity"}),
        422,
    )  # type: ignore
