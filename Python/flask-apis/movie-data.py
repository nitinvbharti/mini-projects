################
# FLASK API ####
################

from flask import Flask, Response, request, abort
from flask import jsonify, json
from flask_restx import Api, Resource, fields

## Entry point
app = Flask(__name__)

## Initialize flask application
api = Api(app)

## Namespace factory
ns_movies = api.namespace('ns_movies', description = "Movies API")

## Load JSON data into dictionary
f = open("./movie-data.json", "r")
loaded_movies = json.load(f)
movie_info = {
    f'{dct["title"]}-{dct["year"]}': dct
    for dct in loaded_movies.get("movies_list")
}

## Movie data model
movie_data = api.model(
    'Movie Data', {
        "title": fields.String(description = "Title of movie", required = True),
        "year": fields.Integer(description = "Year released", required = True),
        "cast": fields.List(fields.String, description = "Cast of movie", required = True),
        "image": fields.Url(description = "Image Url", required = True),
        "description": fields.String(description = "Description of movie", required = True)
    }
)

## Application routes
@ns_movies.route("/")

class movies(Resource):
    
    ## Get movie info as JSON.
    def get(self):
        return jsonify(movie_info)
    
    ## Post method
    @api.expect(movie_data)
    def post(self):
        params = request.get_json()
        if (t:=params.get("title", "")) and (y:=params.get("year","")):
            try:
                new_id = f'{t}-{y}'
                if new_id in movie_info.keys():
                    abort(code=409, description="Movie already exists.")
                
                for p in params:
                    if p not in movie_data:
                        raise KeyError
                movie_info[new_id] = params
            except:
                abort(code= 400, description= 'Bad parameters')
        else:
            abort(code=400, description="Missing required information: Title and Year")
            
        return Response(status=200)
    
## New namespace for routing with movie id
@ns_movies.route("/<string:id>")

class movies(Resource):
    
    def get(self, id):
        if id not in movie_info.keys():
            abort(code=404, description= f"Movie '{id}' doesn't exist.")
        return movie_info.get(id)
    
    ## PUT to update movie details
    @api.expect(movie_info)
    def put(self, id):
        if id not in movie_info.keys():
            abort(code=404, description= f"Movie '{id}' doesn't exist.")
        
        if not(params:=request.get_json()):
            abort(code=400, description="No parameters")
            
        for p in params:
            if p not in movie_info.keys():
                abort(code=400, description="Bad parameters")
        
        for p in params:
            movie_info[id][p]=params[p]
        
        return Response(status=200)
    
    ## DELETE movie by id
    def delete(self, id):
        try:
            del movie_info[id]
        except:
            abort(code=404, description= f"Movie '{id}' doesn't exist.")
        
        return Response(status=200)
    
if __name__ == "__main__":
    ## Run the app on localhost
    app.run(host='0.0.0.0', debug=True)